import argparse
import json
import os
import asyncio
from datetime import datetime

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


def compare_files(verbose, file_name, file_old, file_new, log):
    if file_old != file_new:
        print('Changes in file: ' + file_name, file=log)
        if verbose > 0:
            for key in list(file_old.keys()):
                if 'time' in key:
                    old_value = datetime.fromtimestamp(file_old[key])
                    new_value = datetime.fromtimestamp(file_new[key])
                else:
                    old_value, new_value = file_old[key], file_new[key]
                if old_value != file_new[key]:
                    print(f"{INDENT}Value {key} was changed" +
                          (verbose > 1) * f" from {old_value} to {new_value}", file=log)


def scan(directory, json_file):
    metadata = {}
    for direct in directory:
        for root, dirs, files in os.walk(direct):
            for file in files:
                file_name = os.path.join(root, file)
                metadata[file_name] = file_info(file_name)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=INDENT)


async def async_scan(directory_list, metadata_file):
    metadata = await asyncio.gather(*[scan_dir(directory) for directory in directory_list])
    metadata = {key: value for d in metadata for key, value in d.items()}
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=INDENT)


async def scan_dir(directory):
    metadata = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name = os.path.join(root, file)
            metadata[file_name] = file_info(file_name)
    await asyncio.sleep(1)
    return metadata


def detect(arguments, log):
    with open(arguments.metadata, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        file_list = list(metadata.keys())
        for root, dirs, files in os.walk(arguments.directory):
            for file in files:
                file_name = os.path.join(root, file)
                if file_name not in file_list:
                    print('New file: ' + file_name, file=log)
                else:
                    file_list.remove(file_name)
                    compare_files(arguments.verbose, file_name, metadata[file_name], file_info(file_name), log)
        for file_name in file_list:
            print('Removed file: ' + file_name, file=log)


async def async_detect(arguments, log):
    with open(arguments.metadata, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        metadata_files = list(metadata.keys())
        file_list = await asyncio.gather(*[detect_dir(directory, arguments, metadata, log) for directory in arguments.directory])
        file_list = [item for sublist in file_list for item in sublist]
        for file in metadata_files:
            if file not in file_list:
                print('Removed file: ' + file, file=log)


async def detect_dir(directory, arguments, metadata, log):
    file_list = []
    metadata_files = list(metadata.keys())
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_name = os.path.join(root, file)
            file_list.append(file_name)
            if file_name not in metadata_files:
                print('New file: ' + file_name, file=log)
            else:
                compare_files(arguments.verbose, file_name, metadata[file_name], file_info(file_name), log)
    await asyncio.sleep(1)
    return file_list


def main(arguments):
    if arguments.run_option == 'scan':
        if arguments.asyncio:
            asyncio.run(async_scan(arguments.directory, arguments.metadata))
        else:
            scan(arguments.directory, arguments.metadata)
    else:
        if arguments.log:
            with open(arguments.log, 'a') as log:
                print('-'*20, file=log)
                if arguments.asyncio:
                    asyncio.run(async_detect(arguments, log))
                else:
                    detect(arguments, log)
        else:
            if arguments.asyncio:
                asyncio.run(async_detect(arguments, None))
            else:
                detect(arguments, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('run_option', choices=['scan', 'detect'])
    parser.add_argument('-d', '--directory', type=str, nargs='+', default=[DEFAULT_DIRECTORY])
    parser.add_argument('-v', '--verbose', type=int, default=DEFAULT_VERBOSE)
    parser.add_argument('-m', '--metadata', type=str, default=DEFAULT_METADATA_FILE)
    parser.add_argument('-l', '--log', type=str, default=None)
    parser.add_argument('-a', '--asyncio', action='store_true', default=False)

    args = parser.parse_args()

    main(args)
