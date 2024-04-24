#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#

from analyzerlib.channel import AbstractChannel
from analyzerlib.logger import Logger


# pylint: disable=C0103


class SensorConnector:
    def __init__(self, channel: AbstractChannel, logger: Logger):
        self.channel: AbstractChannel = channel  # communication medium
        self.logger: Logger = logger

    def receive_message(self):
        command = self.channel.read_int(1)

        if command is None:
            # no incoming message
            return None

        # SET_KBD_INTR_RQST
        ## parameters:
        ##    new_state: bool
        if command == 0x01:
            new_state = self.channel.read_int(1)
            return [command, new_state]

        # SET_INTERNAL_LED_RQST
        ## parameters:
        ##    new_state: bool
        if command == 0x02:
            new_state = self.channel.read_int(1)
            return [command, new_state]

        # INTERNAL_TEMP_RQST
        if command == 0x03:
            # no fields
            return [command]

        # MEASURE_RQST
        ## parameters:
        ##    data_size: int16
        ##    transfer_num: int16
        if command == 0x04:
            data_size = self.channel.read_int(2)
            transfer_num = self.channel.read_int(2)
            return [command, data_size, transfer_num]

        # CHANNEL_STATE_RQST
        if command == 0x05:
            # no fields
            return [command]

        # TEST_BYTES_RQST
        ## parameters:
        ##    data_bytes: bytearray
        ##    transfer_num: int16
        if command == 0x06:
            data_size = self.channel.read_int(2)
            data_bytes = self.channel.read_bytes(data_size)
            transfer_num = self.channel.read_int(2)
            return [command, data_bytes, transfer_num]

        # TEST_TEXT_RQST
        ## parameters:
        ##    content: str
        ##    transfer_num: int16
        if command == 0x07:
            content = self.channel.read_text()
            transfer_num = self.channel.read_int(2)
            return [command, content, transfer_num]

        if self.logger:
            self.logger.error(f"unknown message: '{command}'")
        return [None, command]

    ## ============= send methods ===============

    ## send 'UNKNOWN_REQUEST_RSPNS' message
    ## parameters:
    ##    message: byte
    def send_UNKNOWN_REQUEST_RSPNS(self, message):
        self.channel.write_int(0x01, 1)  # "UNKNOWN_REQUEST_RSPNS"
        self.channel.write_int(message, 1)

    ## send 'INTERNAL_TEMP_RSPNS' message
    ## parameters:
    ##    temperature: int16
    def send_INTERNAL_TEMP_RSPNS(self, temperature):
        self.channel.write_int(0x02, 1)  # "INTERNAL_TEMP_RSPNS"
        self.channel.write_int(temperature, 2)

    ## send 'MEASURE_RSPNS' message
    ## parameters:
    ##    data_list: bytearray
    def send_MEASURE_RSPNS(self, data_list):
        self.channel.write_int(0x03, 1)  # "MEASURE_RSPNS"
        self.channel.write_int(len(data_list), 2)
        self.channel.write_bytes(data_list)

    ## send 'CHANNEL_STATE_RSPNS' message
    ## parameters:
    ##    channel_enable_flags: byte
    def send_CHANNEL_STATE_RSPNS(self, channel_enable_flags):
        self.channel.write_int(0x04, 1)  # "CHANNEL_STATE_RSPNS"
        self.channel.write_int(channel_enable_flags, 1)

    ## send 'TEST_BYTES_RSPNS' message
    ## parameters:
    ##    data_bytes: bytearray
    def send_TEST_BYTES_RSPNS(self, data_bytes):
        self.channel.write_int(0x05, 1)  # "TEST_BYTES_RSPNS"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)

    ## send 'TEST_TEXT_RSPNS' message
    ## parameters:
    ##    content: str
    def send_TEST_TEXT_RSPNS(self, content):
        self.channel.write_int(0x06, 1)  # "TEST_TEXT_RSPNS"
        self.channel.write_text(content)
