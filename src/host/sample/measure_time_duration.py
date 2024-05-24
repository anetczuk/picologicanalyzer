#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Measure duration of MEASURE_TIME_RQST request.
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
    timestamps_num = 4

    data_transfer_limit = 10300

    # for measures_num in (10, 64, 100, 128, 160, 255, 500):
    for measures_num in range(8, 512 + 1, 8):
        transfers = int(data_transfer_limit / (measures_num * 4))   # each measurement takes 4 bytes
        transfers = max(transfers, 1)
        connector.send_MEASURED_NO_RQST()
        message = connector.wait_message_type( SensorMessage.MEASURED_NO_RSPNS )

        expected_measures_num = measures_num * transfers
        measures_in_queue = message[1]
        if expected_measures_num > measures_in_queue:
            print("warning! not enough measures in Pico queue! Returned times might be harmed!") 

        diff_list = [0] * (timestamps_num - 1)
        for _ in range(0, transfers):

            connector.send_TEST_MEASURE_TIME_RQST(measures_num)
            connector.receive_message()                     # receive measurements itself

            timestamp_list = []
            for _ in range(0, timestamps_num):
                message = connector.receive_message()
                if message[0] != SensorMessage.CURRENT_TIME_US_RSPNS:
                    print("received invalid message:")
                    connector.print_message(message)
                    return
                timestamp_list.append(message[1])

            for i in range(1, timestamps_num):
                diff_time = timestamp_list[i] - timestamp_list[i-1]
                diff_list[i-1] += diff_time

        single_avg_list = [item / expected_measures_num for item in diff_list]
        single_avg_sum = sum(single_avg_list)
        single_avg_list.append(single_avg_sum)

        print(
            f"measures_num: {measures_num} iters: {transfers}"
            f" single avg: {single_avg_list} us"
        )

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

        except KeyboardInterrupt:
            raise

        finally:
            connector.set_keyboard_interrupt(True)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
