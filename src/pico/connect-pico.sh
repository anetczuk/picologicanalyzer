#!/bin/bash

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


# reset previous connection (otherwise rshell will hang on connection)
sudo ~/.local/bin/ampy --port /dev/ttyACM0 reset

sudo rshell


# # $1 - syspath
# get_id_serial() {
#     local syspath=$1
# 
#     ID_SERIAL=""
#     eval "$(udevadm info -q property --export -p $syspath)"
#     if [[ -z "$ID_SERIAL" ]]; then
#         echo ""
#     else
#         echo "$ID_SERIAL"
#     fi
# }
# 
# 
# for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
#     syspath="${sysdevpath%/dev}"
#     devname="$(udevadm info -q name -p $syspath)"
#     if [[ "$devname" == "bus/"* ]]; then
#         continue
#     fi
#     ID_SERIAL=$(get_id_serial "$syspath")
#     if [[ -z "$ID_SERIAL" ]]; then
#         continue
#     fi
# 
#     if [[ $ID_SERIAL == *"MicroPython_Board"* ]]; then
#         echo "connecting to /dev/$devname"
#         sudo rshell -p "/dev/$devname" --buffer-size 512
#         exit 0
#     fi
# done
# 
# 
# echo "could not find Raspberry Pico device"
# exit 1
