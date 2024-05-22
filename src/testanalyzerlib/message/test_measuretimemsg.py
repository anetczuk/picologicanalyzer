#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from analyzerlib.message import measuretimemsg


class MeasureTimeMsgTest(unittest.TestCase):
    def test_convert_empty(self):
        measures_list = []
        measures_array = measuretimemsg.data_to_bytearray(measures_list)
        measures2_list = measuretimemsg.bytearray_to_data(measures_array)
        self.assertEqual(measures_list, measures2_list)

    def test_convert_data(self):
        measures_list = [(0, 1), (2, 1)]
        measures_array = measuretimemsg.data_to_bytearray(measures_list)
        measures2_list = measuretimemsg.bytearray_to_data(measures_array)
        self.assertEqual(measures_list, measures2_list)
