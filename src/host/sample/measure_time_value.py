#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Get measurements and calculate duration of each state.
# Check measurements. Check if every next measurement have opposite value (1 or 0).
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
from collections import Counter
from typing import List
import argparse
import serial

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from analyzerlib.message import measuretimemsg
from hostanalyzer.serialchannel import SerialChannel

from sample import plotutils


def perform_test(connector: HostEndpoint, plot_output=None, show_plot=False):
    print("starting")

    connector.send_set_measure_buff_size_rqst(3000)
    connector.wait_message()        # ack

    iters = 10
    measurements = 200
    print("iters num:", iters, "measurements per iter:", measurements)

    time_counter: Counter = Counter([])
    last_measure_time = None

    value_change_counter: Counter = Counter([])
    prev_value = None
    curr_value_count = 0

    received_meaurements_num = 0

    plot_data: List[int] = []

    prev_iter_time = time.time()
    for _ in range(0, iters):
        
        while True:
            connector.send_measured_no_rqst()
            message = connector.wait_message_type(SensorMessage.MEASURED_NO_RSPNS)
            measures_in_queue = message[1]
            if measurements < measures_in_queue:
                print(f"measures in queue: {measures_in_queue}")
                break
            print(f"waiting for measures {measurements} in queue: {measures_in_queue}")
            time.sleep(1)

        connector.send_measure_time_rqst(measurements)
        start_time = time.time()
        message = connector.wait_message()
        transfer_time = time.time() - start_time

        # connector.print_message(message)
        if message[0] != SensorMessage.MEASURE_TIME_RSPNS:
            print("unknown message: ", message)
            return

        message_array = message[1]
        measuretime_list = measuretimemsg.bytearray_to_data(message_array)

        measure_size = len(measuretime_list)
        received_meaurements_num += measure_size

        if measure_size < 1:
            prev_iter_time = time.time()
            print("received empty measurements")
            continue

        for curr_measure_item in measuretime_list:
            if last_measure_time is None:
                # first message
                last_measure_time = curr_measure_item[0]
                print("measure time:", curr_measure_item[0], "val:", curr_measure_item[1])
                prev_value = curr_measure_item[1]
                curr_value_count = 1
                continue
            time_diff = curr_measure_item[0] - last_measure_time
            time_counter.update([time_diff])
            # freq = 1000000 / time_diff
            # print(
            #     "measure time:",
            #     curr_measure_item[0],
            #     "val:",
            #     curr_measure_item[1],
            #     "diff:",
            #     time_diff,
            #     "us",
            #     freq,
            #     "Hz",
            # )
            last_measure_time = curr_measure_item[0]

            if curr_measure_item[1] == prev_value:
                curr_value_count += 1
            else:
                value_change_counter.update([curr_value_count])
                prev_value = curr_measure_item[1]
                curr_value_count = 1
            plot_data.append(time_diff)

        curr_iter_time = time.time()
        iter_duration = curr_iter_time - prev_iter_time
        prev_iter_time = curr_iter_time

        print(
            "measures:",
            measure_size,
            "transfer time:",
            transfer_time * 1000,
            "ms",
            "iter time:",
            iter_duration * 1000,
            "ms",
            "iter time per measure:",
            iter_duration * 1000 / measure_size,
            "ms",
        )

    value_change_counter.update([curr_value_count])

    min_delay = min(time_counter.keys())
    max_delay = max(time_counter.keys())
    print(f"min delay: {min_delay} max delay: {max_delay} span: {max_delay - min_delay}")

    print(f"received measurements: {received_meaurements_num} state repeated: {sorted(value_change_counter.items())}")

    plot_config = {'title': 'time between subsequent signal state changes',
                   'xlabel': 'measurement index',
                   'ylabel': 'measured half period [us]'} 

    # plotutils.image_hist(plot_data, plot_output, show_plot)
    data_pairs = list(enumerate(plot_data))
    plotutils.image_points(data_pairs, plot_config, out_path=plot_output, show=show_plot)
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
