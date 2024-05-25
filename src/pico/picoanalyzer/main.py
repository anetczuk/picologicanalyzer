#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import utime

import board

from filelogger import FileLogger


# ==========================================================


def loop(logger: FileLogger):
    try:
        from runner import start

        while True:

            board.blink_led(1.0)
            utime.sleep_ms(100)
            board.blink_led(1.0)
            utime.sleep_ms(100)
            board.blink_led(1.0)

            restart = start(logger)
            if not restart:
                logger.warn("received termination request")
                return

            logger.warn("restarting runner")

    finally:
        logger.info("exiting main")


# ================= main sequence =================


def main():
    with FileLogger("log.txt", "a") as logger:
        try:
            logger.info("===== initializing =====")

            loop(logger)

        except KeyboardInterrupt:
            logger.error("stopping main loop - received keyboard interrupt")

        except BaseException as exc:  # pylint: disable=W0703
            logger.error("stopping main loop - received general exception:")
            logger.error(f"exception: {exc}")
            logger.exception(exc)

        finally:
            # signal before stop
            for _ in range(0, 10):
                utime.sleep(0.2)
                board.blink_led(0.2)

            logger.info("script terminated")


main()
