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


if __name__ == '__main__':
    argv = sys.argv
    files = list()
    if os.path.isfile(argv[1]) and argv[1].endswith('.jack'):
        files.append(argv[1])
    else:
        files = get_files_in_path(argv[1])
    for file_address in files:
        content = files_to_string(file_address)
        file_address = file_address[:-4] + 'xml'
        parser = Parser(content)
        Worker(parser.meal, file_address)
