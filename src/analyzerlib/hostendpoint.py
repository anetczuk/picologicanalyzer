#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

from random import randrange

from analyzerlib.hostmessage import HostMessage
from analyzerlib.sensormessage import SensorMessage
from analyzerlib.hostconnector import HostConnector


class HostEndpoint(HostConnector):
    def send_bytes(self, data_bytes):
        self.channel.write_bytes(data_bytes)

    def receive_bytes(self, length) -> bytes:
        return self.channel.read_bytes(length)

    def send_text(self, content):
        self.channel.write_text(content)

    def receive_text(self):
        return self.channel.read_text()

    # if 'new_state' is False then disable keyboard interrupts (allow value 0x03)
    def set_keyboard_interrupt(self, new_state: bool):
        if new_state:
            print("enabling keyboard interrupt")
            self.send_SET_KBD_INTR_RQST(1)
        else:
            print("disabling keyboard interrupt")
            self.send_SET_KBD_INTR_RQST(0)
        # wait for acknowledge
        while True:
            message = self.wait_message()
            if message[0] != SensorMessage.ACKNOWLEDGE_RSPNS:
                continue
            if message[1] != HostMessage.SET_KBD_INTR_RQST:
                continue
            break

    def receive_measure_time(self):
        command = self.channel.read_byte()
        if command == SensorMessage.MEASURE_TIME_RSPNS:
            data_size = self.channel.read_int(2)
            measure_bytes = self.channel.read_bytes(data_size)
            return [0x0b, measure_bytes]

        callback = self.lookup_dict.get(command)
        if callback is not None:
            return callback()

        if command is None:
            # no incoming message (timeout)
            return None

        # unknown message
        return [None, command]

    # useful in case of receiving invalid message
    def restore_connection(self):
        while True:
            print("clearing buffer")
            while True:
                data = self.receive_bytes(1)
                print("aaa:", data)
                if not data:
                    break
            print("sending test message")
            rand_num = randrange(256)  # nosec
            rand_byte = bytes([rand_num])
            self.send_TEST_BYTES_RQST(rand_byte, 1, 1)
            received = self.receive_message()
            print("xxxx:", rand_byte, received)
            if received[0] != SensorMessage.TEST_BYTES_RSPNS:
                continue
            received_data = received[1]
            if received_data == rand_byte:
                break

    def print_message(self, message):
        if message is None:
            print(f"message: {message}")
            return
        command = message[0]
        if command == SensorMessage.UNKNOWN_REQUEST_RSPNS:
            unknown_command = message[1]            
            message_name = SensorMessage.get_id_from_value(command)
            unknown_name = HostMessage.get_id_from_value(unknown_command)
            print(f"message: {message_name} data: {message} unknown command: {unknown_name}")
        elif command == SensorMessage.ACKNOWLEDGE_RSPNS:
            ack_command = message[1]            
            message_name = SensorMessage.get_id_from_value(command)
            ack_name = HostMessage.get_id_from_value(ack_command)
            print(f"message: {message_name} data: {message} ack command: {ack_name}")
        else:
            message_name = SensorMessage.get_id_from_value(command)
            print(f"message: {message_name} data: {message}")
