#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Checking how pin interrupts work.
#

# import _thread
import time

# import board

from machine import Pin, Timer

from ringbuffer import TimeValueRingBuffer


time.sleep(3.0)

led = Pin(25, Pin.OUT)


def tick(_):
    # def tick(timer):
    led.toggle()


def init_irq():
    timer = Timer()
    # timer.init(freq=2, mode=Timer.PERIODIC, callback=tick)

    timer.init(freq=1, mode=Timer.PERIODIC, callback=tick)

    # _thread.exit()


# init_irq()
# measurement_thread = _thread.start_new_thread(init_irq, ())  # type: int


# ==================================


counter = 1

buffer = TimeValueRingBuffer(1000)


def pin_callback(pin):
    # global counter
    curr_time = time.ticks_us()  # pylint: disable=E1101
    pin_val = pin.value()  # ~23us
    # buffer.put_fast(curr_time, pin_val)        # ~70us

    index_put = (buffer.index_put + 1) % buffer.capacity  # local index 5 us faster than using object's member
    buffer.timestamp_data[index_put] = curr_time
    buffer.value_data[index_put] = pin_val
    buffer.index_put = index_put

    end_time = time.ticks_us()  # pylint: disable=E1101
    diff = time.ticks_diff(end_time, curr_time)  # pylint: disable=E1101
    print("irq duration:", diff, "us")
    # counter += 1


def init_pin():
    probe_pin = Pin(21, Pin.IN, Pin.PULL_DOWN)  # GP21
    # probe_pin.irq(handler=pin_callback, hard=True)
    probe_pin.irq(handler=buffer.put_pin, hard=False)
    # probe_pin.irq(handler=pin_callback, hard=False)


def run_loop():

    iteration = 0

    last_time = time.ticks_us()  # pylint: disable=E1101
    print("started", last_time, "us")

    # 10000 => 9793740 us
    # 1 => 979.3740 us

    #  18.747453 s
    # 118.680862 s

    while True:
        val = counter
        if val % 1000 == 0:
            curr_time = time.ticks_us()
            diff = time.ticks_diff(curr_time, last_time)
            iteration += 1
            print(iteration, "value4:", val, "time:", diff, "us", "curr time:", curr_time, "us")
            last_time = time.ticks_us()


try:

    # measurement_thread = _thread.start_new_thread(run_loop, ())  # type: int

    init_pin()

    run_loop()

except:  # pylint: disable=W0702  # noqa
    print("exception!")
