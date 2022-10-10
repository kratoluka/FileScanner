import argparse
import json
import os
from datetime import datetime
import subprocess

DEFAULT_DIRECTORY = '.\\'
DEFAULT_VERBOSE = 0
DEFAULT_METADATA_FILE = 'metadata.json'

INDENT = 4 * ' '


def file_info(file):
    info = {}
    info['size'] = os.path.getsize(file)
    info['time_modified'] = os.path.getmtime(file)
    info['time_created'] = os.path.getctime(file)
    info['access_rights'] = oct(os.stat(file).st_mode)
    return info


def uncase(text):
    return ' '.join(text.split('_')).capitalize()


def compare_files(verbose, file_name, file_old, file_new):
    if file_old != file_new:
        print('Changes in file ' + file_name)
        if verbose > 0:
            for key in list(file_old.keys()):
                if 'time' in key:
                    old_value = datetime.fromtimestamp(file_old[key])
                    new_value = datetime.fromtimestamp(file_new[key])
                else:
                    old_value, new_value = file_old[key], file_new[key]
                if old_value != file_new[key]:
                    print(f"{INDENT}Value {key} was changed" +
                          (verbose > 1) * f" from {old_value} to {new_value}")


def scan(directory, json_file):
    metadata = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name = os.path.join(root, file)
            metadata[file_name] = file_info(file_name)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=INDENT)


def detect(arguments):
    with open(arguments.metadata, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        file_list = list(metadata.keys())
        for root, dirs, files in os.walk(arguments.directory):
            for file in files:
                file_name = os.path.join(root, file)
                if file_name not in file_list:
                    print('New file: ' + file_name)
                else:
                    file_list.remove(file_name)
                    compare_files(arguments.verbose, file_name, metadata[file_name], file_info(file_name))
        for file_name in file_list:
            print('Removed file: ' + file_name)


def main(arguments):
    if arguments.run_option == 'scan':
        scan(arguments.directory, arguments.metadata)
    else:
        detect(arguments)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('run_option', choices=['scan', 'detect'])
    parser.add_argument('-d', '--directory', type=str, default=DEFAULT_DIRECTORY)
    parser.add_argument('-v', '--verbose', type=int, default=DEFAULT_VERBOSE)
    parser.add_argument('-m', '--metadata', type=str, default=DEFAULT_METADATA_FILE)
    parser.add_argument('-l', '--log', type=str, default=None)

    args = parser.parse_args()

    main(args)
