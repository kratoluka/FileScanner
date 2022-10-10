import argparse
import json
import os
import subprocess

DEFAULT_DIRECTORY = '.\\'
DEFAULT_VERBOSE = 0
DEFAULT_METADATA_FILE = 'metadata.json'


def file_info(file):
    info = {}
    info['size'] = os.path.getsize(file)
    info['modified'] = os.path.getmtime(file)
    info['created'] = os.path.getctime(file)
    info['access_rights'] = oct(os.stat(file).st_mode)
    return info


def scan(directory, json_file):
    metadata = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name = os.path.join(root, file)
            metadata[file_name] = file_info(file_name)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)


def detect(arguments):
    pass


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
