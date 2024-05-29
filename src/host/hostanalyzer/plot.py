#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

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
    def __init__(self, data_stream: DataStream, plot_items_number=10, interval=200):
        signal.signal(signal.SIGINT, self.handle_interrupt)

        self.data_stream: DataStream = data_stream
        self.plot_items_number = plot_items_number

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
            # Draw x and y lists
            self.ax.clear()

            # Add x and y to lists
            # 'self.data_stream' contains state changes, so to draw square signal plot
            # additional points (with previous value) have to be added
            prev_val = 0
            if self.ys:
                prev_val = self.ys[-1]
            while not self.data_stream.empty():
                # data_time = dt.datetime.now().strftime('%H:%M:%S.%f')
                queue_list = self.data_stream.get()
                for queue_data in queue_list:
                    data_time = queue_data[0]
                    data_value = queue_data[1]
                    self.xs.append((data_time - 1) / 1000000)
                    self.ys.append(prev_val)
                    prev_val = data_value
                    self.xs.append(data_time / 1000000)
                    self.ys.append(data_value)

            # cut plot array
            self.xs = self.xs[-self.plot_items_number :]
            self.ys = self.ys[-self.plot_items_number :]

            self.ax.plot(self.xs, self.ys)

            # Format plot
            # plt.xticks(rotation=45, ha='right')
            # plt.xticks(ticks=[], rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            # plt.title('TMP102 Temperature over Time')
            # plt.ylabel('Temperature (deg C)')
        except BaseException as exc:
            # sys.exit(1)
            print("got exception:", exc)
            print(traceback.format_exc())

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
