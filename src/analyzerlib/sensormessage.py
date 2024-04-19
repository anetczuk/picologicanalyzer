#
# File was automatically generated using protocol generator.
#

#
# Do not use enum classes. MicroPython does not support them.
#


class SensorMessage:

    RESPONSE_DATA = 0x01
    SEND_CH_ENABLE = 0x02
    TEST_BYTES_RESPONSE = 0x03
    TEST_TEXT_RESPONSE = 0x04

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "RESPONSE_DATA"
        if value == 0x02:
            return "SEND_CH_ENABLE"
        if value == 0x03:
            return "TEST_BYTES_RESPONSE"
        if value == 0x04:
            return "TEST_TEXT_RESPONSE"

        # unhandled value
        return None
