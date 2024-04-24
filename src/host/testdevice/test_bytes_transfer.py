#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
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
from hostanalyzer.serialchannel import SerialChannel
from hostanalyzer.printlogger import PrintLogger


def test_bytes_transfer(connector: HostEndpoint):
    # there is maximum transfer 200k B/s
    # tsize 128 seems to be optimal value
    for tsize in (1, 64, 100, 128, 160, 255):
        count = 0
        transfers = 2000  # max 65535
        connector.send_TEST_BYTES_RQST(b"\x01" * tsize, transfers)
        start_time = time.time()
        for _ in range(0, transfers):
            response = connector.receive_message()
            data = response[1]
            if data is None:
                continue
            count += len(data)
        transfer_time = time.time() - start_time
        print(
            f"size: {tsize}: transfer: {transfer_time} secs, iters: {transfers}"
            f", iter: {transfer_time / transfers} secs"
            f", bytes: {count}, {count / transfer_time} bytes/sec"
        )

    print("completed")


def main():
    print("connecting")

    # open a serial connection
    with serial.Serial(
        port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1
    ) as medium:
        logger = PrintLogger()
        medium.flush()
        channel = SerialChannel(medium)
        connector = HostEndpoint(channel, logger)

        test_bytes_transfer(connector)

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
