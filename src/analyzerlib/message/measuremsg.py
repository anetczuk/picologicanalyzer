#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#


def data_to_bytearray(measures_list):
    return bytearray(measures_list)


def bytearray_to_data(measures_data):
    return list(measures_data)
    # measures_len = len(measures_data)
    # ret_list = [0] * measures_len
    # for i in range(0, measures_len):
    #     ret_list[i] = measures_data[i]
    # return ret_list
