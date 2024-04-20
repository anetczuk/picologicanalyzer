#
# File was automatically generated using protocol generator.
#

from analyzerlib.channel import AbstractChannel


# pylint: disable=C0103


class SensorConnector:
    def __init__(self, channel: AbstractChannel):
        self.channel: AbstractChannel = channel  # communication medium

    def receive_message(self):
        command = self.channel.read_int(1)

        if command is None:
            print("unhandled message (None)")
            return [None, None]

        # MEASURE_RQST
        ## parameters:
        ##    data_size: int
        ##    transfer_num: int
        if command == 0x01:
            data_size = self.channel.read_int(2)
            transfer_num = self.channel.read_int(2)
            return [command, data_size, transfer_num]

        # CH_STATE_RQST
        if command == 0x02:
            # no params
            return [command]

        # INTERNAL_TEMP_RQST
        if command == 0x03:
            # no params
            return [command]

        # TEST_BYTES_RQST
        ## parameters:
        ##    data_bytes: bytearray
        ##    transfer_num: int
        if command == 0x04:
            data_size = self.channel.read_int(2)
            data_bytes = self.channel.read_bytes(data_size)
            transfer_num = self.channel.read_int(2)
            return [command, data_bytes, transfer_num]

        # TEST_TEXT_RQST
        ## parameters:
        ##    content: str
        ##    transfer_num: int
        if command == 0x05:
            content = self.channel.read_text()
            transfer_num = self.channel.read_int(2)
            return [command, content, transfer_num]

        print(f"unknown message: '{command}'")
        return [None, command]

    ## ============= send methods ===============

    ## send 'MEASURE_RSPNS' message
    ## parameters:
    ##    data_list: bytearray
    def send_MEASURE_RSPNS(self, data_list):
        self.channel.write_int(0x01, 1)  # "MEASURE_RSPNS"
        self.channel.write_int(len(data_list), 2)
        self.channel.write_bytes(data_list)

    ## send 'CH_STATE_RSPNS' message
    ## parameters:
    ##    channel_enable_flags: byte
    def send_CH_STATE_RSPNS(self, channel_enable_flags):
        self.channel.write_int(0x02, 1)  # "CH_STATE_RSPNS"
        self.channel.write_int(channel_enable_flags, 1)

    ## send 'INTERNAL_TEMP_RSPNS' message
    ## parameters:
    ##    channel_enable_flags: byte
    def send_INTERNAL_TEMP_RSPNS(self, channel_enable_flags):
        self.channel.write_int(0x03, 1)  # "INTERNAL_TEMP_RSPNS"
        self.channel.write_int(channel_enable_flags, 1)

    ## send 'TEST_BYTES_RSPNS' message
    ## parameters:
    ##    data_bytes: bytearray
    def send_TEST_BYTES_RSPNS(self, data_bytes):
        self.channel.write_int(0x04, 1)  # "TEST_BYTES_RSPNS"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)

    ## send 'TEST_TEXT_RSPNS' message
    ## parameters:
    ##    content: str
    def send_TEST_TEXT_RSPNS(self, content):
        self.channel.write_int(0x05, 1)  # "TEST_TEXT_RSPNS"
        self.channel.write_text(content)
