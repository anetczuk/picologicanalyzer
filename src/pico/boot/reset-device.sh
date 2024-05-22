#!/bin/bash

set -eu


##
## Script uploads bootloader to connected RPi Pico
##


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


$SCRIPT_DIR/upload-clear.sh

sleep 4

while true; do
    if $SCRIPT_DIR/upload-micropython.sh; then
	    echo "reset completed"
	    exit 0
    fi
    sleep 1
done
