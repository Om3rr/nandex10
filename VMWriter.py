class VMWriter:

    def __init__(self, path):
        self.path = path
        self.lines = []
        self.labels = {}

    def write_push(self, segment, index):
        self.lines.append('\tpush %s %s\n' % (segment, index))

    def write_pop(self, segment, index):
        self.lines.append('\tpop %s %s\n' %(segment, index))

    def write_arithmetic(self, command):
        self.lines.append('\t%s\n' % command)

    def generate_label(self, name):
        if(name not in self.labels):
            self.labels[name] = 1
            return name+'1'
        else:
            temp = self.labels[name]
            self.labels[name] += 1
            return name+str(temp)

    def write_label(self, label):
        self.lines.append('label %s\n' % label)

    def write_go_to(self, label):
        self.lines.append('\tgoto %s\n' % label)

    def write_if(self, label):
        self.lines.append('\tif-goto %s\n' % label)

    def write_call(self, name, n_args):
        self.lines.append('\tcall %s %d\n' %(name,n_args))

    def write_function(self, name, n_locals):
        self.lines.append('\tfunction %s %s\n' %(name, n_locals))

    def write_return(self):
        self.lines.append('\treturn\n')

    def close(self):
        vm_file = open(self.path, 'w')
        for line in self.lines:
            vm_file.write(line)
        vm_file.close()
