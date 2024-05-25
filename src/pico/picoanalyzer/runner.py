#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import _thread
import time
import utime
import machine

from filelogger import FileLogger
from ringbuffer import RingBuffer, TimeValueRingBuffer
from ringbuffer import TimeMeasureContainer
from listener import Listener
from listener import Probe


class ProbeThread:
    def __init__(self, logger: FileLogger):
        self.logger: FileLogger = logger
        self.measurement_thread = None
        self.running = True

        # warning! lock cannot be aquired by the same thread twice (not RLock)
        self.ring_lock = _thread.allocate_lock()
        self.measure_queue = RingBuffer(5000, self.ring_lock)

        self.probe_delay_us = 0

        # self.probe = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  # GP21
        self.probe = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # GP21

    def start_thread(self):
        self.running = True
        self.measurement_thread = _thread.start_new_thread(self.run, ())  # type: int

    def stop_thread(self):
        self.running = False

    def run(self):
        try:
            # gc.disable()
            # gc.collect()    # takes 8ms, sometimes 11ms

            # gc.threshold(100000)

            # last_time = 0
            while self.running:
                # board.blink_led(0.1)
                # utime.sleep(0.1)

                time_value = time.ticks_us()  # pylint: disable=E1101
                curr_state = self.probe.value()
                # time_diff = time_value - last_time
                # time_diff = gc.mem_free()       # takes ~6.5ms
                # time_diff = gc.mem_alloc()      # takes ~6.5ms
                # last_time = time_value
                # self.measure_queue.put((time_diff, curr_state))
                self.measure_queue.put((time_value, curr_state))

                if self.probe_delay_us > 0:
                    # reduce probe frequency to allow communication to transfer
                    # all values without overflow
                    utime.sleep_us(self.probe_delay_us)

        except BaseException as exc:  # pylint: disable=W0703
            self.logger.exception(exc)
            raise


# ====================================================


class ProbeContainer(TimeMeasureContainer):
    def __init__(self):
        self.measure_data = bytearray()

    def append(self, timestamp, value):
        self.measure_data.extend(timestamp.to_bytes(3, "big"))
        self.measure_data.append(value)


class QueueProbe(Probe):
    def __init__(self, measure_queue: RingBuffer):
        super().__init__()
        self.measure_queue: RingBuffer = measure_queue

    def value(self) -> int:
        measurement_list = self.measure_queue.get_wait(1)
        return measurement_list[0][1]

    def value_list(self, measurements):
        measurement_list = self.measure_queue.get_wait(measurements)
        ret_list = [0] * measurements
        for m in range(0, measurements):
            ret_list[m] = measurement_list[m][1]
        return ret_list

    def time_value_list(self, measurements):
        return self.measure_queue.get_nowait(measurements)
        # return self.measure_queue.get_wait(measurements)

    def time_value_bytearray(self, measurements):
        measure_data = bytearray()
        self.measure_queue.get_nowait_buffer(measurements, measure_data)
        return measure_data
        # buffer = ProbeContainer()
        # self.measure_queue.get_nowait_buffer(measurements, buffer)
        # return buffer.measure_data


# class IRQLock:
#
#     def __init__(self):
#         self.irq_state = None
#
#     def __enter__(self):
#         self.irq_state = machine.disable_irq() # Start of critical section
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         machine.enable_irq(self.irq_state) # End of critical section


class MeasureListener(Listener):
    def __init__(self, logger: FileLogger):
        # self.measurement = ProbeThread(logger)
        # probe = QueueProbe(self.measurement.measure_queue)

        # self.probe_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  # GP21
        self.probe_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # GP21

        self.measure_queue = TimeValueRingBuffer(3000)
        probe = QueueProbe(self.measure_queue)
        super().__init__(logger, probe=probe)

        # self._scheduled_callback_ref = self._scheduled_callback
        self.irq_counter = 0

    def _handle_set_measure_buff_size_rqst(self, command_data):
        command = command_data[0]
        buffer_size = command_data[1]

        self.stop_probe()  # start of critical section
        self.measure_queue.set_capacity(buffer_size)
        self.start_probe()  # end of critical section

        self.connector.send_acknowledge_rspns(command)
        return True

    def _handle_measured_no_rqst(self, _):
        # def _handle_measured_no_rqst(self, command_data):
        measure_size = self.measure_queue.size()
        self.connector.send_measured_no_rspns(measure_size)
        return True

    def start_probe(self):
        self.probe_pin.irq(handler=self.measure_queue.put_pin, hard=True)
        # self.probe_pin.irq(handler=self.measure_queue.put_pin, hard=False)    # harmed by garbage collector

        # self.probe_pin.irq(handler=self._callback, hard=True)
        # self.probe_pin.irq(handler=self._callback, hard=False)
        # self.measurement.start_thread()

    def stop_probe(self):
        self.probe_pin.irq(handler=None)
        # self.measurement.stop_thread()

    def _callback(self, pin):
        # time_value = time.ticks_us()
        # self.irq_counter += 1
        self.measure_queue.put(time.ticks_us(), pin.value())  # pylint: disable=E1101
        # self.measure_queue.put(self.irq_counter, pin.value())


# running listener on separate core significantly improve performance
class ListenerThread:
    def __init__(self, listener: MeasureListener):
        self.listener: MeasureListener = listener
        self.thread_id = None
        self.lock = _thread.allocate_lock()

    def start_thread(self):
        self.lock.acquire()
        self.thread_id = _thread.start_new_thread(self._run, ())  # type: int

    def stop_thread(self):
        self.listener.stop_loop()

    def join(self):
        self.lock.acquire()  # wait for release of lock

    def result(self):
        return self.listener.result

    def _run(self):
        try:
            self.listener.listen()

        except BaseException as exc:  # pylint: disable=W0703
            self.listener.logger.error("stopping thread loop - received general exception:")
            self.listener.logger.error(f"exception: {exc}")
            self.listener.logger.exception(exc)

        finally:
            self.listener.logger.info("listening stopped")
            self.lock.release()
            _thread.exit()


def start(logger: FileLogger) -> bool:
    listener = MeasureListener(logger)

    try:
        listener.start_probe()

        listener_thread = ListenerThread(listener)
        listener_thread.start_thread()
        listener_thread.join()

        logger.info("listener thread stopped")
        return listener_thread.result()

    finally:
        logger.info("stopping measure thread")
        listener_thread.stop_thread()
        listener.stop_probe()
