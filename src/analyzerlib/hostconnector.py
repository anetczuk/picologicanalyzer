#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#

from analyzerlib.channel import AbstractChannel


# pylint: disable=C0103


class HostConnector:
    def __init__(self, channel: AbstractChannel):
        self.channel: AbstractChannel = channel  # communication medium

        # under MicroPython lookup dict is significantly faster than if-else chain
        self.lookup_dict = {
                            0x01: self._handle_UNKNOWN_REQUEST_RSPNS,  # UNKNOWN_REQUEST_RSPNS
                            0x02: self._handle_ACKNOWLEDGE_RSPNS,  # ACKNOWLEDGE_RSPNS
                            0x04: self._handle_CURRENT_TIME_MS_RSPNS,  # CURRENT_TIME_MS_RSPNS
                            0x05: self._handle_CURRENT_TIME_US_RSPNS,  # CURRENT_TIME_US_RSPNS
                            0x06: self._handle_CURRENT_TIME_CPU_RSPNS,  # CURRENT_TIME_CPU_RSPNS
                            0x07: self._handle_INTERNAL_TEMP_RSPNS,  # INTERNAL_TEMP_RSPNS
                            0x08: self._handle_CHANNEL_STATE_RSPNS,  # CHANNEL_STATE_RSPNS
                            0x09: self._handle_MEASURED_NO_RSPNS,  # MEASURED_NO_RSPNS
                            0x0a: self._handle_MEASURE_RSPNS,  # MEASURE_RSPNS
                            0x0b: self._handle_MEASURE_TIME_RSPNS,  # MEASURE_TIME_RSPNS
                            0x0c: self._handle_TEST_BYTES_RSPNS,  # TEST_BYTES_RSPNS
                            0x0d: self._handle_TEST_TEXT_RSPNS,  # TEST_TEXT_RSPNS
                            }

    def wait_message(self):
        while True:
            message = self.receive_message()
            if message is None:
                # no message
                continue
            if message[0] is None:
                # unknown message
                continue
            return message

    def wait_message_type(self, message_type):
        while True:
            message = self.receive_message()
            if message is None:
                # no message
                continue
            if message[0] is not message_type:
                # message type not match
                continue
            return message

    def receive_message(self):
        command = self.channel.read_byte()

        callback = self.lookup_dict.get(command)
        if callback is not None:
            return callback()

        self._handle_unknown_command(command)

        # unknown message
        return [None, command]

    def _handle_unknown_command(self, command):
        # override if needed
        pass

    # UNKNOWN_REQUEST_RSPNS
    ## parameters:
    ##    message: byte
    def _handle_UNKNOWN_REQUEST_RSPNS(self):
        message = self.channel.read_byte()
        return [0x01, message]

    # ACKNOWLEDGE_RSPNS
    ## parameters:
    ##    message: byte
    def _handle_ACKNOWLEDGE_RSPNS(self):
        message = self.channel.read_byte()
        return [0x02, message]

    # CURRENT_TIME_MS_RSPNS
    ## parameters:
    ##    time: int32
    def _handle_CURRENT_TIME_MS_RSPNS(self):
        time = self.channel.read_int(4)
        return [0x04, time]

    # CURRENT_TIME_US_RSPNS
    ## parameters:
    ##    time: int32
    def _handle_CURRENT_TIME_US_RSPNS(self):
        time = self.channel.read_int(4)
        return [0x05, time]

    # CURRENT_TIME_CPU_RSPNS
    ## parameters:
    ##    time: int32
    def _handle_CURRENT_TIME_CPU_RSPNS(self):
        time = self.channel.read_int(4)
        return [0x06, time]

    # INTERNAL_TEMP_RSPNS
    ## parameters:
    ##    temperature: int16
    def _handle_INTERNAL_TEMP_RSPNS(self):
        temperature = self.channel.read_int(2)
        return [0x07, temperature]

    # CHANNEL_STATE_RSPNS
    ## parameters:
    ##    channel_enable_flags: byte
    def _handle_CHANNEL_STATE_RSPNS(self):
        channel_enable_flags = self.channel.read_byte()
        return [0x08, channel_enable_flags]

    # MEASURED_NO_RSPNS
    ## parameters:
    ##    measure_num: int16
    def _handle_MEASURED_NO_RSPNS(self):
        measure_num = self.channel.read_int(2)
        return [0x09, measure_num]

    # MEASURE_RSPNS
    ## parameters:
    ##    measure_bytes: bytearray
    def _handle_MEASURE_RSPNS(self):
        data_size = self.channel.read_int(2)
        measure_bytes = self.channel.read_bytes(data_size)
        return [0x0a, measure_bytes]

    # MEASURE_TIME_RSPNS
    ## parameters:
    ##    measure_bytes: bytearray
    def _handle_MEASURE_TIME_RSPNS(self):
        data_size = self.channel.read_int(2)
        measure_bytes = self.channel.read_bytes(data_size)
        return [0x0b, measure_bytes]

    # TEST_BYTES_RSPNS
    ## parameters:
    ##    data_bytes: bytearray
    def _handle_TEST_BYTES_RSPNS(self):
        data_size = self.channel.read_int(2)
        data_bytes = self.channel.read_bytes(data_size)
        return [0x0c, data_bytes]

    # TEST_TEXT_RSPNS
    ## parameters:
    ##    content: str
    def _handle_TEST_TEXT_RSPNS(self):
        content = self.channel.read_text()
        return [0x0d, content]

    ## ============= send methods ===============

    ## send 'SET_KBD_INTR_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_SET_KBD_INTR_RQST(self, new_state):
        self.channel.write_byte(0x01)  # "SET_KBD_INTR_RQST"
        self.channel.write_byte(new_state)

    ## send 'TERMINATE_RQST' message
    def send_TERMINATE_RQST(self):
        self.channel.write_byte(0x02)  # "TERMINATE_RQST"

    ## send 'SET_INTERNAL_LED_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_SET_INTERNAL_LED_RQST(self, new_state):
        self.channel.write_byte(0x04)  # "SET_INTERNAL_LED_RQST"
        self.channel.write_byte(new_state)

    ## send 'CURRENT_TIME_MS_RQST' message
    def send_CURRENT_TIME_MS_RQST(self):
        self.channel.write_byte(0x05)  # "CURRENT_TIME_MS_RQST"

    ## send 'CURRENT_TIME_US_RQST' message
    def send_CURRENT_TIME_US_RQST(self):
        self.channel.write_byte(0x06)  # "CURRENT_TIME_US_RQST"

    ## send 'CURRENT_TIME_CPU_RQST' message
    def send_CURRENT_TIME_CPU_RQST(self):
        self.channel.write_byte(0x07)  # "CURRENT_TIME_CPU_RQST"

    ## send 'INTERNAL_TEMP_RQST' message
    def send_INTERNAL_TEMP_RQST(self):
        self.channel.write_byte(0x08)  # "INTERNAL_TEMP_RQST"

    ## send 'CHANNEL_STATE_RQST' message
    def send_CHANNEL_STATE_RQST(self):
        self.channel.write_byte(0x09)  # "CHANNEL_STATE_RQST"

    ## send 'SELECT_CHANNELS_RQST' message
    ## parameters:
    ##    channel_enable_flags: byte
    def send_SELECT_CHANNELS_RQST(self, channel_enable_flags):
        self.channel.write_byte(0x0a)  # "SELECT_CHANNELS_RQST"
        self.channel.write_byte(channel_enable_flags)

    ## send 'SET_MEASURE_BUFF_SIZE_RQST' message
    ## parameters:
    ##    buffer_size: int16
    def send_SET_MEASURE_BUFF_SIZE_RQST(self, buffer_size):
        self.channel.write_byte(0x0b)  # "SET_MEASURE_BUFF_SIZE_RQST"
        self.channel.write_int(buffer_size, 2)

    ## send 'MEASURED_NO_RQST' message
    def send_MEASURED_NO_RQST(self):
        self.channel.write_byte(0x0c)  # "MEASURED_NO_RQST"

    ## send 'MEASURE_RQST' message
    ## parameters:
    ##    measure_num: int16
    def send_MEASURE_RQST(self, measure_num):
        self.channel.write_byte(0x0d)  # "MEASURE_RQST"
        self.channel.write_int(measure_num, 2)

    ## send 'MEASURE_TR_RQST' message
    ## parameters:
    ##    measure_num: int16
    ##    transfer_num: int16
    def send_MEASURE_TR_RQST(self, measure_num, transfer_num):
        self.channel.write_byte(0x0e)  # "MEASURE_TR_RQST"
        self.channel.write_int(measure_num, 2)
        self.channel.write_int(transfer_num, 2)

    ## send 'MEASURE_TIME_RQST' message
    ## parameters:
    ##    measure_num: int16
    def send_MEASURE_TIME_RQST(self, measure_num):
        self.channel.write_byte(0x0f)  # "MEASURE_TIME_RQST"
        self.channel.write_int(measure_num, 2)

    ## send 'MEASURE_TIME_TR_RQST' message
    ## parameters:
    ##    measure_num: byte
    ##    transfer_num: byte
    ##    params_multiplier: byte
    def send_MEASURE_TIME_TR_RQST(self, measure_num, transfer_num, params_multiplier):
        self.channel.write_byte(0x10)  # "MEASURE_TIME_TR_RQST"
        self.channel.write_byte(measure_num)
        self.channel.write_byte(transfer_num)
        self.channel.write_byte(params_multiplier)

    ## send 'TEST_TRANSFER_TIME_RQST' message
    ## parameters:
    ##    response_size: int16
    def send_TEST_TRANSFER_TIME_RQST(self, response_size):
        self.channel.write_byte(0x11)  # "TEST_TRANSFER_TIME_RQST"
        self.channel.write_int(response_size, 2)

    ## send 'TEST_MEASURE_TIME_RQST' message
    ## parameters:
    ##    measure_num: int16
    def send_TEST_MEASURE_TIME_RQST(self, measure_num):
        self.channel.write_byte(0x13)  # "TEST_MEASURE_TIME_RQST"
        self.channel.write_int(measure_num, 2)

    ## send 'TEST_BYTES_RQST' message
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int16
    ##    data_multiplier: int16
    def send_TEST_BYTES_RQST(self, data_bytes, transfer_num, data_multiplier):
        self.channel.write_byte(0x14)  # "TEST_BYTES_RQST"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)
        self.channel.write_int(transfer_num, 2)
        self.channel.write_int(data_multiplier, 2)

    ## send 'TEST_TEXT_RQST' message
    ## parameters:
    ##    content: str
    ##    transfer_num: int16
    def send_TEST_TEXT_RQST(self, content, transfer_num):
        self.channel.write_byte(0x15)  # "TEST_TEXT_RQST"
        self.channel.write_text(content)
        self.channel.write_int(transfer_num, 2)
