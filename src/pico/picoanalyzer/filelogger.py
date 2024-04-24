#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys

from picoserial.timefunc import get_current_time_str
from picoserial.logger import Logger


try:
    from micropython import const  # pylint: disable=W0611

    mpython = True
except ImportError:
    mpython = False


class FileLogger(Logger):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)  # pylint: disable=R1732,W1514

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):  # pylint: disable=W0622
        self.file_obj.close()

    # =========================================

    def info(self, message):
        curr_time = get_current_time_str()
        self.file_obj.write(f"{curr_time} INFO:  {message}\n")
        self.file_obj.flush()

    def warn(self, message):
        curr_time = get_current_time_str()
        self.file_obj.write(f"{curr_time} WARN:  {message}\n")
        self.file_obj.flush()

    def error(self, message):
        curr_time = get_current_time_str()
        self.file_obj.write(f"{curr_time} ERROR: {message}\n")
        self.file_obj.flush()

    def exception(self, exception):
        if mpython:
            curr_time = get_current_time_str()
            self.file_obj.write(f"{curr_time} ERROR: exception:\n")
            sys.print_exception(exception, self.file_obj)  # pylint: disable=E1101
            self.file_obj.flush()
        else:
            curr_time = get_current_time_str()
            self.file_obj.write(f"{curr_time} ERROR: {exception}\n")
            self.file_obj.flush()
