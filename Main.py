#!/usr/bin/env python
import os
import sys

from Parser import Parser
from Worker import Worker


def files_to_string(path):
    jack = open(path)
    lines = ''
    for line in jack:
        lines += line
    jack.close()
    return lines


def get_files_in_path(path):
    files_list = os.listdir(path)
    files = []
    for file in files_list:
        filename = os.path.join(path, file)
        if file.endswith('.jack') and os.path.isfile(filename):
            files.append(filename)
    return files


def main(arg):
    files = list()
    if os.path.isfile(arg[1]) and arg[1].endswith('.jack'):
        files.append(arg[1])
    else:
        files = get_files_in_path(arg[1])
    for file_address in files:
        content = files_to_string(file_address)
        file_address = file_address[:-4] + 'xml'
        parser = Parser(content)
        Worker(parser.meal, file_address)


if __name__ == '__main__':
    main(sys.argv)
