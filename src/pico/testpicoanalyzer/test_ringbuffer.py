#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest

from picoanalyzer.ringbuffer import RingBuffer, TimeValueRingBuffer


class LockMock:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None


class RingBufferMock(RingBuffer):
    def __init__(self, capacity):
        super().__init__(capacity, LockMock())


class RingBufferTest(unittest.TestCase):
    def test_put_get(self):
        buffer = RingBufferMock(3)

        self.assertEqual(buffer.size(), 0)
        self.assertTrue(buffer.is_empty())

        buffer.put(1)
        self.assertEqual(buffer.size(), 1)
        self.assertFalse(buffer.is_empty())

        buffer.put(2)
        self.assertEqual(buffer.size(), 2)
        self.assertFalse(buffer.is_empty())

        value = buffer.get()
        self.assertEqual(value, 1)
        self.assertEqual(buffer.size(), 1)
        self.assertFalse(buffer.is_empty())

        value = buffer.get()
        self.assertEqual(value, 2)
        self.assertEqual(buffer.size(), 0)
        self.assertTrue(buffer.is_empty())

    def test_size(self):
        buffer = RingBufferMock(2)
        self.assertEqual(buffer.size(), 0)

        buffer.put(1)
        self.assertEqual(buffer.size(), 1)

        buffer.put(2)
        self.assertEqual(buffer.size(), 2)

        buffer.get()
        self.assertEqual(buffer.size(), 1)

        buffer.get()
        self.assertEqual(buffer.size(), 0)

        buffer.get()
        self.assertEqual(buffer.size(), 0)

    # def test_overflow(self):
    #     buffer = RingBufferMock(2)
    #
    #     buffer.put(1)
    #     self.assertEqual(buffer.overflow_counter, 0)
    #
    #     buffer.put(2)
    #     self.assertEqual(buffer.overflow_counter, 1)
    #
    #     buffer.put(3)
    #     self.assertEqual(buffer.overflow_counter, 1)

    def test_overflow_02(self):
        buffer = RingBufferMock(5)

        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        buffer.put(4)
        buffer.put(5)
        buffer.put(6)
        self.assertEqual(buffer.overflow_counter, 1)
        self.assertEqual(buffer.size(), 5)
        self.assertEqual(buffer.next(), 2)

        buffer.put(7)
        self.assertEqual(buffer.overflow_counter, 2)
        self.assertEqual(buffer.size(), 5)
        self.assertEqual(buffer.get(), 3)

    def test_get_nowait_01(self):
        buffer = RingBufferMock(4)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)

        ret_list = buffer.get_nowait(5)
        self.assertEqual(ret_list, [1, 2, 3])
        self.assertEqual(buffer.size(), 0)

    def test_get_nowait_02(self):
        buffer = RingBufferMock(4)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)

        ret_list = buffer.get_nowait(2)
        self.assertEqual(ret_list, [1, 2])
        self.assertEqual(buffer.size(), 1)

    # def test_xxxx(self):
    #     buffer = RingBufferMock(100)
    #     for i in range(0, 60):
    #         buffer.put(i)
    #     ret_list = buffer.get_nowait(40)
    #     print("xxx:", ret_list)
    #
    #     for i in range(60, 120):
    #         buffer.put(i)
    #     ret_list = buffer.get_nowait(40)
    #     print("xxx:", ret_list)


class TimeRingBufferTest(unittest.TestCase):
    def test_put_get(self):
        buffer = TimeValueRingBuffer(3)

        self.assertEqual(buffer.size(), 0)
        self.assertTrue(buffer.is_empty())

        buffer.put(1, 1)
        self.assertEqual(buffer.size(), 1)
        self.assertFalse(buffer.is_empty())

        buffer.put(2, 2)
        self.assertEqual(buffer.size(), 2)
        self.assertFalse(buffer.is_empty())

        value = buffer.get()
        self.assertEqual(value, [1, 1])
        self.assertEqual(buffer.size(), 1)
        self.assertFalse(buffer.is_empty())

        value = buffer.get()
        self.assertEqual(value, [2, 2])
        self.assertEqual(buffer.size(), 0)
        self.assertTrue(buffer.is_empty())

    def test_size(self):
        buffer = TimeValueRingBuffer(3)
        self.assertEqual(buffer.size(), 0)

        buffer.put(1, 1)
        self.assertEqual(buffer.size(), 1)

        buffer.put(2, 2)
        self.assertEqual(buffer.size(), 2)

        buffer.get()
        self.assertEqual(buffer.size(), 1)

        buffer.get()
        self.assertEqual(buffer.size(), 0)

        buffer.get()
        self.assertEqual(buffer.size(), 0)

    def test_get_nowait_01(self):
        buffer = TimeValueRingBuffer(4)
        buffer.put(1, 1)
        buffer.put(2, 2)
        buffer.put(3, 3)

        ret_list = buffer.get_nowait(5)
        self.assertEqual(ret_list, [[1, 1], [2, 2], [3, 3]])
        self.assertEqual(buffer.size(), 0)

    def test_get_nowait_02(self):
        buffer = TimeValueRingBuffer(4)
        buffer.put(1, 1)
        buffer.put(2, 2)
        buffer.put(3, 3)

        ret_list = buffer.get_nowait(2)
        self.assertEqual(ret_list, [[1, 1], [2, 2]])
        self.assertEqual(buffer.size(), 1)

    # def test_xxxx(self):
    #     buffer = RingBufferMock(100)
    #     for i in range(0, 60):
    #         buffer.put(i)
    #     ret_list = buffer.get_nowait(40)
    #     print("xxx:", ret_list)
    #
    #     for i in range(60, 120):
    #         buffer.put(i)
    #     ret_list = buffer.get_nowait(40)
    #     print("xxx:", ret_list)
