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
import serial

from collections import Counter

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from analyzerlib.hostmessage import HostMessage
from analyzerlib.message import measuretimemsg, measuremsg
from hostanalyzer.serialchannel import SerialChannel


def perform_test(connector: HostEndpoint):
    print("starting")

    iters = 300
    measurements = 200
    print("iters num:", iters, "measurements per iter:", measurements)

    time_counter = Counter([])
    last_measure_time = None

    value_change_counter = Counter([])
    prev_value = None
    curr_value_count = 0

    received_meaurements_num = 0

    prev_iter_time = time.time()
    for _ in range(0, iters):
        connector.send_MEASURE_TIME_RQST(measurements)
        start_time = time.time()
        message = wait_message(connector)
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
            freq = 1000000 / time_diff
            print("measure time:", curr_measure_item[0], "val:", curr_measure_item[1], "diff:", time_diff, "us", freq, "Hz")
            last_measure_time = curr_measure_item[0]

            if curr_measure_item[1] == prev_value:
                curr_value_count += 1
            else:
                value_change_counter.update([curr_value_count])
                prev_value = curr_measure_item[1]
                curr_value_count = 1

        curr_iter_time = time.time()
        iter_duration = curr_iter_time - prev_iter_time
        prev_iter_time = curr_iter_time

        print("measures:", measure_size,
              "transfer time:", transfer_time * 1000, "ms",
              "iter time:", iter_duration * 1000, "ms",
              "iter time per measure:", iter_duration * 1000 / measure_size, "ms")

    value_change_counter.update([curr_value_count])

    min_delay = min(time_counter.keys())
    max_delay = max(time_counter.keys())
    print(f"min delay: {min_delay} max delay: {max_delay} span: {max_delay - min_delay}")

    print(f"received measurements: {received_meaurements_num} state repeated: {sorted(value_change_counter.items())}")

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
        print("invalid message:", message)
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

        except KeyboardInterrupt:
            raise

        finally:
            connector.set_keyboard_interrupt(True)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
