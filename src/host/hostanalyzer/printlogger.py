#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys

from analyzerlib.logger import Logger
from analyzerlib.timefunc import get_current_time_str


try:
    from micropython import const  # pylint: disable=W0611

    mpython = True
except ImportError:
    import traceback
    mpython = False


class PrintLogger(Logger):
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):  # pylint: disable=W0622
        pass

    # =========================================

    def info(self, message):
        curr_time = get_current_time_str()
        print(f"{curr_time} INFO:  {message}")

    def warn(self, message):
        curr_time = get_current_time_str()
        print(f"{curr_time} WARN:  {message}")

    def error(self, message):
        curr_time = get_current_time_str()
        print(f"{curr_time} ERROR: {message}")

    def exception(self, exception):
        if mpython:
            curr_time = get_current_time_str()
            print(f"{curr_time} ERROR: received exception:")
            sys.print_exception(exception, self.file_obj)  # pylint: disable=E1101
        else:
            curr_time = get_current_time_str()
            print(f"{curr_time} ERROR: {traceback.format_exc()}")
