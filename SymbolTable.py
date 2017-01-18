class SymbolTable:
    def __init__(self):
        self.subroutines = []
        self.subroutines.append(dict())  # This for the class variables
        self.vars = {
            'static': {},
            'arg': {},
            'field': {},
            'var': {}
        }

    def start_subroutine(self):
        self.subroutines.append(dict())

    def end_subroutine(self):
        self.vars['var'] = {}
        self.vars['arg'] = {}
        self.subroutines.pop()

    # adding new variables to our containe
    # it can be static|field|var type name(,name)*
    # or type and name one after another
    def define(self, statement):
        if (statement[0] not in ['var', 'static', 'field']):
            statement = ['arg'] + statement
        if (not isinstance(statement[2], list)):
            print(statement)
            print('state number 2 is not a list, please check it out')
        for elem in statement[2]:
            self.insertNewVar(statement[0:2] + [elem])

    def insertNewVar(self, state):
        # cant override static var
        if state[0] == 'static' and state[2] in self.vars['static']:
            return None
        self.vars[state[0]][state[2]] = (state[1], len(self.vars[state[0]]))

    # return none if error
    # example for return: ['static','number','type']
    def get(self, name):
        if name in self.vars['static']:
            elem = self.vars['static'][name]
            return ['static', elem[1], elem[0]]
        elif name in self.vars['var']:
            elem = self.vars['var'][name]
            return ['local', elem[1], elem[0]]
        elif name in self.vars['arg']:
            elem = self.vars['arg'][name]
            return ['arg', elem[1], elem[0]]
        elif name in self.vars['field']:
            elem = self.vars['field'][name]
            return ['field', elem[1], elem[0]]
        return None
