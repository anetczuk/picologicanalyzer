#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


OUT_DIR="$SCRIPT_DIR/measurements"

mkdir -p "$OUT_DIR"


$SCRIPT_DIR/../src/host/sample/generate-charts.sh "$OUT_DIR"


# $SCRIPT_DIR/generate_small.sh
