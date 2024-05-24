#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import time
import multiprocessing
from threading import Thread

# import signal
import serial

from hostanalyzer.plot import AnimatedPlot, DataStream
from hostanalyzer.connector import SerialConnector


# signal.signal(signal.SIGINT, signal.SIG_DFL)


class EventWatchdog:
    def __init__(self, name, event, callback):
        self.name = name
        self.event = event
        self.callback = callback
        self.running = True
        self.thread = None

    def watch(self):
        self.thread = Thread(target=self._watch)
        self.thread.start()

    def stop_watchdog(self):
        self.running = False

    def join(self):
        self.thread.join()

    def _watch(self):
        while self.running:
            if self.event.is_set():
                # print(f"{self.name}: detected event")
                self.callback()
                break
            time.sleep(0.5)


class ConnectionStream(DataStream):
    def __init__(self, connection):
        self.data_connection = connection

    def empty(self):
        return not self.data_connection.poll()

    def get(self):
        return self.data_connection.recv()


def device_runner(connection, device_close_request, device_close_event):
    # open a serial connection
    with serial.Serial(
        port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1
    ) as medium:
        medium.flush()
        medium.reset_input_buffer()
        device = SerialConnector(medium, connection)

        # watch for device close requests
        close_callback = device.stop
        watchdog = EventWatchdog("device close request watchdog", device_close_request, close_callback)
        watchdog.watch()

        try:
            device.run()

        finally:
            device.logger.info("device receiver closed")
            device_close_event.set()


def main():
    # signal.signal(signal.SIGINT, signal.SIG_DFL)

    parent_conn, child_conn = multiprocessing.Pipe()

    device_close_request = multiprocessing.Event()
    device_close_event = multiprocessing.Event()

    device_process = multiprocessing.Process(
        target=device_runner, args=(parent_conn, device_close_request, device_close_event)
    )
    device_process.start()

    # plot have to be in main thread
    data_stream = ConnectionStream(child_conn)

    aplot = AnimatedPlot(data_stream, plot_items_number=600, interval=150)

    # watch for device termination
    close_callback = aplot.close
    watchdog = EventWatchdog("device close watchdog", device_close_event, close_callback)
    watchdog.watch()

    aplot.show()
    print("plot closed")

    device_close_request.set()
    device_process.join()

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
