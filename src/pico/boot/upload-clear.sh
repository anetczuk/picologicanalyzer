#!/bin/bash

set -eu


##
## Script uploads bootloader to connected RPi Pico
##


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


BOOT_PATH="$SCRIPT_DIR/flash_nuke.uf2"


PICO_PATH=$(mount | grep "RPI-RP2" | awk '{print $3}')

if [ ! -d "${PICO_PATH}" ]; then
    echo "RPi Pico not mounted"
    exit 1
fi


set -x

cp "${BOOT_PATH}" "${PICO_PATH}"


echo "uploading completed"
