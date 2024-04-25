#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from picoanalyzer.filelogger import FileLogger


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as log_file:
        return log_file.read()


class FileLoggerTest(unittest.TestCase):
    def test_log(self):
        log_file_path = "/tmp/test_logger.txt"  # nosec
        with FileLogger(log_file_path, "w") as logger:
            logger.info("aaa")
            logger.warn("bbb")
            logger.error("ccc")

        content = read_file(log_file_path)
        self.assertRegex(content, r".*INFO:  aaa\n.*WARN:  bbb\n.*ERROR: ccc\n")

    def test_exception(self):
        log_file_path = "/tmp/test_logger.txt"  # nosec
        with FileLogger(log_file_path, "w") as logger:
            try:
                raise RuntimeError("exception example")
            except RuntimeError as exc:
                logger.exception(exc)

        content = read_file(log_file_path)
        self.assertRegex(content, r".*ERROR: exception example\n")
