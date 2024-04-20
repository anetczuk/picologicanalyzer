#
# File was automatically generated using protocol generator.
#

#
# Do not use enum classes. MicroPython does not support them.
#


class SensorMessage:

    MEASURE_RSPNS = 0x01
    CH_STATE_RSPNS = 0x02
    INTERNAL_TEMP_RSPNS = 0x03
    TEST_BYTES_RSPNS = 0x04
    TEST_TEXT_RSPNS = 0x05

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "MEASURE_RSPNS"
        if value == 0x02:
            return "CH_STATE_RSPNS"
        if value == 0x03:
            return "INTERNAL_TEMP_RSPNS"
        if value == 0x04:
            return "TEST_BYTES_RSPNS"
        if value == 0x05:
            return "TEST_TEXT_RSPNS"

        # unhandled value
        return None
