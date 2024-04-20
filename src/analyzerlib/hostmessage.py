#
# File was automatically generated using protocol generator.
#

#
# Do not use enum classes. MicroPython does not support them.
#


class HostMessage:

    MEASURE_RQST = 0x01
    CH_STATE_RQST = 0x02
    INTERNAL_TEMP_RQST = 0x03
    TEST_BYTES_RQST = 0x04
    TEST_TEXT_RQST = 0x05

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "MEASURE_RQST"
        if value == 0x02:
            return "CH_STATE_RQST"
        if value == 0x03:
            return "INTERNAL_TEMP_RQST"
        if value == 0x04:
            return "TEST_BYTES_RQST"
        if value == 0x05:
            return "TEST_TEXT_RQST"

        # unhandled value
        return None
