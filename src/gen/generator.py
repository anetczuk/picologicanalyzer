#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import os
import logging
import argparse

import json
import csv

from pandas import DataFrame

import texthon


_LOGGER = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(__file__)  ## full path to script's directory


# ====================================================================
# ====================================================================


ALLOWED_DIRECTION = ["BOTH", "TO_PY", "TO_GD", "DISABLED"]


def generate(input_json_path, output_dir):
    _LOGGER.info("parsing file %s", input_json_path)

    os.makedirs(output_dir, exist_ok=True)

    config_dict = parse_json(input_json_path)

    messages_defs = config_dict["messages"]
    prepare_messages(messages_defs)

    to_a_msgs = get_messages_by_direction(messages_defs, ["TO_A", "BOTH"])
    to_b_msgs = get_messages_by_direction(messages_defs, ["TO_B", "BOTH"])

    message_id_type = config_dict["message_id_type"]
    generate_message_values(to_a_msgs, message_id_type)
    generate_message_values(to_b_msgs, message_id_type)

    device_a = config_dict["device_a"]
    generate_enum(device_a, to_b_msgs, output_dir)
    generate_device(config_dict, device_a, to_b_msgs, to_a_msgs, output_dir)

    device_b = config_dict["device_b"]
    generate_enum(device_b, to_a_msgs, output_dir)
    generate_device(config_dict, device_b, to_a_msgs, to_b_msgs, output_dir)


def generate_enum(device_config, send_messages, output_dir):
    enum_name = device_config["enum_name"]
    enum_template = device_config["enum_template"]

    template_params = {"class_name": enum_name, "messages": send_messages}

    template_path = os.path.join(SCRIPT_DIR, "template", enum_template)
    output_path = os.path.join(output_dir, enum_name.lower() + ".py")
    _LOGGER.info("generating file %s", output_path)
    generate_file(template_path, template_params, output_path)


def generate_message_values(messages_list, message_id_type):
    filtered_messages = []
    counter = 0
    for message in messages_list:
        if "value" in message:
            continue
        counter += 1
        if message_id_type == "str":
            message_id = message["id"]
            message["value"] = f'"{message_id}"'
        elif message_id_type == "int":
            message["value"] = f"{counter}"
        elif message_id_type == "hex":
            value = f"{counter:#04x}"
            message["value"] = f"{value}"
        else:
            raise RuntimeError(f"invalid id type: '{message_id_type}'")
    return filtered_messages


def generate_device(config_dict, device_config, send_messages, receive_messages, output_dir):
    class_name = device_config["class_name"]
    class_template = device_config["class_template"]

    template_params = {
        "config_dict": config_dict,
        "class_name": class_name,
        "send_messages": send_messages,
        "receive_messages": receive_messages,
    }

    template_path = os.path.join(SCRIPT_DIR, "template", class_template)
    output_path = os.path.join(output_dir, class_name.lower() + ".py")
    _LOGGER.info("generating file %s", output_path)
    generate_file(template_path, template_params, output_path)


def generate_file(template_path, template_params, output_path):
    engine = texthon.Engine()
    module_def = engine.load_file(template_path)  # parse and store the parsed module
    module_id = module_def.path  # store the path so we can find the compiled module later

    engine.make()  # compile all modules

    #     with open( PARAMS_PATH, "r" ) as params_file:
    #         params_content = params_file.read()
    #         params = eval( params_content )

    module = engine.modules[module_id]

    # call the template function named 'main'
    #     script_content = module.main( messages = messages_defs )
    script_content = module.main(**template_params)

    ### === writing to file ===
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(script_content)


def prepare_messages(messages_defs):
    for message in messages_defs:
        params = message["params"]
        param_names = []
        for par in params:
            param_names.append(par["id"])
        message["param_names"] = param_names


# ===================================================================


def get_messages_by_direction(messages_list, allowed_directions):
    filtered_messages = []
    for message in messages_list:
        if message["direction"] in allowed_directions:
            filtered_messages.append(message)
    return filtered_messages


