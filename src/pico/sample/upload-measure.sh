#!/bin/bash

set -eu


SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


$SCRIPT_DIR/../send-pico-analyzer.sh --upload

$SCRIPT_DIR/../send-pico-analyzer.sh --upload-runner $SCRIPT_DIR/measure.py
