#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Check if every character can be transferred through USB.
# Script fails in case of Keyboard Interrupt character (0x03).
# To prevent failure Keyboard Interrupt signal have to be disabled.
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

    for i in range(0, 256):
        data = bytes([i])
        connector.send_test_bytes_rqst(data, 1, 1)
        response = connector.wait_message()
        print(f"data: {data!r} response: {response}")
        received_data = int.from_bytes(response[1], "big")
        if received_data != i:
            print("invalid response")
            raise RuntimeError("invalid response")
        time.sleep(0.01)

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
