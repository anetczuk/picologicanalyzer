#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#


class SensorMessage:

    UNKNOWN_REQUEST_RSPNS = 0x01
    INTERNAL_TEMP_RSPNS = 0x02
    MEASURE_RSPNS = 0x03
    CHANNEL_STATE_RSPNS = 0x04
    TEST_BYTES_RSPNS = 0x05
    TEST_TEXT_RSPNS = 0x06

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "UNKNOWN_REQUEST_RSPNS"
        if value == 0x02:
            return "INTERNAL_TEMP_RSPNS"
        if value == 0x03:
            return "MEASURE_RSPNS"
        if value == 0x04:
            return "CHANNEL_STATE_RSPNS"
        if value == 0x05:
            return "TEST_BYTES_RSPNS"
        if value == 0x06:
            return "TEST_TEXT_RSPNS"

        # unhandled value
        return None
