#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

try:
    from micropython import const  # pylint: disable=W0611

    mpython = True
except ImportError:
    mpython = False


if mpython:
    # micropython version

    import time

    # RPi Pico does not have persistent time clock, so it resets every time when the board is turned off
    # so more reliable is to show time since boot
    def get_current_time_str():
        time_ms = time.ticks_ms()  # pylint: disable=E1101
        millis = time_ms % 1000
        secs = int(time_ms / 1000)
        mins = int(secs / 60)
        hours = int(mins / 60)
        days = int(hours / 24)

        secs %= 60
        mins %= 60
        hours %= 24

        return f"{days:02} {hours:02}:{mins:02}:{secs:02}.{millis:03}"


else:
    # python version

    import datetime

    def get_current_time_str():
        curr_time = datetime.datetime.now()
        return str(curr_time)
