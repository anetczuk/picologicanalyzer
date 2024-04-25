#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys

from analyzerlib.channel import AbstractChannel


class SysStreamChannel(AbstractChannel):
    def write_byte(self, number):
        data_bytes = number.to_bytes(1, "big")
        sys.stdout.buffer.write(data_bytes)

    def read_byte(self):
        return sys.stdin.buffer.read(1)

    def write_bytes(self, data_bytes: bytes):
        sys.stdout.buffer.write(data_bytes)

    def read_bytes(self, length) -> bytes:
        return sys.stdin.buffer.read(length)

    def write_int(self, number, length):
        data_bytes = number.to_bytes(length, "big")
        sys.stdout.buffer.write(data_bytes)

    def read_int(self, length):
        data_bytes = sys.stdin.buffer.read(length)
        return int.from_bytes(data_bytes, "big")

    def write_ints(self, int_list):
        data_bytes = bytearray(int_list)
        sys.stdout.buffer.write(data_bytes)

    def read_ints(self, length):
        data_bytes = sys.stdin.buffer.read(length)
        return list(data_bytes)

    def write_text(self, content):
        line = content + "\n"
        data_bytes = bytearray(line, "utf8")
        sys.stdout.buffer.write(data_bytes)

    def read_text(self):
        try:
            content = sys.stdin.readline()
            if content:
                content = content[:-1]
            return content
        except UnicodeError:
            # data transfer problem - discard data
            return None
