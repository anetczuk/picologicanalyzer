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
        host.send_REQUEST_DATA(4, 2)

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.REQUEST_DATA, 4, 2])

        sensor.send_RESPONSE_DATA([1, 2, 3, 4])
        sensor.send_RESPONSE_DATA([5, 6, 7, 8])

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.RESPONSE_DATA, bytearray(b"\x01\x02\x03\x04")])
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.RESPONSE_DATA, bytearray(b"\x05\x06\x07\x08")])

    def test_channel_enable(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_GET_CH_ENABLE()

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.GET_CH_ENABLE])

        sensor.send_SEND_CH_ENABLE(0x03)

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.SEND_CH_ENABLE, 0x03])

    def test_test_bytes(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_TEST_BYTES_REQUEST(b"\x01\x02\x03", 1)

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.TEST_BYTES_REQUEST, b"\x01\x02\x03", 1])

        sensor.send_TEST_BYTES_RESPONSE(b"\x01\x02\x03")

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.TEST_BYTES_RESPONSE, b"\x01\x02\x03"])

    def test_test_text(self):
        channel = ByteArrayChannel()
        host = HostEndpoint(channel)
        sensor = SensorEndpoint(channel)

        # send request
        host.send_TEST_TEXT_REQUEST("abcd", 1)

        # receive request
        command = sensor.receive_message()
        self.assertEqual(command, [HostMessage.TEST_TEXT_REQUEST, "abcd", 1])

        sensor.send_TEST_TEXT_RESPONSE("abcd")

        # receive response
        response = host.receive_message()
        self.assertEqual(response, [SensorMessage.TEST_TEXT_RESPONSE, "abcd"])
