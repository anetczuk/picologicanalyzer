#!/bin/bash

set -eu


PICO_DEVID=$(lsusb | grep "MicroPython Board in FS mode" | awk '{print $6}')

if [ -z "${PICO_DEVID}" ]; then
    echo "RPi Pico not connected"
    exit 1
fi


echo "resetting device $PICO_DEVID"

sudo usbreset "$PICO_DEVID"

echo "done"
