#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from hostanalyzer.timecorrect import TimeCorrect


class TimeCorrectTest(unittest.TestCase):

    def test_update(self):
        time_correct = TimeCorrect()
        measure_list = [[200, 1], [100, 0]]

        time_correct.update_measure_time_list(measure_list)

        self.assertEquals(measure_list, [[200, 1], [16777316, 0]])

    def test_update_02(self):
        time_correct = TimeCorrect()
        measure_list = [[300, 1], [200, 0], [100, 0]]

        time_correct.update_measure_time_list(measure_list)

        self.assertEquals(measure_list, [[300, 1], [16777416, 0], [33554532, 0]])

    def test_update_03(self):
        time_correct = TimeCorrect()

        time_correct.update_measure_time_list([[300, 1]])

        measure_list = [[200, 0], [100, 0]]
        time_correct.update_measure_time_list(measure_list)

        self.assertEquals(measure_list, [[16777416, 0], [33554532, 0]])
