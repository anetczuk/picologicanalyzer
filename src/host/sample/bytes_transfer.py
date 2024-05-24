#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Measure transfer speed in function of message size
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


def perform_test(connector: HostEndpoint):
    print("starting")

    data_transfer_limit = 6300

    for data_size in range(8, 1024 + 1, 8):
        count = 0
        transfers = int(data_transfer_limit / data_size)
        transfers = max(transfers, 1)

        connector.send_TEST_BYTES_RQST(b"\x01", transfers, data_size)

        start_time = time.time()
        for _ in range(0, transfers):
            message = connector.wait_message()
            if message[0] != SensorMessage.TEST_BYTES_RSPNS:
                print("received invalid message:")
                connector.print_message(message)
                return
            data = message[1]
            if data is None:
                print("received invalid message:")
                return
            count += len(data)
        transfer_time = time.time() - start_time
        print(
            f"data_size: {data_size}: transfer: {transfer_time * 1000} ms, iters: {transfers}"
            f", iter: {transfer_time / transfers * 1000} ms"
            f", bytes: {count}, {count / transfer_time / 1024} KB/S"
        )

    print("completed")


def handle_message(connector: HostEndpoint):
    message = connector.receive_message()
    if message is None:
        print("invalid message:", message)
        return

    command = message[0]
    if command == SensorMessage.ACKNOWLEDGE_RSPNS:
        ack_command = message[1]
        if ack_command == HostMessage.SET_KBD_INTR_RQST:
            print("keyboard interrupt acknowledge")
            return


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

        except KeyboardInterrupt:
            raise

        finally:
            connector.set_keyboard_interrupt(True)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
