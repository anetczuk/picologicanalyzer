#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#


class AbstractChannel:
    def write_byte(self, number):
        raise NotImplementedError()

    def read_byte(self):
        raise NotImplementedError()

    def write_bytes(self, data_bytes: bytes):
        raise NotImplementedError()

    def read_bytes(self, length) -> bytes:
        raise NotImplementedError()

    def write_int(self, number, length):
        raise NotImplementedError()

    def read_int(self, length):
        raise NotImplementedError()

    def write_ints(self, int_list):
        raise NotImplementedError()

    def read_ints(self, length):
        raise NotImplementedError()

    def write_text(self, content):
        raise NotImplementedError()

    def read_text(self):
        raise NotImplementedError()
