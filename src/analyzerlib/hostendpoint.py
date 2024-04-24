#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

from random import randrange

from analyzerlib.sensormessage import SensorMessage
from analyzerlib.hostconnector import HostConnector


class HostEndpoint(HostConnector):
    def send_bytes(self, data_bytes):
        self.channel.write_bytes(data_bytes)

    def receive_bytes(self, length) -> bytes:
        return self.channel.read_bytes(length)

    def send_text(self, content):
        self.channel.write_text(content)

    def receive_text(self):
        return self.channel.read_text()

    # useful in case of receiving invalid message
    def restore_connection(self):
        while True:
            print("clearing buffer")
            while True:
                data = self.receive_bytes(1)
                print("aaa:", data)
                if not data:
                    break
            print("sending test message")
            rand_num = randrange(256)
            rand_byte = bytes([rand_num])
            self.send_TEST_BYTES_RQST(rand_byte, 1)
            received = self.receive_message()
            print("xxxx:", rand_byte, received)
            if received[0] != SensorMessage.TEST_BYTES_RSPNS:
                continue
            received_data = received[1]
            if received_data == rand_byte:
                break
