#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Checking lookup dict.
#

import time
import utime
import micropython
import machine

import board
from filelogger import FileLogger

from sysstreamchannel import SysStreamChannel
from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensorendpoint import SensorEndpoint
from analyzerlib.message import measuretimemsg


# self.probe = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  # GP21
probe = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # GP21


def keyboard_interrupt(connector, command_data):
    value = command_data[1]
    if value == 0:
        # disable keyboard interrupt (allow binary 0x03 characters instead of Control-C interrupt)
        micropython.kbd_intr(-1)
    else:
        # enable keyboard interrupt (allow connecting to REPL console various tools)
        micropython.kbd_intr(3)
    utime.sleep(0.1)
    connector.send_ACKNOWLEDGE_RSPNS(HostMessage.SET_KBD_INTR_RQST)


def current_time_us(connector, _):
    # def current_time_us(connector, command_data):
    time_value = time.ticks_us()  # pylint: disable=E1101
    connector.send_CURRENT_TIME_US_RSPNS(time_value)


def measure(connector, command_data):
    measure_num = command_data[1]
    send_measures(connector, measure_num)


def measure_tr(connector, command_data):
    measure_num = command_data[1]
    transfer_num = command_data[2]
    for _ in range(0, transfer_num):
        send_measures(connector, measure_num)


def send_measures(connector, measure_num):
    values = bytearray([0] * measure_num)
    for m in range(0, measure_num):
        values[m] = probe.value()  # type: int
    connector.send_MEASURE_RSPNS(values)


def measure_time(connector, command_data):
    measure_num = command_data[1]
    measurements_list = [None] * measure_num
    for m in range(0, measure_num):
        # pylint: disable=E1101
        curr_time = time.ticks_us()  # in microseconds (10^-6)
        curr_state = probe.value()  # type: int
        measurements_list[m] = (curr_time, curr_state)
    measures_data = measuretimemsg.data_to_bytearray(measurements_list)
    connector.send_MEASURE_TIME_RSPNS(measures_data)


def probe_time(connector, command_data):
    probe_num = command_data[1]
    start_time = time.ticks_us()  # pylint: disable=E1101
    for _ in range(0, probe_num):
        probe.value()
    end_time = time.ticks_us()  # pylint: disable=E1101
    diff_time = end_time - start_time

    connector.send_CURRENT_TIME_US_RSPNS(diff_time)


lookup_dict = {
    HostMessage.SET_KBD_INTR_RQST: keyboard_interrupt,
    HostMessage.CURRENT_TIME_US_RQST: current_time_us,
    HostMessage.MEASURE_RQST: measure,
    HostMessage.MEASURE_TR_RQST: measure_tr,
    HostMessage.MEASURE_TIME_RQST: measure_time,
}


# ================================================================


def handle(connector, logger) -> bool:
    command_data = connector.receive_message()

    if command_data is None:
        # no incoming message
        return True

    command = command_data[0]

    if command is None:
        # no incoming message (timeout)
        return None

    # logger.info(f"received command: {HostMessage.get_id_from_value(command)}('{command}')")

    callback = lookup_dict.get(command)
    if callback is not None:
        return callback(connector, command_data)

    if logger:
        # unhandled command
        logger.warn(f"unhandled command: {command_data}")

    board.blink_led(0.01)
    connector.send_UNKNOWN_REQUEST_RSPNS(command)
    return True


def start(logger: FileLogger) -> bool:
    logger: FileLogger = logger
    channel = SysStreamChannel()
    connector = SensorEndpoint(channel)

    while True:
        handle(connector, logger)
