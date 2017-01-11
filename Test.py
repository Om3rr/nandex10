import os

import Main


def run_over_dir(path):
    jack_files = list()
    dir_files = os.listdir(path)
    for file in dir_files:
        address = path + '/' + file
        if file.endswith('.jack') and os.path.isfile(address):
            jack_files.append(address)
        elif not os.path.isfile(address):
            jack_files += run_over_dir(address)
    return jack_files


def execute(jack_files):
    arg = ['', '']
    length = len(jack_files)
    counter = 0
    for jack_file in jack_files:
        counter += 1
        arg[1] = jack_file
        Main.main(arg)
    if counter < length - 1:
        print('problem, run just %s times' % counter)


def do_diff(jack_files):
    failed = list()
    for file in jack_files:
        xml_res = file[:-4] + 'xml'
        xml_sor = xml_res.replace('Tests', 'Expected')
        print('diff -w %s:' % file)
        result = os.system('diff -w %s ' % xml_res + xml_sor)
        if result != 0:
            failed.append(file)
        print(result, '\n')
    if len(failed) > 0:
        print('Failed in the files:')
        for file in failed:
            print(file)
    else:
        print('Congratulation you pass all the files successfully.')


if __name__ == '__main__':
    files = run_over_dir(os.getcwd() + '/Tests')
    execute(files)
    do_diff(files)
