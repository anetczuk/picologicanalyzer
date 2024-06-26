#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import select
import time
import utime
import machine
import micropython

from filelogger import FileLogger
from sysstreamchannel import SysStreamChannel
import board

from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensorendpoint import SensorEndpoint
from analyzerlib.message import measuremsg, measuretimemsg


def read_channel_state():
    return 0x00


class Probe:
    def value(self):
        raise NotImplementedError("not implemented")

    def value_list(self, measurements):
        raise NotImplementedError("not implemented")

    def time_value_list(self, measurements):
        raise NotImplementedError("not implemented")

    def time_value_bytearray(self, measurements):
        raise NotImplementedError("not implemented")


class DirectProbe(Probe):
    def __init__(self):
        super().__init__()
        # self.probe_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  # GP21
        self.probe_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # GP21

    def value(self) -> int:
        return self.probe_pin.value()  # int

    def value_list(self, measurements):
        ret_list = [0] * measurements
        for i in range(0, measurements):
            ret_list[i] = self.probe_pin.value()  # type: int
        return ret_list

    def time_value_list(self, measurements):
        ret_list = [None] * measurements
        for i in range(0, measurements):
            curr_time = time.ticks_us()  # pylint: disable=E1101
            curr_state = self.probe_pin.value()  # type: int
            ret_list[i] = (curr_time, curr_state)
        return ret_list

    def time_value_bytearray(self, measurements):
        measurements_list = self.time_value_list(measurements)
        return measuretimemsg.data_to_bytearray(measurements_list)


