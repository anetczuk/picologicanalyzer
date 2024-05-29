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


import datetime

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensorendpoint import SensorEndpoint
from analyzerlib.bytearraychannel import ByteArrayChannel


def main():
    channel = ByteArrayChannel()
    host = HostEndpoint(channel)
    sensor = SensorEndpoint(channel)

    start_time = datetime.datetime.now()

    iters = 100000
    for _ in range(0, iters):
        host.send_test_bytes_rqst(b"\x01", 1, 1)
        sensor.receive_message()

    end_time = datetime.datetime.now()
    total_millis = (end_time - start_time).total_seconds() * 1000

    print("xxx:", total_millis, "ms")


if __name__ == "__main__":
    main()
