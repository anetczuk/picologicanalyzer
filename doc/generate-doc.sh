#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


SRC_DIR="$SCRIPT_DIR/../src"

HELP_PATH=$SCRIPT_DIR/cmdargs.md
PROGRAM_COMMAND="python3 -m astgraph"


cd $SRC_DIR


PROGRM_LABEL="${PROGRAM_COMMAND}"
if [ -f "${PROGRM_LABEL}" ]; then
    PROGRM_LABEL=$(basename "${PROGRM_LABEL}")
fi


generate_help() {
    
    echo "## <a name=\"main_help\"></a> ${PROGRM_LABEL} --help" > ${HELP_PATH}
    echo -e "\`\`\`" >> ${HELP_PATH}
    ${PROGRAM_COMMAND} --help >> ${HELP_PATH}
    echo -e "\`\`\`" >> ${HELP_PATH}
    
    
#     tools=$(${PROGRAM_COMMAND} --listtools)
#     
#     IFS=', ' read -r -a tools_list <<< "$tools"   # convert output to array
#     
#     
#     for item in ${tools_list[@]}; do
#         echo $item
#         echo -e "\n\n" >> ${HELP_PATH}
#         echo "## <a name=\"${item}_help\"></a> ${PROGRM_LABEL} $item --help" >> ${HELP_PATH}
#         echo -e "\`\`\`" >> ${HELP_PATH}
#         ${PROGRAM_COMMAND} $item --help >> ${HELP_PATH}
#         echo -e "\`\`\`"  >> ${HELP_PATH}
#     done
}


# generate_help


$SCRIPT_DIR/generate_small.sh
