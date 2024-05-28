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
import argparse
import serial

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from hostanalyzer.serialchannel import SerialChannel

from sample import plotutils


def perform_test(connector: HostEndpoint, plot_output=None, show_plot=False):
    print("starting")

    connector.send_set_measure_buff_size_rqst(3000)
    connector.wait_message()  # ack

    time.sleep(2)

    timestamps_num = 4

    transfers = 20

    plot_data = []

    # for measures_num in (10, 64, 100, 128, 160, 255, 500):
    for measures_num in range(8, 512 + 1, 8):
        expected_measures_num = measures_num * transfers

        diff_list = [0] * (timestamps_num - 1)
        for _ in range(0, transfers):

            # wait for expected number of measures in Pico buffer
            while True:
                connector.send_measured_no_rqst()
                message = connector.wait_message_type(SensorMessage.MEASURED_NO_RSPNS)
                measures_in_queue = message[1]
                if measures_num < measures_in_queue:
                    break
                print(f"waiting for measures {measures_num} in queue: {measures_in_queue}")
                time.sleep(1)

            connector.send_test_measure_time_rqst(measures_num)
            connector.wait_message()  # receive measurements itself

            timestamp_list = []
            for _ in range(0, timestamps_num):
                message = connector.wait_message()
                if message[0] != SensorMessage.CURRENT_TIME_US_RSPNS:
                    print("received invalid message:")
                    connector.print_message(message)
                    return
                timestamp_list.append(message[1])

            for i in range(1, timestamps_num):
                diff_time = timestamp_list[i] - timestamp_list[i - 1]
                diff_list[i - 1] += diff_time

        single_avg_list = [item / expected_measures_num for item in diff_list]
        single_avg_sum = sum(single_avg_list)
        single_avg_list.append(single_avg_sum)

        print(f"measures_num: {measures_num} transfers: {transfers} single measure avg: {single_avg_list} us")

        plot_data.append((measures_num, single_avg_list))

    plot_config = {
        "title": "duration of sending measures inside Pico",
        "xlabel": "number of measures per message",
        "ylabel": "time per measure [us]",
        "legendpos": "upper right",
        "labels": ["getting probe values", "converting to bytearray", "sending message", "total time"],
    }
    plotutils.image_xyplot(plot_data, plot_config, out_path=plot_output, show=show_plot)
    if plot_output:
        print("plot stored to:", plot_output)

    print("completed")


def main():
    parser = argparse.ArgumentParser(description="Calculate byte transfer")
    parser.add_argument("-sp", "--showplot", action="store_true", help="Show plot")
    parser.add_argument("-opf", "--outplotfile", action="store", default=None, help="Path to file to output plot")

    args = parser.parse_args()
    show_plot = args.showplot
    plot_output = args.outplotfile

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

            perform_test(connector, plot_output, show_plot)

        finally:
            connector.set_keyboard_interrupt(True)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
