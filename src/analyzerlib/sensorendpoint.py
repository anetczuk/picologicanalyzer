#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

from analyzerlib.sensorconnector import SensorConnector


class SensorEndpoint(SensorConnector):
    def send_bytes(self, data_bytes):
        self.channel.write_bytes(data_bytes)

    def receive_bytes(self, length) -> bytes:
        return self.channel.read_bytes(length)

    def send_text(self, content):
        self.channel.write_text(content)

    def receive_text(self):
        return self.channel.read_text()
