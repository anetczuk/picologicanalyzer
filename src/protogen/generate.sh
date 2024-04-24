#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


python3 -m mpyserialprotogen --input_config "$SCRIPT_DIR/protocol.json" --output_dir "$SCRIPT_DIR/.." $@
