#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from analyzerlib.channel import ByteArrayChannel
from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensorendpoint import SensorEndpoint
from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensormessage import SensorMessage


class ProtocolTest(unittest.TestCase):
    def test_request_text(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        sensor.send_text("abcde")

        content = host.receive_text()
        self.assertEqual(content, "abcde")

    def test_request_data(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_MEASURE_RQST(4, 2)

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.MEASURE_RQST, 4, 2])

        sensor.send_MEASURE_RSPNS([1, 2, 3, 4])
        sensor.send_MEASURE_RSPNS([5, 6, 7, 8])

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.MEASURE_RSPNS, bytearray(b"\x01\x02\x03\x04")])
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.MEASURE_RSPNS, bytearray(b"\x05\x06\x07\x08")])

    def test_channel_enable(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_CH_STATE_RQST()

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.CH_STATE_RQST])

        sensor.send_CH_STATE_RSPNS(0x03)

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.CH_STATE_RSPNS, 0x03])

    def test_test_bytes(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_TEST_BYTES_RQST(b"\x01\x02\x03", 1)

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.TEST_BYTES_RQST, b"\x01\x02\x03", 1])

        sensor.send_TEST_BYTES_RSPNS(b"\x01\x02\x03")

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.TEST_BYTES_RSPNS, b"\x01\x02\x03"])

    def test_test_text(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_TEST_TEXT_RQST("abcd", 1)

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.TEST_TEXT_RQST, "abcd", 1])

        sensor.send_TEST_TEXT_RSPNS("abcd")

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.TEST_TEXT_RSPNS, "abcd"])
