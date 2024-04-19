#
# File was automatically generated using protocol generator.
#

from analyzerlib.channel import AbstractChannel


# pylint: disable=C0103


class HostConnector:
    def __init__(self, channel: AbstractChannel):
        self.channel: AbstractChannel = channel  # communication medium

    def receive_message(self):
        command = self.channel.read_int(1)

        if command is None:
            print("unhandled message (None)")
            return [None, None]

        # RESPONSE_DATA
        ## parameters:
        ##    data_list: bytearray
        if command == 0x01:
            data_size = self.channel.read_int(2)
            data_list = self.channel.read_bytes(data_size)
            return [command, data_list]

        # SEND_CH_ENABLE
        ## parameters:
        ##    channel_enable_flags: byte
        if command == 0x02:
            channel_enable_flags = self.channel.read_int(1)
            return [command, channel_enable_flags]

        # TEST_BYTES_RESPONSE
        ## parameters:
        ##    data_bytes: bytearray
        if command == 0x03:
            data_size = self.channel.read_int(2)
            data_bytes = self.channel.read_bytes(data_size)
            return [command, data_bytes]

        # TEST_TEXT_RESPONSE
        ## parameters:
        ##    content: str
        if command == 0x04:
            content = self.channel.read_text()
            return [command, content]

        print(f"unknown message: '{command}'")
        return [None, command]

    ## ============= send methods ===============

    ## send 'REQUEST_DATA' message
    ## parameters:
    ##    data_size: int
    ##    transfer_num: int
    def send_REQUEST_DATA(self, data_size, transfer_num):
        self.channel.write_int(0x01, 1)  # "REQUEST_DATA"
        self.channel.write_int(data_size, 2)
        self.channel.write_int(transfer_num, 2)

    ## send 'GET_CH_ENABLE' message
    def send_GET_CH_ENABLE(self):
        self.channel.write_int(0x02, 1)  # "GET_CH_ENABLE"

    ## send 'TEST_BYTES_REQUEST' message
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int
    def send_TEST_BYTES_REQUEST(self, data_bytes, transfer_num):
        self.channel.write_int(0x03, 1)  # "TEST_BYTES_REQUEST"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)
        self.channel.write_int(transfer_num, 2)

    ## send 'TEST_TEXT_REQUEST' message
    ## parameters:
    ##    content: str
    ##    transfer_num: int
    def send_TEST_TEXT_REQUEST(self, content, transfer_num):
        self.channel.write_int(0x04, 1)  # "TEST_TEXT_REQUEST"
        self.channel.write_text(content)
        self.channel.write_int(transfer_num, 2)
