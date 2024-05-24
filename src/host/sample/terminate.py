#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Sending terminate command to stop Pico main loop..
#

try:
    ## following import success only when file is directly executed from command line
    ## otherwise will throw exception when executing as parameter for "python -m"
    # pylint: disable=W0611
    import __init__
except ImportError:
    ## when import fails then it means that the script was executed indirectly
    ## in this case __init__ is already loaded
    pass

import sys
import time
import serial

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from analyzerlib.hostmessage import HostMessage
from hostanalyzer.serialchannel import SerialChannel


def main():
    print("connecting")

    # open a serial connection
    with serial.Serial(
        port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1
    ) as medium:
        medium.flush()
        medium.reset_input_buffer()
        channel = SerialChannel(medium)
        connector = HostEndpoint(channel)

        # disable keyboard interrupts (allow value 0x03)
        connector.set_keyboard_interrupt(0)

        connector.send_INTERNAL_TEMP_RQST()
        message = connector.wait_message_type(SensorMessage.INTERNAL_TEMP_RSPNS)
        temperature = message[1] / 100.0
        print("current Pico temperature:", temperature)
        time.sleep(0.5)

        # enable keyboard interrupt
        connector.set_keyboard_interrupt(1)

        print("sending terminate signal")
        connector.send_TERMINATE_RQST()

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
