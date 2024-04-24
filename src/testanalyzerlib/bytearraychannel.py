#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

from analyzerlib.channel import AbstractChannel


class ByteArrayChannel(AbstractChannel):
    def __init__(self, stream=None):
        super().__init__()
        if stream is None:
            stream = bytearray()
        self.stream = stream  # communication medium

    def write_byte(self, number):
        data_bytes = number.to_bytes(1, byteorder="big")
        self.stream.extend(data_bytes)

    def read_byte(self):
        data_bytes = self.stream[:1]
        self._rem_front(1)
        return data_bytes

    def write_bytes(self, data_bytes):
        self.stream.extend(data_bytes)

    def read_bytes(self, length) -> bytes:
        data_bytes = self.stream[:length]
        self._rem_front(length)
        return data_bytes

    def write_int(self, number, length):
        data_bytes = number.to_bytes(length, byteorder="big")
        self.stream.extend(data_bytes)

    def read_int(self, length):
        data_bytes = self.stream[:length]
        self._rem_front(length)
        return int.from_bytes(data_bytes, "big")

    def write_ints(self, int_list):
        data_bytes = bytearray(int_list)
        self.stream.extend(data_bytes)

    def read_ints(self, length):
        data_bytes = self.stream[:length]
        self._rem_front(length)
        return list(data_bytes)

    def write_text(self, content):
        line = content + "\n"
        data_bytes = bytearray(line, encoding="utf8")
        self.stream.extend(data_bytes)

    def read_text(self):
        pos = self.stream.find(ord("\n"))
        if pos < 0:
            return None
        part = self.stream[:pos]
        self._rem_front(pos + 1)
        return part.decode()

    def _rem_front(self, length):
        remaining = self.stream[length:]
        self.stream.clear()
        self.stream.extend(remaining)
