#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Execute each command and display return message.
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
import serial

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from analyzerlib.hostmessage import HostMessage
from hostanalyzer.serialchannel import SerialChannel


def perform_test(connector: HostEndpoint):
    print("starting")

    connector.send_set_kbd_intr_rqst(0)
    message = connector.wait_message()
    connector.print_message(message)

    connector.send_internal_temp_rqst()
    message = connector.wait_message()
    connector.print_message(message)

    connector.send_select_channels_rqst(1)
    message = connector.wait_message()
    connector.print_message(message)

    connector.send_measured_no_rqst()
    message = connector.wait_message()
    connector.print_message(message)

    connector.send_measure_rqst(10)
    message = connector.wait_message()
    connector.print_message(message)

    connector.send_measure_tr_rqst(10, 2)
    for _ in range(0, 2):
        message = connector.wait_message()
        connector.print_message(message)

    connector.send_measure_time_rqst(10)
    message = connector.wait_message()
    connector.print_message(message)

    print("completed")


def wait_message(connector: HostEndpoint):
    message = None
    while True:
        message = handle_message(connector)
        if message is None:
            continue
        if message[0] is None:
            continue
        break
    return message


def handle_message(connector: HostEndpoint):
    message = connector.receive_message()
    if message is None:
        print("no message - timeout")
        return message

    command = message[0]
    if command == SensorMessage.ACKNOWLEDGE_RSPNS:
        ack_command = message[1]
        if ack_command == HostMessage.SET_KBD_INTR_RQST:
            print("keyboard interrupt acknowledge")
            return message

    return message


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
