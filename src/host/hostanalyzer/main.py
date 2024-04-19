#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import time
import serial

from analyzerlib.hostendpoint import HostEndpoint
from hostanalyzer.serialchannel import SerialChannel


def test_bytes_transfer(connector):
    # there is maximum transfer 200k B/s
    # tsize 128 seems to be optimal value
    for tsize in (1, 64, 100, 128, 160, 255):
        count = 0
        transfers = 2000  # max 65535
        connector.send_TEST_BYTES_REQUEST(b"\x01" * tsize, transfers)
        start_time = time.time()
        for _ in range(0, transfers):
            response = connector.receive_message()
            count += len(response[1])
        transfer_time = time.time() - start_time
        print(
            f"size: {tsize}: transfer: {transfer_time} secs, iters: {transfers}"
            f", iter: {transfer_time / transfers} secs"
            f", bytes: {count}, {count / transfer_time} bytes/sec"
        )


def test_text_transfer(connector):
    # there is maximum transfer 200k B/s
    # tsize 128 seems to be optimal value
    for tsize in (1, 64, 100, 128, 160, 255):
        # for tsize in (1, 50, 100, 200, 400):
        count = 0
        transfers = 2000  # max 65535
        connector.send_TEST_TEXT_REQUEST("a" * tsize, transfers)
        start_time = time.time()
        for _ in range(0, transfers):
            response = connector.receive_message()
            count += len(response[1])
        transfer_time = time.time() - start_time
        print(
            f"size: {tsize}: transfer: {transfer_time} secs, iters: {transfers}"
            f", iter: {transfer_time / transfers} secs"
            f", chars: {count}, {count / transfer_time} chars/sec"
        )


def main():
    print("connecting")

    # open a serial connection
    with serial.Serial(
        port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1
    ) as medium:
        medium.flush()
        channel = SerialChannel(medium)
        connector = HostEndpoint(channel)

        # test_bytes_transfer(connector)
        test_text_transfer(connector)
        #     time.sleep(1)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
