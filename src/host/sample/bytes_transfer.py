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
import argparse
import serial

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from hostanalyzer.serialchannel import SerialChannel

from sample import plotutils


def perform_test(connector: HostEndpoint, plot_output=None, show_plot=False):
    print("starting")

    data_transfer_limit = 6000

    plot_data = []

    for data_size in range(8, 1024 + 1, 8):
        count = 0
        transfers = int(data_transfer_limit / (data_size + 1))
        transfers = max(transfers, 1)

        start_time = time.time()

        connector.send_test_bytes_rqst(b"\x01", transfers, data_size)

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
        transfer_rate = count / transfer_time / 1024
        print(
            f"data_size: {data_size}: transfer: {transfer_time * 1000} ms, transfers: {transfers}"
            f", iter: {transfer_time / transfers * 1000} ms"
            f", bytes: {count}, {transfer_rate} KiB/s"
        )
        plot_data.append((data_size, transfer_rate))

    plot_config = {
        "title": "average send and receive time in relation to receive message size",
        "xlabel": "message size [B]",
        "ylabel": "transfer rate [KiB/s]",
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
