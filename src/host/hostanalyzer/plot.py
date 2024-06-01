#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import time
import abc
import signal
from queue import Queue
import traceback
from typing import List

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class DataStream(abc.ABC):
    @abc.abstractmethod
    def empty(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError()


class QueueStream(DataStream):
    def __init__(self, data_queue: Queue):
        self.data_queue = data_queue

    def empty(self):
        return self.data_queue.empty()

    def get(self):
        return self.data_queue.get_nowait()


class AnimatedPlot:
    def __init__(self, data_stream: DataStream, plot_items_number=None, plot_x_span=None, interval=200):
        signal.signal(signal.SIGINT, self.handle_interrupt)

        self.data_stream: DataStream = data_stream
        self.plot_items_number = plot_items_number
        self.plot_x_span = plot_x_span

        if self.plot_items_number is None and self.plot_x_span is None:
            self.plot_items_number = 10

        # Enable interactive mode for non-blocking plotting
        # plt.ion()

        # Create figure for plotting
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect("key_press_event", self.handle_close)

        self.ax = self.fig.add_subplot(1, 1, 1)
        self.xs: List[int] = []
        self.ys: List[int] = []

        # Set up plot to call animate() function periodically
        self.ani = FuncAnimation(self.fig, self._draw, interval=interval)
        # self.ani = animation.FuncAnimation(self.fig, self._draw, fargs=(self.xs, self.ys), interval=200)

    # This function is called periodically from FuncAnimation
    def _draw(self, i):  # pylint: disable=W0613
        try:
            if self.data_stream.empty():
                self._redraw_unchanged()
                return

            added_item = self._add_data()

            if not added_item:
                self._redraw_unchanged()
                return

            x_len = len(self.xs)
            if x_len < 1:
                return

            # cut plot array
            if self.plot_items_number is not None:
                self.xs = self.xs[-self.plot_items_number :]
                self.ys = self.ys[-self.plot_items_number :]

            elif self.plot_x_span is not None:
                recent_x = self.xs[-1]
                for i in range(0, x_len - 1):
                    index = x_len - i - 1
                    curr_x = self.xs[index]
                    diff_x = recent_x - curr_x
                    if diff_x > self.plot_x_span:
                        self.xs = self.xs[index :]
                        self.ys = self.ys[index :]

            self._redraw_plot()

        except BaseException as exc:
            # sys.exit(1)
            print("got exception:", exc)

    def _add_data(self) -> bool:
        # Add x and y to lists
        # 'self.data_stream' contains state changes, so to draw square signal plot
        # additional points (with previous value) have to be added
        prev_val = 0
        if self.ys:
            prev_val = self.ys[-1]
        added_item = False
        while not self.data_stream.empty():
            # data_time = dt.datetime.now().strftime('%H:%M:%S.%f')
            queue_list = self.data_stream.get()
            for queue_data in queue_list:
                data_time = queue_data[0]
                data_value = queue_data[1]
                if prev_val != data_value:
                    self.xs.append(data_time)
                    self.ys.append(prev_val)
                prev_val = data_value
                self.xs.append(data_time)
                self.ys.append(data_value)
                added_item = True
        return added_item

    def _redraw_unchanged(self):
        pass

    def _redraw_plot(self):
        # Draw x and y lists
        self.ax.clear()

        self.ax.plot(self.xs, self.ys)

        # Format plot
        # plt.xticks(rotation=45, ha='right')
        # plt.xticks(ticks=[], rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        # plt.title('TMP102 Temperature over Time')
        # plt.ylabel('Temperature (deg C)')

    def show(self):
        plt.show()

    def close(self):
        plt.close("all")
        # plt.close()

    def handle_close(self, evt):
        if evt != "ctrl+c":
            return
        print("closing plot...")
        self.fig.close()
        # plt.close() # close the figure
        # exit() # exit the program, or raise KeyboardInterrupt for interrupt stack

    def handle_interrupt(self, signum, frame):  # pylint: disable=W0613
        self.close()


class AnimatedTimePlot(AnimatedPlot):
    def __init__(self, data_stream: DataStream, plot_items_number=None, plot_time_span=None, interval=200):
        self.data_last_time = None
        super().__init__(data_stream, plot_items_number, plot_time_span, interval)

    def _add_data(self) -> bool:
        # Add x and y to lists
        # 'self.data_stream' contains state changes, so to draw square signal plot
        # additional points (with previous value) have to be added
        prev_val = 0
        if self.ys:
            prev_val = self.ys[-1]
        added_item = False
        while not self.data_stream.empty():
            # data_time = dt.datetime.now().strftime('%H:%M:%S.%f')
            queue_list = self.data_stream.get()
            for queue_data in queue_list:
                data_time = queue_data[0]
                data_value = queue_data[1]
                if prev_val != data_value:
                    self.xs.append(data_time / 1000000)
                    self.ys.append(prev_val)
                prev_val = data_value
                self.xs.append(data_time / 1000000)
                self.ys.append(data_value)
                added_item = True
        return added_item

    def _redraw_unchanged(self):
        self._update_last()
        self._redraw_plot()

    def _update_last(self):
        # repeat last value
        if not self.data_last_time:
            return

        if len(self.xs) > 1:
            if self.ys[-2] != self.ys[-1]:
                # repeat last value
                self.xs.append(self.xs[-1])
                self.ys.append(self.ys[-1])

        curr_time = time.time()
        diff_time = curr_time - self.data_last_time  # in s
        self.data_last_time = curr_time
        self.xs[-1] += diff_time
