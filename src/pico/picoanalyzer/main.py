#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import select
import sys

# import time

# import machine
import utime

from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensorendpoint import SensorEndpoint

from board import blink_led, read_temperaure
from sysstreamchannel import SysStreamChannel


def start(logger):
    # Set up the poll object
    poll_obj = select.poll()
    poll_obj.register(sys.stdin, select.POLLIN)

    channel = SysStreamChannel()
    connector = SensorEndpoint(channel)

    print("starting")

    # Loop indefinitely
    while True:
        # toggle_led()

        # Wait for input on stdin
        # the '1' is how long it will wait for message before looping again (in microseconds)
        poll_results = poll_obj.poll(1)
        if poll_results:
            command_data = connector.receive_message()
            command = command_data[0]

            # logger.write(f"received command: '{command}'\n")

            if command is None:
                # unknown command
                blink_led(0.01)
                unknown_command = command_data[1]
                logger.write(f"unknown command: '{unknown_command}'\n")

            # elif command == HostMessage.REQUEST_DATA:
            #     pass
            #     # transfer_num = command_data[1]
            #     # data_size = command_data[2]
            #     connector.send_RESPONSE_DATA([0x03])

            # elif command == HostMessage.GET_CH_ENABLE:
            #     pass

            elif command == HostMessage.TEST_BYTES_RQST:
                data_content = command_data[1]
                transfer_num = command_data[2]
                for _ in range(0, transfer_num):
                    connector.send_TEST_BYTES_RSPNS(data_content)

            elif command == HostMessage.TEST_TEXT_RQST:
                data_content = command_data[1]
                transfer_num = command_data[2]
                for _ in range(0, transfer_num):
                    connector.send_TEST_TEXT_RSPNS(data_content)

            else:
                # unhandled command
                blink_led(0.01)
                unknown_command = command_data[1]
                logger.write(f"unhandled command: '{command}'\n")


def main():
    blink_led(0.5)  # sleep 1 sec
    utime.sleep(0.5)
    blink_led(0.01)

    with open("log.txt", "a", encoding="utf-8") as log_file:
        # with open("log.txt", "at", encoding="utf-8") as log_file:
        start(log_file)

    return 0


main()
