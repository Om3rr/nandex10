from SymbolTable import SymbolTable
from VMWriter import VMWriter

arithmetic = {'+': 'add', '-': 'sub', '*': 'call Math.multiply 2', '/': 'call Math.divide 2', '&': 'and', '|': 'or',
              '<': 'lt', '>': 'gt', '=': 'eq'}
keyword_words = {'true', 'false', 'null'}
unary_op = {'~': 'not', '-': 'neg'}


class Worker:
    def __init__(self, tokens, path):
        self.writer = VMWriter(path)
        self.class_name = ''
        self.symbol_table = SymbolTable()
        # self.dbg = True
        self.tokens = tokens[::-1]
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec, 'identifier': self.compile_identifier,
                      'subroutineDec': self.compile_subroutine_dec, 'keyword': self.compile_keyword_constant,
                      'op': self.compile_keyword_constant, 'unaryOp': self.compile_unary_op,
                      'StringConstant': self.compile_string_constant,
                      'whileStatement': self.compile_while_statement, 'integerConstant': self.compile_integer_constant,
                      'doStatement': self.compile_do_statement, 'ReturnStatement': self.compile_return_statement,
                      'varDec': self.compile_var_dec, 'letStatement': self.compile_let,
                      'ifStatement': self.compile_if_statement,
                      'KeywordConstant': self.compile_keyword_constant}
        self.statements = {'letStatement', 'ifStatement', 'ReturnStatement', 'whileStatement', 'doStatement'}
        self.popped = ['', '']
        self.compile_class()

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.pop()
        self.class_name = self.pop()[0]
        self.untilBracket(inClass=True)
        return self.writer.close()

    # var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        variables = list()
        variables.append(self.pop()[0])
        variables.append(self.pop()[0])
        variables.append(list())
        variables[2].append(self.pop()[0])
        if self.next()[0] == ',':
            while self.next()[0] == ',':
                self.pop()
                variables[2].append(self.pop()[0])
        return self.symbol_table.define(variables)

    # ( (type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        if self.next()[0] == ')':
            return
        variables = [None, [None]]
        variables[0] = self.pop()[0]
        variables[1][0] = (self.pop()[0])
        self.symbol_table.define(variables)
        while self.next()[0] == ',':
            self.pop()
            variables[0] = self.pop()[0]
            variables[1][0] = (self.pop()[0])
            self.symbol_table.define(variables)
        return

    # ('static' | 'field' ) type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        variables = list()
        variables.append(self.pop()[0])
        variables.append(self.pop()[0])
        variables.append(list())
        variables[2].append(self.pop()[0])
        while self.next()[0] == ',':
            self.pop()
            variables[2].append(self.pop()[0])
        return self.symbol_table.define(variables)

    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName
    # '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):
        function = self.pop()[0]
        self.pop()
        name = '%s.%s' % (self.class_name, self.pop()[0])
        counter = self.counter_local_variables()
        self.writer.write_function(name, counter)
        if function == 'constructor':
            self.writer.write_push('constant', len(self.symbol_table.vars['field']))
            self.writer.write_call('Memory.alloc', 1)
            self.writer.write_pop('pointer', 0)
        elif function == 'method':
            self.writer.write_push('argument', 0)
            self.writer.write_pop('pointer', 0)
            self.symbol_table.define(['int',['this#1231359123102405aisjdfijasdifjaisdjfiasjdifjasdgjasdnfaisdnfaisdnfasidfnasidfnasd']])
        self.pop()
        self.compile_parameter_list()
        self.pop()
        self.untilBracket()
        return self.symbol_table.end_subroutine()

    def untilBracket(self, inClass=False):
        self.pop()
        key = self.next()
        state_opened = False
        while key[0] != '}':
            if key[0] != 'var':
                if not inClass and not state_opened:
                    state_opened = True
            self.types[key[1]]()
            key = self.next()
        return self.pop()

    def compile_statements(self, key):
        while key[1] in self.statements:
            self.types[key[1]]()
            key = self.next()
        return

    # if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compile_if_statement(self):
        else_case = self.writer.generate_label('IF_FALSE')
        end = self.writer.generate_label('IF_END')
        self.pop()
        self.pop()
        self.compile_expression()  # expression
        self.writer.write_arithmetic('not')
        self.writer.write_if(else_case)
        self.pop()
        self.untilBracket()
        if self.next()[0] == 'else':
            self.writer.write_go_to(end)
            self.writer.write_label(else_case)
            self.pop()
            self.untilBracket()
            self.writer.write_label(end)
            return
        return self.writer.write_label(else_case)

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while_statement(self):
        self.pop()
        start = self.writer.generate_label('WHILE_EXP')
        end = self.writer.generate_label('WHILE_END')
        self.writer.write_label(start)
        self.pop()
        # self.compile_keyword_constant()
        # self.compile_symbol()
        # self.pop()
        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.writer.write_if(end)
        self.pop()
        # self.compile_symbol()
        self.untilBracket()
        self.writer.write_go_to(start)
        return self.writer.write_label(end)

    # 'do' subroutineCall ';'
    def compile_do_statement(self):
        self.pop()
        self.compile_subroutine_call()
        self.pop()
        return self.writer.write_pop('temp', 0)

    # 'return' expression? ';'
    def compile_return_statement(self):
        self.pop()
        # self.compile_keyword_constant()
        if self.next()[0] == 'this':
            self.writer.write_push('pointer', 0)
        elif self.next()[0] != ';':
            self.compile_expression()
        else:
            self.writer.write_push('constant', 0)
        self.pop()
        return self.writer.write_return()


    # term (op term)*
    def compile_expression(self):
        self.compile_term()
        while self.next()[1] in ['op', 'unaryOp']:
            temp = self.compile_op()
            self.compile_term()
            self.writer.write_arithmetic(temp)

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        print(self.tokens[-5:])
        if self.next()[1] in ['op', 'unaryOp']:
            temp = self.pop()[0]
            self.compile_term()
            self.writer.write_arithmetic(unary_op[temp])
            return
        if self.isNextSubRoutineCall():
            return self.compile_subroutine_call()
        if self.next()[0] == '(':
            self.pop()
            self.compile_expression()
            return self.pop()
        symbol = self.symbol_table.get(self.next()[0])
        # if not symbol or symbol[2] != 'Array' or self.tokens[-2][0] != '[':
        if not symbol or  self.tokens[-2][0] != '[':
            self.types[self.next()[1]]()
        else:
            self.pop()
        if self.next()[0] == '[':
            self.pop()
            self.compile_expression()
            self.pop()
            self.writer.write_push(symbol[0], symbol[1])
            self.writer.write_arithmetic('add')
            self.writer.write_pop('pointer', 1)
            self.writer.write_push('that', 0)
        return

    def isNextSubRoutineCall(self):
        import re
        reg = re.compile('[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_][A-Za-z_0-9]*)|([A-Za-z_][A-Za-z_0-9]*\()')
        l = self.tokens[::-1]
        l = l[0:3]
        s = ""
        for elem in l:
            s += "%s" % elem[0]
        m = reg.match(s)
        if not m:
            return False
        if m.start(0) == 0:
            return True
        return False

        # subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName'(' expressionList ')'
        #

    def compile_subroutine_call(self):
        subroutine = self.pop()[0]
        variable = self.symbol_table.get(subroutine)
        is_method = variable is not None
        count = 0
        if self.next()[0] == '.':  # cass of expression
            name = subroutine + '%s%s' % (self.pop()[0], self.pop()[0])
        else:
            name = '%s.%s' % (self.class_name, subroutine)
            self.writer.write_push('pointer', 0)
            count += 1
        self.pop()
        count += self.counter_variables()
        if is_method:
            count += 1
            self.writer.write_push(variable[0], variable[1])
            name = name.replace(subroutine, variable[2])
        self.compile_expression_list()
        self.pop()
        return self.writer.write_call(name, count)


    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        isArray = False
        self.pop()
        symbol = self.symbol_table.get(self.pop()[0])
        if self.next()[0] == '[':
            isArray = True
            self.pop()  # [
            self.compile_expression()  # expression
            self.pop()  # ]
            self.writer.write_push(symbol[0], symbol[1])
            self.writer.write_arithmetic('add')
        self.pop()
        self.compile_expression()
        if isArray:
            self.writer.write_pop('temp', 0)
            self.writer.write_pop('pointer', 1)
            self.writer.write_push('temp', 0)
            self.writer.write_pop('that', 0)
        else:
            self.writer.write_pop(symbol[0], symbol[1])

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        first = True
        while self.next()[0] != ')':
            if not first:
                self.pop()
                self.compile_expression()
            else:
                self.compile_expression()
                first = False

    def compile_op(self):
        keyword = self.pop()
        return arithmetic[keyword[0]]

    def compile_unary_op(self):
        keyword = self.pop()
        if keyword[0] == '-':
            self.writer.write_arithmetic('neg')
        self.writer.write_arithmetic('not')

    def compile_keyword_constant(self):
        keyword = self.tokens.pop()
        if keyword[0] == 'this':
            return self.writer.write_push('pointer', 0)
        # value = keyword_words.get(keyword[0])
        # if value is not None:
        if keyword[0] in keyword_words:
            self.writer.write_push('constant', 0)
            if keyword[0] == 'true':
                self.writer.write_arithmetic('not')
        else:
            self.writer.write_push('local', 0)

    def compile_symbol(self):
        keyword = self.pop()
        if keyword[0] in {'<', '>', '=='}:
            self.writer.write_arithmetic(keyword[0])

    def compile_identifier(self):
        symbol = self.symbol_table.get(self.next()[0])
        if not symbol:
            self.compile_subroutine_call()
        else:
            self.pop()
            self.writer.write_push(symbol[0], symbol[1])

    def compile_integer_constant(self):
        keyword = self.tokens.pop()
        self.writer.write_push('constant', int(keyword[0]))

    # don't pop the string to any location.
    def compile_string_constant(self):
        keyword = self.tokens.pop()
        string = keyword[0][1:-1]
        string = string.replace('\r', '\\r')
        string = string.replace('\t', '\\t')
        string = string.replace('\b', '\\b')
        string = string.replace('\n', '\\n')
        string = string.replace('\'', '\\')
        string = string.replace('\f', '\\f')
        string = string.replace('\v', '\\v')
        string = string.replace('\0', '\\0')
        self.writer.write_push('constant', len(string))
        self.writer.write_call('String.new', 1)
        for char in string:
            self.writer.write_push('constant', ord(char))
            self.writer.write_call('String.appendChar', 2)

    def next(self):
        if len(self.tokens) == 0:
            exit()
        return self.tokens[-1]

    def pop(self):
        if len(self.tokens) == 0:
            exit()
        self.popped = self.tokens.pop()
        return self.popped

    def counter_variables(self):
        index = len(self.tokens) - 1
        in_parentheses = False
        counter = 0 if self.tokens[index][0] == ')' else 1
        while self.tokens[index][0] != ')':
            if self.tokens[index][0] == ',':
                counter += 1
            elif self.tokens[index][0] == '(':
                while self.tokens[index][0] != ')':
                    index -= 1
            index -= 1
        return counter

    def counter_local_variables(self):
        index = len(self.tokens) - 1
        while self.tokens[index][0] != 'var':
            if self.tokens[index][0] == 'return':
                return 0
            index -= 1
        local_variables = 0
        while self.tokens[index][0] == 'var':
            index -= 3
            local_variables += 1
            while self.tokens[index][0] == ',':
                local_variables += 1
                index -= 2
            index -= 1
        return local_variables
