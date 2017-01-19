class VMWriter:
    def __init__(self, path):
        self.path = path
        self.lines = []
        self.labels = {}

    def write_push(self, segment, index):
        self.lines.append('push %s %s\n' % (segment, index))

    def write_pop(self, segment, index):
        self.lines.append('pop %s %s\n' % (segment, index))

    def write_arithmetic(self, command):
        self.lines.append('%s\n' % command)

    def generate_label(self, name):
        if name not in self.labels:
            self.labels[name] = 0
            return name + '0'
        else:
            self.labels[name] += 1
            temp = self.labels[name]
            return name + str(temp)

    def write_label(self, label):
        self.lines.append('label %s\n' % label)

    def write_go_to(self, label):
        self.lines.append('goto %s\n' % label)

    def write_if(self, label):
        self.lines.append('if-goto %s\n' % label)

    def write_call(self, name, n_args):
        a = 'call %s %s\n' % (name, n_args)
        self.lines.append('call %s %s\n' % (name, n_args))

    def write_function(self, name, n_locals):  # todo adding class name into print
        self.lines.append('function %s %s\n' % (name, n_locals))

    def write_return(self):
        self.lines.append('return\n')

    def close(self):
        vm_file = open(self.path, 'w')
        for line in self.lines:
            vm_file.write(line)
        vm_file.close()
