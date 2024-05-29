#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Receive measurements and print it on stdout.
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
from analyzerlib.message import measuretimemsg
from hostanalyzer.serialchannel import SerialChannel
from hostanalyzer.timecorrect import TimeCorrect


def perform_test(connector: HostEndpoint):
    print("starting")

    measures_num = 1

    connector.send_set_measure_buff_size_rqst(3000)
    connector.wait_message()  # ack

    last_measure_time = None

    time_correct = TimeCorrect()

    while True:

        connector.send_measure_time_rqst(measures_num)

        message = connector.wait_message()

        # connector.print_message(message)
        if message[0] != SensorMessage.MEASURE_TIME_RSPNS:
            print("unknown message: ", message)
            return

        message_array = message[1]
        measuretime_list = measuretimemsg.bytearray_to_data(message_array)

        measure_size = len(measuretime_list)
        if measure_size < 1:
            # print("received empty measurements")
            continue

        time_correct.update_measure_time_list(measuretime_list)

        for curr_measure_item in measuretime_list:
            if last_measure_time is None:
                # first message
                last_measure_time = curr_measure_item[0]
                print("measure time:", curr_measure_item[0], "val:", curr_measure_item[1])
                continue

            time_diff = curr_measure_item[0] - last_measure_time

            freq = 1000000 / time_diff
            print(
                "measure time:",
                curr_measure_item[0],
                "val:",
                curr_measure_item[1],
                "diff:",
                time_diff,
                "us",
                freq,
                "Hz",
            )
            last_measure_time = curr_measure_item[0]

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
