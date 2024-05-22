#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

## bit shifting seems not to improve performance
# def data_to_bytearray(measures_list):
#     values = bytearray()
#     for curr_item in measures_list:
#         values.extend(curr_item[0].to_bytes(3, "big"))
#     bool_flags = 0
#     for curr_item in measures_list:
#         bool_flags = bool_flags << 1 | curr_item[1]
#     bytes_num = int(len(measures_list)/8) + 1
#     values.extend(bool_flags.to_bytes(bytes_num, "big"))
#     return values
#
#
# def bytearray_to_data(measures_data):
#     measures_num = int(len(measures_data) * 8 / 24)
#     ret_list = [None] * measures_num
#     for i in range(0, measures_num):
#         time_offset = i * 3
#         time_array = measures_data[time_offset : time_offset + 3]
#         measure_time = int.from_bytes(time_array, "big")
#         ret_list[i] = [measure_time, 0]
#
#     value_offset = measures_num * 3
#     bool_flags_array = measures_data[value_offset: ]
#     bool_flags = int.from_bytes(bool_flags_array, "big")
#     for i in range(0, measures_num):
#         ret_list[i][1] = bool_flags & 1
#         bool_flags = bool_flags >> 1
#     return ret_list


def data_to_bytearray(measures_list):
    values = bytearray()
    for curr_item in measures_list:
        values.extend(curr_item[0].to_bytes(3, "big"))
        values.append(curr_item[1])   
    return values


def bytearray_to_data(measures_data):
    measures_num = int(len(measures_data) / 4)
    ret_list = [None] * measures_num
    for i in range(0, measures_num):
        time_offset = i * 4
        time_array = measures_data[time_offset : time_offset + 3]
        measure_time = int.from_bytes(time_array, "big")
        value = measures_data[time_offset + 3]
        ret_list[i] = (measure_time, value)
    return ret_list
