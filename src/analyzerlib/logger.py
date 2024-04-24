#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#


class Logger:
    def info(self, message):
        raise NotImplementedError()

    def warn(self, message):
        raise NotImplementedError()

    def error(self, message):
        raise NotImplementedError()

    def exception(self, exception):
        raise NotImplementedError()
