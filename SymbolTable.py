import re
class SymbolTable:
    def __init__(self):
        self.subroutines = list()
        self.subroutines.append(dict())  # This for the class variables

    def start_subroutine(self):
        self.subroutines.append(dict())

    def end_subroutine(self):
        self.subroutines.pop()

    # adding new variables to our containe
    # it can be static|field|var type name(,name)*
    # or type and name one after another
    def define(self, statement):
        if(statement[0] not in ['var','static','field']):
            statement = ['arg'] + statement
        for elem in statement[2]:
            self.insertNewVar(statement[0:2]+[elem])



    def insertNewVar(self,state):
        print('cool, i got: ')
        print(state)


    # return none if error
    def get(self, name):
        pass


sym = SymbolTable()
sym.define(['int',['a','b','c']])
