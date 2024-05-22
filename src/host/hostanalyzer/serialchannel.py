#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import math
import serial

from analyzerlib.channel import AbstractChannel


class SerialChannel(AbstractChannel):
    def __init__(self, serialobj: serial.Serial):
        super().__init__()
        self.serial: serial.Serial = serialobj  # communication medium

    def reset_input_buffer(self):
        self.serial.reset_input_buffer()

    def reset_output_buffer(self):
        self.serial.reset_output_buffer()

    def write_byte(self, number):
        # data_bytes = number.to_bytes(1, byteorder="big")
        data_bytes = bytearray([number])
        self.serial.write(data_bytes)

    def read_byte(self):
        bytes_array = self.serial.read_until(size=1)
        if not bytes_array:
            return None
        return bytes_array[0]

    def write_bytes(self, data_bytes: bytes):
        self.serial.write(data_bytes)

    def read_bytes(self, length) -> bytes:
        # "serial.read_until()" interrupts after receiving character '\n', so
        # it won't receive desired number of bytes
        # to make it work properly receive data in loop
        receive_count = length
        received_data = bytes()
        while receive_count > 0:
            received = self.serial.read_until(size=receive_count)
            if not received:
                # no data in buffer
                break
            receive_count -= len(received)
            received_data += received
        return received_data

    def write_int(self, number, length):
        if number >= math.pow(2, 8 * length):
            raise ValueError(f"number {number} does not fit in array of size {length}")
        data_bytes = number.to_bytes(length, byteorder="big")
        self.serial.write(data_bytes)

    def read_int(self, length):
        data_bytes = self.read_bytes(length)
        if not data_bytes:
            return None
        return int.from_bytes(data_bytes, "big")

    def write_ints(self, int_list):
        data_bytes = bytearray(int_list)
        self.serial.write(data_bytes)

    def read_ints(self, length):
        data_bytes = self.read_bytes(length)
        if not data_bytes:
            return None
        return list(data_bytes)

    def write_text(self, content):
        line = content + "\n"
        data_bytes = bytearray(line, encoding="utf8")
        self.serial.write(data_bytes)

    def read_text(self):
        data_bytes = self.serial.read_until()
        content = data_bytes.decode()
        if content:
            content = content[:-1]
        return content
