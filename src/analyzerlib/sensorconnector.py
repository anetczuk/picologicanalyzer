#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#

from analyzerlib.channel import AbstractChannel


# pylint: disable=C0103


class SensorConnector:
    def __init__(self, channel: AbstractChannel):
        self.channel: AbstractChannel = channel  # communication medium

        # under MicroPython lookup dict is significantly faster than if-else chain
        self.lookup_dict = {
            0x01: self._handle_set_kbd_intr_rqst,  # SET_KBD_INTR_RQST
            0x02: self._handle_terminate_rqst,  # TERMINATE_RQST
            0x04: self._handle_set_internal_led_rqst,  # SET_INTERNAL_LED_RQST
            0x05: self._handle_current_time_ms_rqst,  # CURRENT_TIME_MS_RQST
            0x06: self._handle_current_time_us_rqst,  # CURRENT_TIME_US_RQST
            0x07: self._handle_current_time_cpu_rqst,  # CURRENT_TIME_CPU_RQST
            0x08: self._handle_internal_temp_rqst,  # INTERNAL_TEMP_RQST
            0x09: self._handle_channel_state_rqst,  # CHANNEL_STATE_RQST
            0x0A: self._handle_select_channels_rqst,  # SELECT_CHANNELS_RQST
            0x0B: self._handle_set_measure_buff_size_rqst,  # SET_MEASURE_BUFF_SIZE_RQST
            0x0C: self._handle_measured_no_rqst,  # MEASURED_NO_RQST
            0x0D: self._handle_measure_rqst,  # MEASURE_RQST
            0x0E: self._handle_measure_tr_rqst,  # MEASURE_TR_RQST
            0x0F: self._handle_measure_time_rqst,  # MEASURE_TIME_RQST
            0x10: self._handle_measure_time_tr_rqst,  # MEASURE_TIME_TR_RQST
            0x11: self._handle_test_transfer_time_rqst,  # TEST_TRANSFER_TIME_RQST
            0x12: self._handle_test_measure_time_rqst,  # TEST_MEASURE_TIME_RQST
            0x13: self._handle_test_bytes_rqst,  # TEST_BYTES_RQST
            0x14: self._handle_test_text_rqst,  # TEST_TEXT_RQST
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

    # SET_KBD_INTR_RQST
    ## parameters:
    ##    new_state: bool
    def _handle_set_kbd_intr_rqst(self):
        new_state = self.channel.read_byte()
        return [0x01, new_state]

    # TERMINATE_RQST
    def _handle_terminate_rqst(self):
        # no fields
        return [0x02]

    # SET_INTERNAL_LED_RQST
    ## parameters:
    ##    new_state: bool
    def _handle_set_internal_led_rqst(self):
        new_state = self.channel.read_byte()
        return [0x04, new_state]

    # CURRENT_TIME_MS_RQST
    def _handle_current_time_ms_rqst(self):
        # no fields
        return [0x05]

    # CURRENT_TIME_US_RQST
    def _handle_current_time_us_rqst(self):
        # no fields
        return [0x06]

    # CURRENT_TIME_CPU_RQST
    def _handle_current_time_cpu_rqst(self):
        # no fields
        return [0x07]

    # INTERNAL_TEMP_RQST
    def _handle_internal_temp_rqst(self):
        # no fields
        return [0x08]

    # CHANNEL_STATE_RQST
    def _handle_channel_state_rqst(self):
        # no fields
        return [0x09]

    # SELECT_CHANNELS_RQST
    ## parameters:
    ##    channel_enable_flags: byte
    def _handle_select_channels_rqst(self):
        channel_enable_flags = self.channel.read_byte()
        return [0x0A, channel_enable_flags]

    # SET_MEASURE_BUFF_SIZE_RQST
    ## parameters:
    ##    buffer_size: int16
    def _handle_set_measure_buff_size_rqst(self):
        buffer_size = self.channel.read_int(2)
        return [0x0B, buffer_size]

    # MEASURED_NO_RQST
    def _handle_measured_no_rqst(self):
        # no fields
        return [0x0C]

    # MEASURE_RQST
    ## parameters:
    ##    measure_num: int16
    def _handle_measure_rqst(self):
        measure_num = self.channel.read_int(2)
        return [0x0D, measure_num]

    # MEASURE_TR_RQST
    ## parameters:
    ##    measure_num: int16
    ##    transfer_num: int16
    def _handle_measure_tr_rqst(self):
        measure_num = self.channel.read_int(2)
        transfer_num = self.channel.read_int(2)
        return [0x0E, measure_num, transfer_num]

    # MEASURE_TIME_RQST
    ## parameters:
    ##    measure_num: int16
    def _handle_measure_time_rqst(self):
        measure_num = self.channel.read_int(2)
        return [0x0F, measure_num]

    # MEASURE_TIME_TR_RQST
    ## parameters:
    ##    measure_num: byte
    ##    transfer_num: byte
    ##    params_multiplier: byte
    def _handle_measure_time_tr_rqst(self):
        measure_num = self.channel.read_byte()
        transfer_num = self.channel.read_byte()
        params_multiplier = self.channel.read_byte()
        return [0x10, measure_num, transfer_num, params_multiplier]

    # TEST_TRANSFER_TIME_RQST
    ## parameters:
    ##    response_size: int16
    def _handle_test_transfer_time_rqst(self):
        response_size = self.channel.read_int(2)
        return [0x11, response_size]

    # TEST_MEASURE_TIME_RQST
    ## parameters:
    ##    measure_num: int16
    def _handle_test_measure_time_rqst(self):
        measure_num = self.channel.read_int(2)
        return [0x12, measure_num]

    # TEST_BYTES_RQST
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int16
    ##    data_multiplier: int16
    def _handle_test_bytes_rqst(self):
        data_size = self.channel.read_int(2)
        data_bytes = self.channel.read_bytes(data_size)
        transfer_num = self.channel.read_int(2)
        data_multiplier = self.channel.read_int(2)
        return [0x13, data_bytes, transfer_num, data_multiplier]

    # TEST_TEXT_RQST
    ## parameters:
    ##    content: str
    ##    transfer_num: int16
    def _handle_test_text_rqst(self):
        content = self.channel.read_text()
        transfer_num = self.channel.read_int(2)
        return [0x14, content, transfer_num]

    ## ============= send methods ===============

    ## send 'UNKNOWN_REQUEST_RSPNS' message
    ## parameters:
    ##    message: byte
    def send_unknown_request_rspns(self, message):
        self.channel.write_byte(0x01)  # "UNKNOWN_REQUEST_RSPNS"
        self.channel.write_byte(message)

    ## send 'ACKNOWLEDGE_RSPNS' message
    ## parameters:
    ##    message: byte
    def send_acknowledge_rspns(self, message):
        self.channel.write_byte(0x02)  # "ACKNOWLEDGE_RSPNS"
        self.channel.write_byte(message)

    ## send 'CURRENT_TIME_MS_RSPNS' message
    ## parameters:
    ##    time: int32
    def send_current_time_ms_rspns(self, time):
        self.channel.write_byte(0x04)  # "CURRENT_TIME_MS_RSPNS"
        self.channel.write_int(time, 4)

    ## send 'CURRENT_TIME_US_RSPNS' message
    ## parameters:
    ##    time: int32
    def send_current_time_us_rspns(self, time):
        self.channel.write_byte(0x05)  # "CURRENT_TIME_US_RSPNS"
        self.channel.write_int(time, 4)

    ## send 'CURRENT_TIME_CPU_RSPNS' message
    ## parameters:
    ##    time: int32
    def send_current_time_cpu_rspns(self, time):
        self.channel.write_byte(0x06)  # "CURRENT_TIME_CPU_RSPNS"
        self.channel.write_int(time, 4)

    ## send 'INTERNAL_TEMP_RSPNS' message
    ## parameters:
    ##    temperature: int16
    def send_internal_temp_rspns(self, temperature):
        self.channel.write_byte(0x07)  # "INTERNAL_TEMP_RSPNS"
        self.channel.write_int(temperature, 2)

    ## send 'CHANNEL_STATE_RSPNS' message
    ## parameters:
    ##    channel_enable_flags: byte
    def send_channel_state_rspns(self, channel_enable_flags):
        self.channel.write_byte(0x08)  # "CHANNEL_STATE_RSPNS"
        self.channel.write_byte(channel_enable_flags)

    ## send 'MEASURED_NO_RSPNS' message
    ## parameters:
    ##    measure_num: int16
    def send_measured_no_rspns(self, measure_num):
        self.channel.write_byte(0x09)  # "MEASURED_NO_RSPNS"
        self.channel.write_int(measure_num, 2)

    ## send 'MEASURE_RSPNS' message
    ## parameters:
    ##    measure_bytes: bytearray
    def send_measure_rspns(self, measure_bytes):
        self.channel.write_byte(0x0A)  # "MEASURE_RSPNS"
        self.channel.write_int(len(measure_bytes), 2)
        self.channel.write_bytes(measure_bytes)

    ## send 'MEASURE_TIME_RSPNS' message
    ## parameters:
    ##    measure_bytes: bytearray
    def send_measure_time_rspns(self, measure_bytes):
        self.channel.write_byte(0x0B)  # "MEASURE_TIME_RSPNS"
        self.channel.write_int(len(measure_bytes), 2)
        self.channel.write_bytes(measure_bytes)

    ## send 'TEST_BYTES_RSPNS' message
    ## parameters:
    ##    data_bytes: bytearray
    def send_test_bytes_rspns(self, data_bytes):
        self.channel.write_byte(0x0C)  # "TEST_BYTES_RSPNS"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)

    ## send 'TEST_TEXT_RSPNS' message
    ## parameters:
    ##    content: str
    def send_test_text_rspns(self, content):
        self.channel.write_byte(0x0D)  # "TEST_TEXT_RSPNS"
        self.channel.write_text(content)
