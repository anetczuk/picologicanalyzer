#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#


class SensorMessage:

    UNKNOWN_REQUEST_RSPNS = 0x01
    SET_KBD_INTR_RSPNS = 0x02
    INTERNAL_TEMP_RSPNS = 0x03
    MEASURE_RSPNS = 0x04
    CHANNEL_STATE_RSPNS = 0x05
    TEST_BYTES_RSPNS = 0x06
    TEST_TEXT_RSPNS = 0x07

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "UNKNOWN_REQUEST_RSPNS"
        if value == 0x02:
            return "SET_KBD_INTR_RSPNS"
        if value == 0x03:
            return "INTERNAL_TEMP_RSPNS"
        if value == 0x04:
            return "MEASURE_RSPNS"
        if value == 0x05:
            return "CHANNEL_STATE_RSPNS"
        if value == 0x06:
            return "TEST_BYTES_RSPNS"
        if value == 0x07:
            return "TEST_TEXT_RSPNS"

        # unhandled value
        return None
