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


SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


PROJ_DIR="$SCRIPT_DIR/picoanalyzer"


help_info() {
    echo "parameters:"
    echo "      --help      this message"
    echo "      --upload    upload project, otherwise run main.py script"
    echo "      --run       upload and run particular script (default main.py)"
    exit 0
}


RUN_SCRIPT=""
UPLOAD=""

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      help_info
      ;;

    --run)
      RUN_SCRIPT="$2"
      shift # past argument
      shift # past value
      ;;

    --upload)
      UPLOAD=YES
      shift # past argument
      ;;

    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;

    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done


if [[ ! -z $UPLOAD ]]; then
    echo "uploading the project"

    # reset previous connection (otherwise rshell will hang on connection)
    sudo ~/.local/bin/ampy --port /dev/ttyACM0 reset

	sudo rshell mkdir /pyboard/analyzerlib
	sudo rshell cp $PROJ_DIR/../../analyzerlib/* /pyboard/analyzerlib

    sudo rshell cp $PROJ_DIR/* /pyboard

    echo "upload completed"
    exit 0
fi

if [[ ! -z $RUN_SCRIPT ]]; then
    echo "running script $RUN_SCRIPT"

    sudo ~/.local/bin/ampy --port /dev/ttyACM0 -d 0.5 run "$RUN_SCRIPT"

    exit 0
fi


echo "running the project"

sudo ~/.local/bin/ampy --port /dev/ttyACM0 -d 0.5 run "$PROJ_DIR/main.py"