#
# Inheritance (method override) and lookup dict have almost exactly the same performance.
#
class Listener:
    def __init__(self, logger: FileLogger, probe: Probe = None):
        self.logger: FileLogger = logger
        self.channel = SysStreamChannel()
        self.connector = SensorEndpoint(self.channel)

        self.probe = probe
        if self.probe is None:
            self.probe = DirectProbe()

        # under MicroPython lookup dict is significantly faster than if-else chain
        self.lookup_dict = {
            HostMessage.SET_KBD_INTR_RQST: self._handle_set_kbd_intr_rqst,
            HostMessage.TERMINATE_RQST: self._handle_terminate_rqst,
            HostMessage.SET_INTERNAL_LED_RQST: self._handle_set_internal_led_rqst,
            HostMessage.CURRENT_TIME_MS_RQST: self._handle_current_time_ms_rqst,
            HostMessage.CURRENT_TIME_US_RQST: self._handle_current_time_us_rqst,
            HostMessage.CURRENT_TIME_CPU_RQST: self._handle_current_time_cpu_rqst,
            HostMessage.INTERNAL_TEMP_RQST: self._handle_internal_temp_rqst,
            HostMessage.CHANNEL_STATE_RQST: self._handle_channel_state_rqst,
            HostMessage.SELECT_CHANNELS_RQST: self._handle_select_channels_rqst,
            HostMessage.SET_MEASURE_BUFF_SIZE_RQST: self._handle_set_measure_buff_size_rqst,
            HostMessage.MEASURED_NO_RQST: self._handle_measured_no_rqst,
            HostMessage.MEASURE_RQST: self._handle_measure_rqst,
            HostMessage.MEASURE_TR_RQST: self._handle_measure_tr_rqst,
            HostMessage.MEASURE_TIME_RQST: self._handle_measure_time_rqst,
            HostMessage.MEASURE_TIME_TR_RQST: self._handle_measure_time_tr_rqst,
            HostMessage.TEST_TRANSFER_TIME_RQST: self._handle_test_transfer_time_rqst,
            HostMessage.TEST_MEASURE_TIME_RQST: self._handle_test_measure_time_rqst,
            HostMessage.TEST_BYTES_RQST: self._handle_test_bytes_rqst,
            HostMessage.TEST_TEXT_RQST: self._handle_test_text_rqst,
        }

        self.running_loop: bool = True
        self.result = True

    def stop_loop(self):
        self.running_loop = False

    def listen(self) -> bool:
        # Set up the poll object
        poll_obj = select.poll()
        poll_obj.register(sys.stdin, select.POLLIN)

        self.logger.info("starting")

        # Loop indefinitely
        self.running_loop = True
        while self.running_loop:
            # Wait for input on stdin
            # the '1' is how long it will wait for message before looping again (in microseconds)
            # poll_results = poll_obj.poll(1)
            # if poll_results:
            #     if not self.handle():
            #         return False

            poll_obj.poll()  # blocking wait (without parameters)

            command_data = self.connector.receive_message()
            callback = self.lookup_dict.get(command_data[0], self._handle__unhandled_command)
            if not callback(command_data):
                self.result = False
                return self.result

            # if not self.handle():
            #     self.result = False
            #     return self.result

        self.result = True
        return self.result

    def handle(self) -> bool:
        command_data = self.connector.receive_message()
        callback = self.lookup_dict.get(command_data[0], self._handle__unhandled_command)
        return callback(command_data)

    def _handle__unhandled_command(self, command_data):
        if self.logger:
            # unhandled command
            self.logger.warn(f"unhandled command: {command_data}")

        # if command is None:
        #     # no incoming message (timeout)
        #     return True
        #
        # board.blink_led(0.01)
        # self.connector.send_unknown_request_rspns(command)
        return True

    def _handle_set_kbd_intr_rqst(self, command_data):
        value = command_data[1]
        if value == 0:
            # disable keyboard interrupt (allow binary 0x03 characters instead of Control-C interrupt)
            micropython.kbd_intr(-1)
        else:
            # enable keyboard interrupt (allow connecting to REPL console various tools)
            micropython.kbd_intr(3)
        utime.sleep(0.1)
        self.connector.send_acknowledge_rspns(HostMessage.SET_KBD_INTR_RQST)
        return True

    def _handle_terminate_rqst(self, _):
        # exit the program
        self.logger.warn("received termination request")
        return False

    def _handle_set_internal_led_rqst(self, command_data):
        value = command_data[1]
        board.set_led(value)
        return True

    def _handle_current_time_ms_rqst(self, _):
        time_value = time.ticks_ms()  # pylint: disable=E1101
        self.connector.send_current_time_ms_rspns(time_value)
        return True

    def _handle_current_time_us_rqst(self, _):
        time_value = time.ticks_us()  # pylint: disable=E1101
        self.connector.send_current_time_us_rspns(time_value)
        return True

    def _handle_current_time_cpu_rqst(self, _):
        time_value = time.ticks_cpu()  # pylint: disable=E1101
        self.connector.send_current_time_cpu_rspns(time_value)
        return True

    def _handle_internal_temp_rqst(self, _):
        temp = board.read_temperaure()
        temp_date = int(temp * 100)
        # logger.info(f"sending temperature data: {temp} {temp_date}")
        self.connector.send_internal_temp_rspns(temp_date)
        return True

    def _handle_channel_state_rqst(self, _):
        channel_flags = read_channel_state()
        self.connector.send_channel_state_rspns(channel_flags)
        return True

    def _handle_select_channels_rqst(self, _):
        # channel_flags = command_data[1]
        channel_flags = read_channel_state()
        self.connector.send_channel_state_rspns(channel_flags)
        return True

    def _handle_set_measure_buff_size_rqst(self, command_data):
        command = command_data[0]
        self.connector.send_unknown_request_rspns(command)
        return True

    def _handle_measured_no_rqst(self, command_data):
        command = command_data[0]
        self.connector.send_unknown_request_rspns(command)
        return True

    def _handle_measure_rqst(self, command_data):
        measure_num = command_data[1]
        measures_list = self.probe.value_list(measure_num)
        measures_data = measuremsg.data_to_bytearray(measures_list)
        self.connector.send_measure_rspns(measures_data)
        return True

    def _handle_measure_tr_rqst(self, command_data):
        measure_num = command_data[1]
        transfer_num = command_data[2]
        for _ in range(0, transfer_num):
            measures_list = self.probe.value_list(measure_num)
            measures_data = measuremsg.data_to_bytearray(measures_list)
            self.connector.send_measure_rspns(measures_data)
        return True

    def _handle_measure_time_rqst(self, command_data):
        measurements_list = self.probe.time_value_list(command_data[1])
        measures_data = measuretimemsg.data_to_bytearray(measurements_list)
        self.connector.send_measure_time_rspns(measures_data)
        return True

    def _handle_measure_time_tr_rqst(self, command_data):
        params_multiplier = command_data[3]
        measures = command_data[1] * params_multiplier
        transfers = command_data[2] * params_multiplier
        # measures_data = bytearray(b'00000' * measures)
        # measurements_list = [(0,0)] * measures

        for _ in range(0, transfers):
            measures_data = self.probe.time_value_bytearray(measures)  # faster ~1k Hz
            self.connector.send_measure_time_rspns(measures_data)

            # measurements_list = self.probe.time_value_list(measures)
            # measures_data = measuretimemsg.data_to_bytearray(measurements_list)
            # self.connector.send_measure_time_rspns(measures_data)

        return True

    def _handle_test_measure_time_rqst(self, command_data):
        time_value1 = time.ticks_us()  # pylint: disable=E1101
        measurements_list = self.probe.time_value_list(command_data[1])
        time_value2 = time.ticks_us()  # pylint: disable=E1101
        measures_data = measuretimemsg.data_to_bytearray(measurements_list)
        time_value3 = time.ticks_us()  # pylint: disable=E1101
        self.connector.send_measure_time_rspns(measures_data)
        time_value4 = time.ticks_us()  # pylint: disable=E1101
        self.connector.send_current_time_us_rspns(time_value1)
        self.connector.send_current_time_us_rspns(time_value2)
        self.connector.send_current_time_us_rspns(time_value3)
        self.connector.send_current_time_us_rspns(time_value4)
        return True

    def _handle_test_transfer_time_rqst(self, command_data):
        response_size = command_data[1]
        response = bytearray()
        if response_size > 0:
            response = bytearray([0] * response_size)

        time_value1 = time.ticks_us()  # pylint: disable=E1101
        self.connector.send_test_bytes_rspns(response)
        time_value2 = time.ticks_us()  # pylint: disable=E1101

        self.connector.send_current_time_us_rspns(time_value1)
        self.connector.send_current_time_us_rspns(time_value2)
        return True

    def _handle_test_bytes_rqst(self, command_data):
        data_content = command_data[1]
        transfer_num = command_data[2]
        data_multiplier = command_data[3]
        if data_multiplier > 1:
            data_content = data_content * data_multiplier
        # logger.info(f"sending test bytes data: {data_content} {transfer_num}")
        for _ in range(0, transfer_num):
            self.connector.send_test_bytes_rspns(data_content)
        return True

    def _handle_test_text_rqst(self, command_data):
        data_content = command_data[1]
        transfer_num = command_data[2]
        # logger.info(f"sending test text data: {data_content} {transfer_num}")
        for _ in range(0, transfer_num):
            self.connector.send_test_text_rspns(data_content)
        return True
