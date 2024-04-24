#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
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
from hostanalyzer.serialchannel import SerialChannel
from hostanalyzer.printlogger import PrintLogger


def read_pico_temperature(connector: HostEndpoint):
    connector.send_INTERNAL_TEMP_RQST()
    message = connector.receive_message()
    temperature = message[1]
    if temperature is None:
        print("invalid data:", message)
        return
    temperature = temperature / 100.0
    print("current Pico temperature:", temperature)


def main():
    print("connecting")

    # open a serial connection
    with serial.Serial(
        port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1
    ) as medium:
        logger = PrintLogger()
        medium.flush()
        channel = SerialChannel(medium)
        connector = HostEndpoint(channel, logger)

        for _ in range(0, 5):
            read_pico_temperature(connector)
            time.sleep(0.5)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
