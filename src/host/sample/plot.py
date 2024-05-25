#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Plot example.
#

try:
    ## following import success only when file is directly executed from command line
    ## otherwise will throw exception when executing as parameter for "python -m"
    # pylint: disable=W0611
    import __init__
except ImportError:
    ## when import fails then it means that the script was executed indirectly
    ## in this case __init__ is already loaded
    pass

import sys
import time
from random import randrange

from queue import Queue
from threading import Thread

from hostanalyzer.plot import AnimatedPlot, QueueStream


class Producer:
    def __init__(self):  # noqa
        self.data_queue: Queue = Queue()
        self.running = True
        self.sleep_time = 0.1

    def run(self):
        counter = -1
        while self.running:
            counter += 1
            value = randrange(0, 2)  # nosec
            # value = randrange(0, 100)
            # print("adding value:", value)
            self.data_queue.put_nowait([(counter, value)])
            time.sleep(self.sleep_time)

    def stop(self):
        self.running = False


def main():
    device = Producer()
    device.sleep_time = 0.01

    thread = Thread(target=device.run)
    thread.start()

    data_stream = QueueStream(device.data_queue)
    aplot = AnimatedPlot(data_stream, interval=5)
    aplot.plot_items_number = 300
    aplot.show()

    print("plot closed")

    device.stop()
    thread.join()

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
