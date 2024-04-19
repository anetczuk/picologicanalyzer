#
# File was automatically generated using protocol generator.
#

#
# Do not use enum classes. MicroPython does not support them.
#


class HostMessage:

    REQUEST_DATA = 0x01
    GET_CH_ENABLE = 0x02
    TEST_BYTES_REQUEST = 0x03
    TEST_TEXT_REQUEST = 0x04

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "REQUEST_DATA"
        if value == 0x02:
            return "GET_CH_ENABLE"
        if value == 0x03:
            return "TEST_BYTES_REQUEST"
        if value == 0x04:
            return "TEST_TEXT_REQUEST"

        # unhandled value
        return None
