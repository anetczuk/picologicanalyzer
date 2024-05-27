#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


if [ $# -eq 0 ]; then
    echo "Missing input parameter: output directory"
    exit 1
fi

OUT_DIR="$1"

mkdir -p "$OUT_DIR"


$SCRIPT_DIR/bytes_transfer.py --outplotfile $OUT_DIR/bytes_transfer.png

$SCRIPT_DIR/measure_time_duration.py --outplotfile $OUT_DIR/measure_time_duration.png

$SCRIPT_DIR/measure_time_value.py --outplotfile $OUT_DIR/measure_time_value.png

$SCRIPT_DIR/pico_send_time.py --outplotfile $OUT_DIR/pico_send_time.png