def read_messages_defs_csv(dataMatrix):
    messages_defs = []

    for _, row in dataMatrix.iterrows():
        message_id = row["message id"]
        _LOGGER.info("handling message %s", message_id)

        direction: str = row["direction"]
        direction = direction.strip()
        if not direction:
            direction = "BOTH"
        elif direction not in ALLOWED_DIRECTION:
            _LOGGER.error("invalid 'direction' parameter: '%s' allowed: %s", direction, ALLOWED_DIRECTION)
            direction = "BOTH"

        method_args_list = read_args(row)

        messages_dict = {}
        messages_dict["id"] = message_id
        messages_dict["direction"] = direction
        messages_dict["params"] = method_args_list

        messages_defs.append(messages_dict)

    return messages_defs


def read_args(row):
    method_args_list = []
    field_index = -1
    while True:
        field_index += 1
        field_name = "field " + str(field_index)
        field_value = get_row_value(row, field_name, None)
        if field_value is None:
            break
        method_args_list.append(field_value)
    return method_args_list


def get_row_value(row, key, default_value):
    try:
        rowVal = row[key]
        if not is_field_empty(rowVal):
            return rowVal
        return default_value
    except KeyError:
        return None


def is_field_empty(value):
    if value is None:
        return True
    if len(str(value)) < 1:
        return True
    return False


# ===================================================================


def parse_json(json_path):
    with open(json_path, encoding="utf-8") as json_file:
        ret_dict = json.load(json_file)
        ret_dict["input_file"] = json_path
        return ret_dict


## returns tuple ( config_dict, data_matrix )
def parse_csv(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        dataReader = csv.reader(csvfile, delimiter=",", quotechar="|")

        configPart = False
        dataPart = False

        configList = []
        dataList = []

        for line in dataReader:
            # print( line )
            rawLine = "".join(line)
            if len(rawLine) > 0:
                if rawLine == "Config:":
                    configPart = True
                    continue
                if rawLine == "Data:":
                    dataPart = True
                    continue
                # if rawLine[0] == '#':
                #    continue
                # if rawLine.startswith( "//" ):
                #    continue
            else:
                configPart = False
                dataPart = False
                continue

            if configPart is True:
                configList.append(line)
            elif dataPart is True:
                dataList.append(line)

        configMatrix = create_matrix(configList)
        dataMatrix = create_matrix(dataList)

        ## convert matrix to dict
        zip_iterator = zip(configMatrix["parameter"], configMatrix["value"])
        configDict = dict(zip_iterator)

        return (configDict, dataMatrix)
    return (None, None)


def create_matrix(dataList):
    if len(dataList) < 1:
        raise Exception("No data field found")

    matrixHeader = dataList[0]
    matrixData = DataFrame(dataList)

    ## remove redundant columns
    headerSize = len(matrixHeader)
    colsNum = len(matrixData.columns)
    if colsNum > headerSize:
        for _ in range(headerSize, colsNum):
            colName = matrixData.columns[len(matrixData.columns) - 1]
            matrixData.drop(colName, axis=1, inplace=True)

    matrixData.columns = matrixHeader

    matrixData = matrixData.iloc[1:]  ## remove first row (containing header labels)

    return matrixData


# ====================================================================
# ====================================================================


def configure_logger(level=None):
    formatter = create_formatter()
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(formatter)

    logging.root.addHandler(consoleHandler)
    if level is None:
        logging.root.setLevel(logging.INFO)
    else:
        logging.root.setLevel(level)


def create_formatter(loggerFormat=None):
    if loggerFormat is None:
        loggerFormat = "%(asctime)s,%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    #        loggerFormat = ('%(asctime)s,%(msecs)-3d %(levelname)-8s %(threadName)s %(name)s:%(funcName)s '
    #                        '[%(filename)s:%(lineno)d] %(message)s')
    dateFormat = "%H:%M:%S"
    #    dateFormat = '%Y-%m-%d %H:%M:%S'
    return logging.Formatter(loggerFormat, dateFormat)


def main():
    parser = argparse.ArgumentParser(description="Protocol generator")
    parser.add_argument(
        "-ll",
        "--log_level",
        action="store",
        default="INFO",
        help="Set log level: DEBUG, INFO, WARNING, ERROR, CRITICAL, default: INFO",
    )
    parser.add_argument("--input_config", action="store", required=True, help="Configuration file (json)")
    parser.add_argument("--output_dir", action="store", required=True, help="Directory to output data")

    args = parser.parse_args()

    configure_logger(args.log_level)

    generate(args.input_config, args.output_dir)

    _LOGGER.info("done")

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
