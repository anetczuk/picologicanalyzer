#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#


class TimeCorrect:

    TIME_MAX = 16777216  # 2^24 is because 3 bytes timestamp is send in message

    def __init__(self):
        self.last_measure_time = None
        self.measure_time_offset = 0

    def update_measure_time_list(self, measure_list):
        measure_list_size = len(measure_list)
        if measure_list_size < 1:
            return
        if self.last_measure_time is None:
            self.last_measure_time = measure_list[0][0]
        prev_measure_time = measure_list[0][0]
        if measure_list[0][0] < self.last_measure_time:
            self.measure_time_offset += self.TIME_MAX
        measure_list[0][0] += self.measure_time_offset

        for i in range(1, measure_list_size):
            curr = measure_list[i]
            if curr[0] < prev_measure_time:
                self.measure_time_offset += self.TIME_MAX
            prev_measure_time = curr[0]
            curr[0] += self.measure_time_offset

        self.last_measure_time = prev_measure_time
