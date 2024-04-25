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
import micropython
import machine

from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensorendpoint import SensorEndpoint

import board
from filelogger import FileLogger
from sysstreamchannel import SysStreamChannel


def start(logger):
    # Set up the poll object
    poll_obj = select.poll()
    poll_obj.register(sys.stdin, select.POLLIN)

    channel = SysStreamChannel()
    connector = SensorEndpoint(channel, logger)

    keyboard_interrupt_enabled = True

    logger.info("starting")

    # button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  # GP21
    button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # GP21

    # Loop indefinitely
    while True:
        # toggle_led()

        # Wait for input on stdin
        # the '1' is how long it will wait for message before looping again (in microseconds)
        poll_results = poll_obj.poll(1)
        if poll_results:
            if keyboard_interrupt_enabled:
                keyboard_interrupt_enabled = False
                # disable keyboard interrupt (allow binary 0x03 characters instead of Control-C interrupt)
                micropython.kbd_intr(-1)
                utime.sleep(0.01)

            command_data = connector.receive_message()

            if command_data is None:
                # no incoming message
                continue

            command = command_data[0]

            # logger.info(f"received command: {HostMessage.get_id_from_value(command)}('{command}')")

            if command is None:
                # unknown command
                board.blink_led(0.01)
                # unknown_command = command_data[1]
                # logger.info(f"unknown command: '{unknown_command}'")
                invalid_command = command_data[1]
                connector.send_UNKNOWN_REQUEST_RSPNS(invalid_command)

            elif command == HostMessage.MEASURE_RQST:
                curr_state = button.value()
                # transfer_num = command_data[1]
                # data_size = command_data[2]
                values = bytearray([curr_state])
                connector.send_MEASURE_RSPNS(values)

            # elif command == HostMessage.CH_STATE_RQST:
            #     pass

            elif command == HostMessage.INTERNAL_TEMP_RQST:
                temp = board.read_temperaure()
                temp_date = int(temp * 100)
                # logger.info(f"sending temperature data: {temp} {temp_date}")
                connector.send_INTERNAL_TEMP_RSPNS(temp_date)

            elif command == HostMessage.SET_INTERNAL_LED_RQST:
                value = command_data[1]
                board.set_led(value)

            elif command == HostMessage.SET_KBD_INTR_RQST:
                value = command_data[1]
                if value == 0:
                    # disable keyboard interrupt (allow binary 0x03 characters instead of Control-C interrupt)
                    micropython.kbd_intr(-1)
                else:
                    # enable keyboard interrupt (allow connecting to REPL console various tools)
                    micropython.kbd_intr(3)
                utime.sleep(0.1)
                connector.send_SET_KBD_INTR_RSPNS()

            elif command == HostMessage.TEST_BYTES_RQST:
                data_content = command_data[1]
                transfer_num = command_data[2]
                # logger.info(f"sending test bytes data: {data_content} {transfer_num}")
                for _ in range(0, transfer_num):
                    connector.send_TEST_BYTES_RSPNS(data_content)

            elif command == HostMessage.TEST_TEXT_RQST:
                data_content = command_data[1]
                transfer_num = command_data[2]
                # logger.info(f"sending test text data: {data_content} {transfer_num}")
                for _ in range(0, transfer_num):
                    connector.send_TEST_TEXT_RSPNS(data_content)

            else:
                # unhandled command
                board.blink_led(0.01)
                logger.warn(f"unhandled command: {command_data}")
                connector.send_UNKNOWN_REQUEST_RSPNS(command)


# ==========================================================


def main():
    with FileLogger("log.txt", "a") as logger:
        logger.info("===== initializing =====")

        while True:
            board.blink_led(0.5)  # sleep 1 sec
            utime.sleep(0.5)
            board.blink_led(0.01)

            try:
                start(logger)

            except Exception as exc:  # pylint: disable=W0703
                logger.exception(exc)

            except KeyboardInterrupt as exc:  # pylint: disable=W0703
                logger.exception(exc)


main()
