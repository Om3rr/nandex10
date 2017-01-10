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
        # print('Working on', jack_file)
        arg[1] = jack_file
        Main.main(arg)
        # print('Done working on', jack_file)
    if counter < length - 1:
        print('problem, run just %s times' % counter)


def do_diff(jack_files):
    for file in jack_files:
        xml_res = file[:-4] + 'xml'
        xml_sor = xml_res.replace('Tests', 'Expected')
        print('diff %s:' % file)
        print(os.system('diff %s ' % xml_res + xml_sor + '\n'))


if __name__ == '__main__':
    files = run_over_dir(os.getcwd() + '/Tests')
    execute(files)
    do_diff(files)