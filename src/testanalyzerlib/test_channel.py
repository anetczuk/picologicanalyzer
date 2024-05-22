#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from analyzerlib.bytearraychannel import ByteArrayChannel


class ChannelTest(unittest.TestCase):
    def test_write(self):
        stream = bytearray()
        host = ByteArrayChannel(stream)
        sensor = ByteArrayChannel(stream)

        host.write_byte(123)
        received = sensor.read_byte()
        self.assertEqual(received, 123)

    def test_communication(self):
        stream = bytearray()
        host = ByteArrayChannel(stream)
        sensor = ByteArrayChannel(stream)

        # send request
        host.write_text("aaa")
        host.write_int(4, 2)

        # receive request
        command = sensor.read_text()
        self.assertEqual(command, "aaa")

        requested_size = sensor.read_int(2)
        self.assertEqual(requested_size, 4)

        # send response
        sensor.write_text("bbb")
        sensor.write_int(4, 2)
        sensor.write_ints([1, 2, 3, 4])

        # receive response
        response = host.read_text()
        self.assertEqual(response, "bbb")

        response_size = host.read_int(2)
        self.assertEqual(response_size, 4)

        response_data = host.read_ints(response_size)
        self.assertEqual(response_data, [1, 2, 3, 4])
