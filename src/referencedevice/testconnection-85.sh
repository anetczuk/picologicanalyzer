#!/bin/bash

set -eu


COMMAND="avrdude -p attiny85 -P usb -c usbasp"


if [[ $* == *--help* ]]; then
    echo "parameters:"
    echo "      {no param}  try reading fuse once"
    echo "      --repeat    try to connect to device (in loop until succees)"
    echo "      --find      iterate over bit rate range and find working value"
    echo "      --help      this message"
    exit 0
fi


if [[ $* == *--find* ]]; then
    COUNTER=4

    while true; do
        if sudo $COMMAND -B$COUNTER -v; then
            echo "found rate: $COUNTER"
            break;
        fi

        COUNTER=$[$COUNTER *2]
        if [ $COUNTER -ge 2048 ]; then
            echo "unable to find bit rate"
            exit 1
        fi

        sleep 1
    done

    echo "Done"
    exit 0
fi


if [[ $* == *--repeat* ]]; then
    while true; do
        if sudo $COMMAND -B4 -v; then
            break;
        fi
        sleep 1
    done

    echo "Done"
    exit 0
fi



if sudo $COMMAND -B4 -v; then
	echo "Done"
else
	echo -e "\nUnable to connect (check wiring)"
fi
