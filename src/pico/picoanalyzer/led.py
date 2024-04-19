#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import machine
import utime


# pylint: disable=W0603


led = machine.Pin(25, machine.Pin.OUT)
led_value = 0


def toggle_led():
    global led_value
    led_value = (led_value + 1) % 2  # toggle value
    led.value(led_value)


def blink_led(blink_duration=0.1):
    led.value(1)
    utime.sleep(blink_duration)
    led.value(0)
