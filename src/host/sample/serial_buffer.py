#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Find buffer size of USB serial port.
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


def perform_test(connector: HostEndpoint):
    print("starting")

    data_size = 0
    while True:
        data_size += 64
        connector.send_test_bytes_rqst(b"0", 1, data_size)
        time.sleep(0.1)  # wait for data to arrive into internal buffer
        expected_message_size = 3 + data_size
        data = connector.receive_bytes(expected_message_size)
        received_size = len(data)

        print(f"expected: {expected_message_size} received: {received_size}")
        if expected_message_size != received_size:
            print("hit buffer limit")
            break

    print("completed")


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

        try:
            connector.set_keyboard_interrupt(False)

            perform_test(connector)

        finally:
            connector.set_keyboard_interrupt(True)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
