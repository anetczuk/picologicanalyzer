#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


$SCRIPT_DIR/src/protogen/generate.sh


# tests
$SCRIPT_DIR/src/testanalyzerlib/runtests.py
$SCRIPT_DIR/src/host/testhostanalyzer/runtests.py
$SCRIPT_DIR/src/pico/testpicoanalyzer/runtests.py


$SCRIPT_DIR/doc/generate-doc.sh

$SCRIPT_DIR/tools/mdpreproc.py $SCRIPT_DIR/README.md

$SCRIPT_DIR/tools/checkall.sh


echo "generation completed"
