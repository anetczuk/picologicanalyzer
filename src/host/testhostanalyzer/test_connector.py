#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest
import time

from hostanalyzer.connector import Connector
from analyzerlib.bytearraychannel import ByteArrayChannel
from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensormessage import SensorMessage


class ConnectorMock(Connector):
    def __init__(self):
        channel = ByteArrayChannel()
        super().__init__(channel, None)


# class ConnectorTest(unittest.TestCase):
#     def test_log(self):
#         iters = 1000
#         connector = ConnectorMock()
#         connector.channel.write_bytes( bytearray([SensorMessage.ACKNOWLEDGE_RSPNS, 0] * iters) )
#
#         start_time = time.time()
#         for _ in range(0, iters):
#             connector.handle_message()
#         diff_time = (time.time() - start_time)
#         print(f"call time: {diff_time * 1000} ms item time: {diff_time / iters * 1000} ms")
