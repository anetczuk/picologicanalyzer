#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import time
import array


class LockMock:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class RingBuffer:
    def __init__(self, capacity, lock=None, init_value=None):
        if lock is None:
            lock = LockMock()
        self.data = [init_value] * capacity
        self.capacity = capacity
        self.index_put = capacity - 1  # index of last 'put' operation
        self.index_get = capacity - 1  # index of last 'get' operation
        self.curr_size = 0
        self.overflow_counter = 0
        self.ring_lock = lock

    def is_empty(self):
        with self.ring_lock:
            return self.curr_size == 0

    def size(self):
        with self.ring_lock:
            return self.curr_size

    def put(self, value):
        with self.ring_lock:
            if self.curr_size < self.capacity:
                self.curr_size += 1
            else:
                if self.index_get == self.index_put:
                    # data overflow
                    self.overflow_counter += 1
                    self.index_get = (self.index_get + 1) % self.capacity
            self.index_put = (self.index_put + 1) % self.capacity
            self.data[self.index_put] = value

    def next(self):
        with self.ring_lock:
            index_next = (self.index_get + 1) % self.capacity
            return self.data[index_next]

    def get(self):
        with self.ring_lock:
            return self._get()

    def _get(self):
        if self.curr_size > 0:
            self.curr_size -= 1
        self.index_get = (self.index_get + 1) % self.capacity
        return self.data[self.index_get]

    def get_nowait(self, items_num):
        with self.ring_lock:
            items = min(items_num, self.curr_size)
            ret_list = []
            for _ in range(0, items):
                ret_list.append(self._get())
            return ret_list

    def get_wait(self, items_num):
        ret_list = []
        items_needed = items_num
        while items_needed > 0:
            curr_data = self.get_nowait(items_needed)
            ret_list.extend(curr_data)
            items_needed -= len(curr_data)
        return ret_list


# ==============================================================


class TimeMeasureContainer:
    def __init__(self):
        self.measure_data = bytearray()

    def append(self, timestamp, value):
        raise NotImplementedError()


class TimeValueRingBuffer:
    def __init__(self, capacity):
        # # access speed to list of pairs same as for two arrays
        # self.data = [None] * capacity
        # for i in range(0, capacity):
        #     self.data[i] = [0, 0]

        self.timestamp_data = array.array("L", (0 for _ in range(capacity)))
        self.value_data = array.array("B", (0 for _ in range(capacity)))
        self.capacity = capacity
        self.index_put = capacity - 1  # index of last 'put' operation
        self.index_get = capacity - 1  # index of last 'get' operation

    def set_capacity(self, capacity):
        if capacity == self.capacity:
            return
        if capacity > self.capacity:
            self.timestamp_data = array.array("L", (0 for _ in range(capacity)))
            self.value_data = array.array("B", (0 for _ in range(capacity)))
            self.capacity = capacity
            self.index_put = capacity - 1  # index of last 'put' operation
            self.index_get = capacity - 1  # index of last 'get' operation
        else:
            self.capacity = capacity
            self.index_put = capacity - 1  # index of last 'put' operation
            self.index_get = capacity - 1  # index of last 'get' operation
            self.timestamp_data = array.array("L", (0 for _ in range(capacity)))
            self.value_data = array.array("B", (0 for _ in range(capacity)))

    def is_empty(self):
        return self.index_put == self.index_get

    def size(self):
        return (self.index_put + self.capacity - self.index_get) % self.capacity
        # return self.curr_size

    # calling method takes ~30 us
    def put(self, timestamp, value):
        # if and add takes ~15 us
        # # if is faster than "min()"
        # if self.curr_size < self.capacity:
        #     self.curr_size += 1

        # modulo is slightly faster than if
        next_index_put = (self.index_put + 1) % self.capacity
        self.timestamp_data[next_index_put] = timestamp
        self.value_data[next_index_put] = value  # ~5 us slower than writing to single variable
        if next_index_put == self.index_get:
            self.index_get = (self.index_get + 1) % self.capacity
        self.index_put = next_index_put

        # item = self.data[self.index_put]
        # item[0] = timestamp
        # item[1] = value

    def put_pin(self, pin):
        # modulo is slightly faster than if
        next_index_put = (self.index_put + 1) % self.capacity  # local index 5 us faster than using object's member
        self.timestamp_data[next_index_put] = time.ticks_us()  # pylint: disable=E1101
        # ~5 us slower than writing to single variable
        self.value_data[next_index_put] = pin.value()  # ~23us
        if next_index_put == self.index_get:
            self.index_get = (self.index_get + 1) % self.capacity
        self.index_put = next_index_put

    # for tests only
    def next(self):
        index_next = (self.index_get + 1) % self.capacity
        return [self.timestamp_data[index_next], self.value_data[index_next]]
        # return self.data[index_next]

    def get(self):
        return self._get()

    def _get(self):
        if self.index_get == self.index_put:
            # empty buffer
            return None
        index_get = (self.index_get + 1) % self.capacity
        self.index_get = index_get
        return [self.timestamp_data[self.index_get], self.value_data[self.index_get]]
        # return self.data[self.index_get]

    def _get_items(self, items):
        ret_list = [None] * items
        for i in range(0, items):
            self.index_get = (self.index_get + 1) % self.capacity
            ret_list[i] = [self.timestamp_data[self.index_get], self.value_data[self.index_get]]  # append pair
            # timestamp = self.timestamp_data[self.index_get]
            # value = self.value_data[self.index_get]
            # buffer.extend(timestamp.to_bytes(3, "big"))
            # buffer.append(value)
        # return buffer
        return ret_list
        # return self.data[self.index_get]

    def _get_items_buffer(self, items, measure_buffer):
        for _ in range(0, items):
            self.index_get = (self.index_get + 1) % self.capacity
            timestamp = self.timestamp_data[self.index_get]
            value = self.value_data[self.index_get]
            measure_buffer.extend(timestamp.to_bytes(3, "big"))
            measure_buffer.append(value)
            # measure_buffer.append(timestamp, value)

    def get_nowait(self, items_num):
        items = min(items_num, self.size())
        if items < 1:
            return []
        return self._get_items(items)

    def get_nowait_buffer(self, items_num, measure_buffer):
        items = min(items_num, self.size())
        if items > 0:
            self._get_items_buffer(items, measure_buffer)

    def get_wait(self, items_num):
        ret_list = []
        items_needed = items_num
        while items_needed > 0:
            curr_data = self.get_nowait(items_needed)
            ret_list.extend(curr_data)
            items_needed -= len(curr_data)
        return ret_list
