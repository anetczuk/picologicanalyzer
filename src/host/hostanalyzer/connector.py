#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import time
from queue import Queue

from multiprocessing.connection import Connection

import serial

from analyzerlib.hostendpoint import HostEndpoint
from analyzerlib.sensormessage import SensorMessage
from analyzerlib.hostmessage import HostMessage
from analyzerlib.message import measuremsg, measuretimemsg
from analyzerlib.channel import AbstractChannel
from hostanalyzer.printlogger import PrintLogger
from hostanalyzer.serialchannel import SerialChannel


class Connector:
    # connection - inter process connection
    def __init__(self, channel: AbstractChannel, connection: Connection):
        self.logger: PrintLogger = PrintLogger()
        self.channel: AbstractChannel = channel
        self.connector = HostEndpoint(self.channel)

        # self.data_queue: Queue = Queue()
        self.data_connection: Connection = connection
        # self.recent_data = (0, 0)
        self.data_counter = 0
        self.running = True

    def stop(self):
        self.logger.info("device thread stop request")
        self.running = False
        self.data_connection.close()  # close process connection

    def run(self):
        # disable keyboard interrupts (allow value 0x03)
        self.logger.info("starting runner")
        self.logger.info("disabling Pico keyboard interrupt")
        self.connector.send_SET_KBD_INTR_RQST(0)
        self.handle_message()

        self.connector.send_INTERNAL_TEMP_RQST()
        message = self.wait_message()
        self.connector.print_message(message)

        # self.connector.send_SET_INTERNAL_LED_RQST(1)

        self.connector.send_SELECT_CHANNELS_RQST(0x01)
        message = self.wait_message()
        self.connector.print_message(message)

        self.connector.send_MEASURED_NO_RQST()
        message = self.wait_message_type( SensorMessage.MEASURED_NO_RSPNS )
        self.connector.print_message(message)

        try:
            measurements = 10
            transfer_num = 10
            multiplier = 10

            while self.running:
                start_time = time.time()

                received_measurements = self.request_measure_time_tr(measurements, transfer_num, multiplier)
                if received_measurements < 1:
                    # data not received
                    continue

                diff_time = time.time() - start_time
                transfer_time = diff_time / received_measurements
                freq = 1.0 / transfer_time
                print(f"received: {received_measurements} single measure time: {transfer_time * 1000} ms freq: {freq} Hz")

                # self.connector.send_MEASURED_NO_RQST()
                # message = self.wait_message_type( SensorMessage.MEASURED_NO_RSPNS )
                # self.connector.print_message(message)

        except KeyboardInterrupt:
            self.logger.info("received keyboard interrupt")
            # raise

        except BaseException as exc:
            self.logger.exception(exc)

        finally:
            self.logger.info("closing connection")
            time.sleep(0.25)  # wait for all incoming data
            self.clear_buffers()
            self.enable_keyb_interrupt()

    def request_measure(self, measurements, transfer_num):
        self.connector.send_MEASURE_TR_RQST(measurements, transfer_num)
        for _ in range(0, transfer_num):
            # self.connector.send_MEASURE_RQST(measurements)
            message = self.handle_message()

            if message is not None and message[0] == SensorMessage.MEASURE_RSPNS:
                measure_array = message[1]
                measures_list = measuremsg.bytearray_to_data(measure_array)
                for measure in measures_list:
                    self.data_counter += 1
                    self._send_data((self.data_counter, measure))

    def request_measure_time(self, measurements, transfer_num) -> int:
        #for _ in range(0, transfer_num):
        received_measurements = 0
        while transfer_num > 0:
            self.connector.send_MEASURE_TIME_RQST(measurements)
            # self.connector.send_TEST_BYTES_RQST(b"\x01", 1, measurements)

            # message = self.handle_message()
            message = self.connector.receive_message()
            # message = self.connector.receive_measure_time()
            # self.connector.print_message(message)

            if message is None:
                self.logger.info(f"invalid message - received None")
                continue

            transfer_num -= 1

            if message[0] == SensorMessage.MEASURE_TIME_RSPNS:
                measure_array = message[1]
                measuretime_list = measuretimemsg.bytearray_to_data(measure_array)
                
                # TODO: uncomment
                # self._send_data(measuretime_list)
                
                measures_size = len(measuretime_list)
                # measures_size = int(len(measure_array) / 4)

                received_measurements += measures_size
                if measures_size == measurements:
                    print("possible loss of data:", measurements, measures_size)

            elif message[0] == SensorMessage.TEST_BYTES_RSPNS:
                received_measurements += measurements / 4

            else:
                command = message[0]
                command_name = SensorMessage.get_id_from_value(command)
                self.logger.info(f"invalid message '{command_name}' - expected measurement")
        return received_measurements

    def request_measure_time_tr(self, measurements, transfer_num, multiplier) -> int:
        #for _ in range(0, transfer_num):
        received_measurements = 0

        measuremest_multiplied = measurements * multiplier
        transfers_multiplied = transfer_num * multiplier

        self.connector.send_MEASURE_TIME_TR_RQST(measurements, transfer_num, multiplier)

        while transfers_multiplied > 0:
            transfers_multiplied -= 1

            # self.connector.send_TEST_BYTES_RQST(b"\x01", 1, measurements)

            message = self.connector.receive_message()
            # message = self.handle_message()
            # message = self.connector.receive_measure_time()
            # self.connector.print_message(message)

            if message[0] == SensorMessage.MEASURE_TIME_RSPNS:
                measure_array = message[1]
                measuretime_list = measuretimemsg.bytearray_to_data(measure_array)
                
                self._send_data(measuretime_list)
                
                measures_size = len(measuretime_list)
                # measures_size = int(len(measure_array) / 4)

                if received_measurements < 1:
                    if measures_size == measuremest_multiplied:
                        print("possible loss of data:", measuremest_multiplied, measures_size)
                received_measurements += measures_size

            elif message[0] == SensorMessage.TEST_BYTES_RSPNS:
                received_measurements += measuremest_multiplied / 4

            else:
                command = message[0]
                command_name = SensorMessage.get_id_from_value(command)
                self.logger.info(f"invalid message '{command_name}' - expected measurement")

        return received_measurements

    def _send_data(self, data):
        try:
            # if self.recent_data[1] == data[1]:
            #     self.recent_data = data
            #     return
            #
            # self.data_connection.send(self.recent_data)
            # self.recent_data = data

            self.data_connection.send(data)

        except OSError:
            return

    def enable_keyb_interrupt(self):
        # enable keyboard interrupt
        self.logger.info("enabling Pico keyboard interrupt")
        # self.handle_message()
        self.connector.send_SET_KBD_INTR_RQST(1)
        while True:
            message = self.handle_message()
            if message is None:
                self.print_message(message)
                break
            command = message[0]
            if command is SensorMessage.ACKNOWLEDGE_RSPNS:
                ack_command = message[1]
                if ack_command == HostMessage.SET_KBD_INTR_RQST:
                    break

    def read_pico_temperature(self):
        self.connector.send_INTERNAL_TEMP_RQST()
        message = self.connector.receive_message()
        temperature = message[1]
        if temperature is None:
            print("invalid data:", message)
            return
        temperature = temperature / 100.0
        print("current Pico temperature:", temperature)

    def wait_message(self):
        return self.connector.wait_message()

    def wait_message_type(self, message_type):
        return self.connector.wait_message_type(message_type)

    def handle_message(self) -> list:
        # return self.connector.receive_message()

        command_data = self.connector.receive_message()
        
        if command_data is None:
            # no incoming message
            return None
        
        command = command_data[0]

        # this if-chain is slightly faster than overriding methods of HostEndpoint class
        if command is None:
            # unknown command
            # logger.info(f"unknown command: {command_data}")
            return command_data
        
        elif command == SensorMessage.ACKNOWLEDGE_RSPNS:
            ack_command = command_data[1]
            if ack_command == HostMessage.SET_KBD_INTR_RQST:
                self.logger.info("keyboard interrupt acknowledge")
        
        elif command == SensorMessage.UNKNOWN_REQUEST_RSPNS:
            message_value = command_data[1]
            message_id = HostMessage.get_id_from_value(message_value)
            self.logger.info(f"Pico does not know how to handle message '{message_value}'({message_id})")
        
        elif command == SensorMessage.CHANNEL_STATE_RSPNS:
            channel_flags = command_data[1]
            self.logger.info(f"channels state: {channel_flags:>08b}")
        
        # elif command == SensorMessage.MEASURED_NO_RSPNS:
        #     return command_data
        #
        # elif command == SensorMessage.MEASURE_RSPNS:
        #     # self.logger.info(f"received measurements: {command_data[1]}")
        #     return command_data
        #
        # elif command == SensorMessage.MEASURE_TIME_RSPNS:
        #     # self.logger.info(f"received measurements: {command_data[1]}")
        #     return command_data
        
        elif command == SensorMessage.INTERNAL_TEMP_RSPNS:
            temperature = command_data[1] / 100.0
            self.logger.info(f"Pico internal temperature: {temperature}")
        
        # else:
        #     # unhandled command
        #     command_id = SensorMessage.get_id_from_value(command)
        #     self.logger.warn(f"unhandled command: {command_data}, '{command_id}'")
        
        return command_data

    def handle_connection(self):
        while True:
            self.handle_message()

    def clear_buffers(self):
        self.channel.reset_input_buffer()
        self.channel.reset_output_buffer()
        while True:
            command_data = self.connector.receive_message()
            if command_data is None:
                # no incoming message
                break

    def print_message(self, message):
        self.connector.print_message(message)


class SerialConnector(Connector):
    def __init__(self, medium: serial.Serial, connection: Connection):
        channel: SerialChannel = SerialChannel(medium)
        super().__init__(channel, connection)    
