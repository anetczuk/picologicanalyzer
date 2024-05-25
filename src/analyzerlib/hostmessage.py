#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#


class HostMessage:

    SET_KBD_INTR_RQST = 0x01
    TERMINATE_RQST = 0x02
    SET_INTERNAL_LED_RQST = 0x04
    CURRENT_TIME_MS_RQST = 0x05
    CURRENT_TIME_US_RQST = 0x06
    CURRENT_TIME_CPU_RQST = 0x07
    INTERNAL_TEMP_RQST = 0x08
    CHANNEL_STATE_RQST = 0x09
    SELECT_CHANNELS_RQST = 0x0A
    SET_MEASURE_BUFF_SIZE_RQST = 0x0B
    MEASURED_NO_RQST = 0x0C
    MEASURE_RQST = 0x0D
    MEASURE_TR_RQST = 0x0E
    MEASURE_TIME_RQST = 0x0F
    MEASURE_TIME_TR_RQST = 0x10
    TEST_TRANSFER_TIME_RQST = 0x11
    TEST_MEASURE_TIME_RQST = 0x13
    TEST_BYTES_RQST = 0x14
    TEST_TEXT_RQST = 0x15

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "SET_KBD_INTR_RQST"
        if value == 0x02:
            return "TERMINATE_RQST"
        if value == 0x04:
            return "SET_INTERNAL_LED_RQST"
        if value == 0x05:
            return "CURRENT_TIME_MS_RQST"
        if value == 0x06:
            return "CURRENT_TIME_US_RQST"
        if value == 0x07:
            return "CURRENT_TIME_CPU_RQST"
        if value == 0x08:
            return "INTERNAL_TEMP_RQST"
        if value == 0x09:
            return "CHANNEL_STATE_RQST"
        if value == 0x0A:
            return "SELECT_CHANNELS_RQST"
        if value == 0x0B:
            return "SET_MEASURE_BUFF_SIZE_RQST"
        if value == 0x0C:
            return "MEASURED_NO_RQST"
        if value == 0x0D:
            return "MEASURE_RQST"
        if value == 0x0E:
            return "MEASURE_TR_RQST"
        if value == 0x0F:
            return "MEASURE_TIME_RQST"
        if value == 0x10:
            return "MEASURE_TIME_TR_RQST"
        if value == 0x11:
            return "TEST_TRANSFER_TIME_RQST"
        if value == 0x13:
            return "TEST_MEASURE_TIME_RQST"
        if value == 0x14:
            return "TEST_BYTES_RQST"
        if value == 0x15:
            return "TEST_TEXT_RQST"

        # unhandled value
        return None
