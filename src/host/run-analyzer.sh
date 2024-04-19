#!/bin/bash

set -eu

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


ANALYZERLIB="$SCRIPT_DIR/.."

if [ ! -z ${PYTHONPATH+x} ]; then
	export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR:$ANALYZERLIB
else
	export PYTHONPATH=$SCRIPT_DIR:$ANALYZERLIB
fi


cd $SCRIPT_DIR

python3 $SCRIPT_DIR/hostanalyzer/main.py $@


## ModuleNotFoundError: No module named 'analyzer.channel'
# python3 -m analyzer.main


## ModuleNotFoundError: No module named 'analyzer.channel'
# python3 -m analyzer $@
