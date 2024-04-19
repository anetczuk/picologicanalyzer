#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


GEN_PATH="$SCRIPT_DIR/generator.py"


$GEN_PATH --input_config "$SCRIPT_DIR/protocol.json" --output_dir "$SCRIPT_DIR/../analyzerlib" $@
