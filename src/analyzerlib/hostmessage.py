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
    SELECT_CHANNELS_RQST = 0x0a
    SET_PROBE_DELAY_US_RQST = 0x0b
    MEASURED_NO_RQST = 0x0c
    MEASURE_RQST = 0x0d
    MEASURE_TR_RQST = 0x0e
    MEASURE_TIME_RQST = 0x0f
    MEASURE_TIME_TR_RQST = 0x10
    TRANSFER_TIME_RQST = 0x11
    PROBE_TIME_RQST = 0x12
    TEST_BYTES_RQST = 0x13
    TEST_TEXT_RQST = 0x14
    TEST_MEASURE_TIME_RQST = 0x15

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
        if value == 0x0a:
            return "SELECT_CHANNELS_RQST"
        if value == 0x0b:
            return "SET_PROBE_DELAY_US_RQST"
        if value == 0x0c:
            return "MEASURED_NO_RQST"
        if value == 0x0d:
            return "MEASURE_RQST"
        if value == 0x0e:
            return "MEASURE_TR_RQST"
        if value == 0x0f:
            return "MEASURE_TIME_RQST"
        if value == 0x10:
            return "MEASURE_TIME_TR_RQST"
        if value == 0x11:
            return "TRANSFER_TIME_RQST"
        if value == 0x12:
            return "PROBE_TIME_RQST"
        if value == 0x13:
            return "TEST_BYTES_RQST"
        if value == 0x14:
            return "TEST_TEXT_RQST"
        if value == 0x15:
            return "TEST_MEASURE_TIME_RQST"

        # unhandled value
        return None
