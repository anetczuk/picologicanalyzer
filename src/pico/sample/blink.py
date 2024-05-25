#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Simply blink internal LED.
#

import utime
import board

from filelogger import FileLogger


def start(_: FileLogger) -> bool:
    # def start(logger: FileLogger) -> bool:
    while True:
        board.blink_led(0.2)
        utime.sleep(0.2)
    return False
