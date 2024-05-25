#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#


class SensorMessage:

    UNKNOWN_REQUEST_RSPNS = 0x01
    ACKNOWLEDGE_RSPNS = 0x02
    CURRENT_TIME_MS_RSPNS = 0x04
    CURRENT_TIME_US_RSPNS = 0x05
    CURRENT_TIME_CPU_RSPNS = 0x06
    INTERNAL_TEMP_RSPNS = 0x07
    CHANNEL_STATE_RSPNS = 0x08
    MEASURED_NO_RSPNS = 0x09
    MEASURE_RSPNS = 0x0A
    MEASURE_TIME_RSPNS = 0x0B
    TEST_BYTES_RSPNS = 0x0C
    TEST_TEXT_RSPNS = 0x0D

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "UNKNOWN_REQUEST_RSPNS"
        if value == 0x02:
            return "ACKNOWLEDGE_RSPNS"
        if value == 0x04:
            return "CURRENT_TIME_MS_RSPNS"
        if value == 0x05:
            return "CURRENT_TIME_US_RSPNS"
        if value == 0x06:
            return "CURRENT_TIME_CPU_RSPNS"
        if value == 0x07:
            return "INTERNAL_TEMP_RSPNS"
        if value == 0x08:
            return "CHANNEL_STATE_RSPNS"
        if value == 0x09:
            return "MEASURED_NO_RSPNS"
        if value == 0x0A:
            return "MEASURE_RSPNS"
        if value == 0x0B:
            return "MEASURE_TIME_RSPNS"
        if value == 0x0C:
            return "TEST_BYTES_RSPNS"
        if value == 0x0D:
            return "TEST_TEXT_RSPNS"

        # unhandled value
        return None
