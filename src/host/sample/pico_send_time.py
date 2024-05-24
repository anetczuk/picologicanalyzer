#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Measure time of send data on Pico board.
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


def measure_avg(connector: HostEndpoint, response_size, avg_size):
    time_sum = 0
    for _ in range(0, avg_size):
        connector.send_TEST_TRANSFER_TIME_RQST(response_size)

        connector.wait_message()                # test bytes - ignore

        message1 = connector.wait_message()
        start_time_us = message1[1]
    
        message2 = connector.wait_message()
        end_time_us = message2[1]
    
        time_diff = (end_time_us - start_time_us) / 1000
        time_sum += time_diff
        
    time_avg = time_sum / avg_size
    return time_avg


def perform_test(connector: HostEndpoint):
    print("starting")

    avg_size = 100

    data_size = 0
    while data_size < 1024:
        data_size += 32
        time_avg = measure_avg(connector, data_size, avg_size)
        print(
            f"message size: {data_size} time avg: {time_avg} ms time per byte: {time_avg/data_size} ms"
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