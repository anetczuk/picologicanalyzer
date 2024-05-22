#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Checking basic listener.
#

from filelogger import FileLogger

from listener import Listener


def start(logger: FileLogger) -> bool:
    listener = Listener(logger)
    return listener.listen()
