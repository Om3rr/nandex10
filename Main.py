#!/usr/bin/env python
import os
import re
import sys

from Parser import Parser
from Worker import Worker

FILENAME = re.compile('([ \-\_\w]+).vm')


def path_to_string(path):
    jack = open(path)
    lines = ''
    for line in jack:
        lines += line
    jack.close()
    return lines


def getFilesInPath(path):
    files_list = os.listdir(arg[1])
    files = []
    for file in files_list:
        filename = os.path.join(path, file)
        if file.endswith('.vm') and os.path.isfile(filename):
            files.append(filename)
    return files


def argToPath(arg):
    if arg[-1] in ['\\','/']:
        arg = arg[:-1]
    # if '.vm' in arg:
    if os.path.isfile(arg):
        arg = arg.replace('.vm', '')
        return arg + '.asm'
    if arg.rfind('\\') != -1:
        return os.path.join(arg, arg[arg.rfind('\\') + 1:] + '.asm')
    elif arg.rfind('/') != -1:
        return os.path.join(arg, arg[arg.rfind('/') + 1:] + '.asm')
    elif '/' not in arg:
        arg = os.path.abspath(arg)
        return argToPath(arg)
        # return arg + '/' + arg + '.asm'
    return arg + '.asm'


if __name__ == '__main__':
    arg = sys.argv
    path = argToPath(arg[1])
    # print(path)
    if os.path.isdir(arg[1]):
        files = getFilesInPath(arg[1])
        writer = Worker(path)
    else:
        files = [arg[1]]
        writer = Worker(path)
    for jack_file in files:
        m = FILENAME.search(jack_file)
        Parser(path_to_string(jack_file), m.group(1).replace(" ", "_"), writer)
    writer.save()
