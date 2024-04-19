#!/bin/bash

##
## Script allows uploading and running remotely Python project.
##

set -eu


if ! ampy --help > /dev/null; then
    echo "missing adafruit-ampy package, run following command to install:"
    echo "      pip3 install adafruit-ampy"
    exit 1
fi

if ! rshell --version > /dev/null; then
    echo "missing rshell package, run following command to install:"
    echo "      pip3 install rshell"
    exit 1
fi


if [[ $* == *--clear* ]]; then
	echo "removing log file"
	sudo rshell rm /pyboard/log.txt
	exit 0
fi

sudo ~/.local/bin/ampy --port /dev/ttyACM0 -d 0.5 get log.txt
