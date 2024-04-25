#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#

from analyzerlib.channel import AbstractChannel
from analyzerlib.logger import Logger


# pylint: disable=C0103


class HostConnector:
    def __init__(self, channel: AbstractChannel, logger: Logger):
        self.channel: AbstractChannel = channel  # communication medium
        self.logger: Logger = logger

    def receive_message(self):
        command = self.channel.read_int(1)

        if command is None:
            # no incoming message
            return None

        # UNKNOWN_REQUEST_RSPNS
        ## parameters:
        ##    message: byte
        if command == 0x01:
            message = self.channel.read_int(1)
            return [command, message]

        # SET_KBD_INTR_RSPNS
        if command == 0x02:
            # no fields
            return [command]

        # INTERNAL_TEMP_RSPNS
        ## parameters:
        ##    temperature: int16
        if command == 0x03:
            temperature = self.channel.read_int(2)
            return [command, temperature]

        # MEASURE_RSPNS
        ## parameters:
        ##    data_list: bytearray
        if command == 0x04:
            data_size = self.channel.read_int(2)
            data_list = self.channel.read_bytes(data_size)
            return [command, data_list]

        # CHANNEL_STATE_RSPNS
        ## parameters:
        ##    channel_enable_flags: byte
        if command == 0x05:
            channel_enable_flags = self.channel.read_int(1)
            return [command, channel_enable_flags]

        # TEST_BYTES_RSPNS
        ## parameters:
        ##    data_bytes: bytearray
        if command == 0x06:
            data_size = self.channel.read_int(2)
            data_bytes = self.channel.read_bytes(data_size)
            return [command, data_bytes]

        # TEST_TEXT_RSPNS
        ## parameters:
        ##    content: str
        if command == 0x07:
            content = self.channel.read_text()
            return [command, content]

        if self.logger:
            self.logger.error(f"unknown message: '{command}' '{chr(command)}'")
        return [None, command]

    ## ============= send methods ===============

    ## send 'SET_KBD_INTR_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_SET_KBD_INTR_RQST(self, new_state):
        self.channel.write_int(0x01, 1)  # "SET_KBD_INTR_RQST"
        self.channel.write_int(new_state, 1)

    ## send 'SET_INTERNAL_LED_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_SET_INTERNAL_LED_RQST(self, new_state):
        self.channel.write_int(0x02, 1)  # "SET_INTERNAL_LED_RQST"
        self.channel.write_int(new_state, 1)

    ## send 'INTERNAL_TEMP_RQST' message
    def send_INTERNAL_TEMP_RQST(self):
        self.channel.write_int(0x03, 1)  # "INTERNAL_TEMP_RQST"

    ## send 'MEASURE_RQST' message
    ## parameters:
    ##    data_size: int16
    ##    transfer_num: int16
    def send_MEASURE_RQST(self, data_size, transfer_num):
        self.channel.write_int(0x04, 1)  # "MEASURE_RQST"
        self.channel.write_int(data_size, 2)
        self.channel.write_int(transfer_num, 2)

    ## send 'CHANNEL_STATE_RQST' message
    def send_CHANNEL_STATE_RQST(self):
        self.channel.write_int(0x05, 1)  # "CHANNEL_STATE_RQST"

    ## send 'TEST_BYTES_RQST' message
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int16
    def send_TEST_BYTES_RQST(self, data_bytes, transfer_num):
        self.channel.write_int(0x06, 1)  # "TEST_BYTES_RQST"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)
        self.channel.write_int(transfer_num, 2)

    ## send 'TEST_TEXT_RQST' message
    ## parameters:
    ##    content: str
    ##    transfer_num: int16
    def send_TEST_TEXT_RQST(self, content, transfer_num):
        self.channel.write_int(0x07, 1)  # "TEST_TEXT_RQST"
        self.channel.write_text(content)
        self.channel.write_int(transfer_num, 2)
