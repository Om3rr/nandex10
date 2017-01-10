class Worker:
    def __init__(self, tokens, path):
        self.dbg = True
        self.tokens = tokens[::-1]
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec, 'identifier': self.compile_identifier,
                      'subroutineDec': self.compile_subroutine_dec, 'keyword': self.compile_keyword_constant,
                      'type': self.compile_keyword_constant,
                      'op': self.compile_keyword_constant, 'unaryOp': self.compile_keyword_constant,
                      'StringConstant': self.compile_string_constant,
                      'whileStatement': self.compile_while_statement, 'integerConstant': self.compile_integer_constant,
                      'doStatement': self.compile_do_statement, 'ReturnStatement': self.compile_return_statement,
                      'varDec': self.compile_var_dec, 'letStatement': self.compile_let,
                      'ifStatement': self.compile_if_statement,
                      'KeywordConstant': self.compile_keyword_constant}
        self.statements = {'letStatement', 'ifStatement', 'ReturnStatement', 'whileStatement', 'doStatement'}
        self.lines = []
        self.indentation = 0
        self.path = path
        self.compile_class()
        self.to_xml()

    def to_xml(self):
        print(self.path)
        xml_file = open(self.path, 'w')
        for line in self.lines:
            xml_file.write(line)
        xml_file.close()

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        # print(self.tokens[::-1])
        self.writeSingle('class')
        self.compile_keyword_constant()  # class name
        self.compile_identifier()  # class name
        self.untilBracket()
        self.writeSingle('class', False)

    # var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.writeSingle('varDec')
        self.compile_keyword_constant()
        if self.next()[0] == 'Array':
            self.compile_identifier()
        else:
            self.compile_keyword_constant()
        self.compile_identifier()
        if self.next()[0] == ',':
            while self.next()[0] == ',':
                self.compile_symbol()
                self.compile_identifier()
        self.compile_symbol()
        self.writeSingle('varDec', False)

    # ( (type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        self.writeSingle('parameterList')
        if self.next()[0] == ')':
            return self.writeSingle('parameterList', False)
        self.compile_identifier()  # type
        self.compile_identifier()  # varName (first)
        while self.next()[0] == ',':
            self.compile_symbol()
            self.compile_identifier()
            self.compile_identifier()
        self.writeSingle('parameterList', False)

    # ('static' | 'field' ) type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        self.writeSingle('classVarDec')
        self.compile_keyword_constant()
        self.compile_identifier()
        self.compile_identifier()
        while self.next()[0] == ',':
            self.compile_symbol()
            self.compile_identifier()
        self.compile_symbol()
        self.writeSingle('classVarDec', False)

    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName
    # '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):
        self.writeSingle('subroutineDec')
        self.compile_keyword_constant()  # # const / func / method
        self.compile_keyword_constant()  # static / field
        self.compile_identifier()  # name
        self.compile_symbol()
        self.compile_parameter_list()
        self.compile_symbol()
        self.writeSingle('subroutineBody')
        self.untilBracket()
        self.writeSingle('subroutineBody', False)
        self.writeSingle('subroutineDec', False)

    def untilBracket(self):
        self.compile_symbol()
        key = self.next()
        while key[0] != '}':
            print(key)
            if key[1] in self.statements:
                self.compile_statements(key)
            else:
                self.types[key[1]]()
            key = self.next()
        self.compile_symbol()

    def compile_statements(self, key):
        self.writeSingle('statements')
        while key[1] in self.statements:
            self.types[key[1]]()
            key = self.next()
        self.writeSingle('statements', False)

    # if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compile_if_statement(self):
        self.writeSingle('ifStatement')
        self.compile_keyword_constant()
        self.compile_symbol()
        self.compile_expression()
        self.compile_symbol()
        self.untilBracket()
        if self.next()[0] == 'else':
            self.untilBracket()
        self.writeSingle('ifStatement', False)

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while_statement(self):
        self.writeSingle('whileStatement')
        self.compile_keyword_constant()
        self.compile_symbol()
        self.compile_expression()
        self.compile_symbol()
        self.untilBracket()
        self.writeSingle('whileStatement', False)

    # 'do' subroutineCall ';'
    def compile_do_statement(self):
        self.writeSingle('doStatement')
        self.compile_keyword_constant()
        self.compile_subroutine_call()
        self.compile_symbol()
        self.writeSingle('doStatement', False)

    # 'return' expression? ';'
    def compile_return_statement(self):
        self.writeSingle('returnStatement')
        self.compile_keyword_constant()
        if self.next()[0] != ';':
            self.compile_expression()
        self.compile_symbol()
        self.writeSingle('returnStatement', False)

    # term (op term)*
    def compile_expression(self):  # todo should support expressionList case
        self.writeSingle('expression')
        self.compile_term()
        while self.next()[1] in ['op', 'unaryOp']:
            self.compile_op()
            self.compile_term()
        self.writeSingle('expression', False)

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        self.writeSingle('term')
        if self.next()[1] == 'unaryOp':
            self.compile_symbol()
            self.compile_term()
            return self.writeSingle('term', False)
        if self.isNextSubRoutineCall():
            self.compile_subroutine_call()
            self.writeSingle('term', False)
            return
        if self.next()[0] == '(':
            self.compile_symbol()
            self.compile_expression()
            self.compile_symbol()
            self.writeSingle('term', False)
            return
        self.types[self.next()[1]]()
        # a = self.next()
        # if self.next()[1] == 'integerConstant':
        #     self.
        # self.compile_identifier()
        if self.next()[0] == '[':
            self.compile_symbol()
            self.compile_expression()
            self.compile_symbol()
        self.writeSingle('term', False)

    def isNextSubRoutineCall(self):
        import re
        reg = re.compile('[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_][A-Za-z_0-9]*)|(\()')
        l = self.tokens[::-1]
        l = l[0:3]
        s = ""
        for elem in l:
            s += "%s" % elem[0]
        m = reg.match(s)
        if not m:
            return False
        if m.start(0) == 0 and m.end(0) == len(s):
            return True
        return False

        # subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName'(' expressionList ')'
        #

    def compile_subroutine_call(self):
        self.compile_identifier()
        if self.next()[0] == '.':  # cass of expression
            self.compile_symbol()
            self.compile_identifier()
        self.compile_symbol()
        self.compile_expression_list()
        self.compile_symbol()

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        self.writeSingle('letStatement')
        self.compile_keyword_constant()
        self.compile_identifier()

        if self.next()[0] == '[':
            self.compile_symbol()
            self.compile_expression()
            self.compile_symbol()
        self.compile_symbol()  # =
        self.compile_expression()
        self.compile_symbol()  # ;
        self.writeSingle('letStatement', False)

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        self.writeSingle('expressionList')
        first = True
        while self.next()[0] != ')':
            if not first:
                self.compile_symbol()
                self.compile_expression()
            else:
                self.compile_expression()
                first = False
        self.writeSingle('expressionList', False)

    def compile_op(self):
        self.compile_symbol()

    def compile_unary_op(self):
        self.compile_symbol()
        self.compile_term()

    def compile_keyword_constant(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'keyword':
                # print(str(keyword) + " != keyword")
                pass
        self.writeLine(keyword[0], 'keyword')

    def compile_symbol(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'symbol':
                # print(str(keyword) + " != symbol")
                pass
        self.writeLine(keyword[0], 'symbol')

    def compile_identifier(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'identifier':
                pass
                # print(str(keyword) + " != identifier")
        self.writeLine(keyword[0], 'identifier')

    def compile_integer_constant(self):
        keyword = self.tokens.pop()
        self.writeLine(keyword[0], 'integerConstant')

    def compile_string_constant(self):
        keyword = self.tokens.pop()
        self.writeLine(keyword[0], 'stringConstant')

    def writeLine(self, keyword, tag):
        # self.counter += 2
        self.lines.append('%s<%s> %s </%s>\n' % ('  ' * self.indentation, tag, keyword, tag))

    def writeSingle(self, tag, toOpen=True):
        if toOpen:
            s = '%s<%s>\n' % ('  ' * self.indentation, tag)
            self.indentation += 1
            self.lines.append(s)
        else:
            self.indentation -= 1
            self.lines.append('%s</%s>\n' % ('  ' * self.indentation, tag))

    def next(self):
        if len(self.tokens) == 0:
            print('tokens are empty')
            self.printLines()
            exit()
        return self.tokens[-1]

    def pop(self):
        if len(self.tokens) == 0:
            print('tokens are empty')
            self.printLines()
            exit()
        return self.tokens.pop()

    def printLines(self):
        for i in range(len(self.lines) - 10, len(self.lines)):
            print(self.lines[i][:-1])


            # if __name__ == '__main__':
        #     f = open('etc/Square/SquareGame.jack', 'r')
        #     reader = f.read()
        #     p = Parser(reader)
        #     path = 'etc/writing.xml'
        #     print(p.meal[0:10])
        #     worker = Worker(p.meal, path)
        #     exit()

            # import os
            #
            # d = os.listdir('etc')
            # for elem in d:
            #     if os.path.isdir(os.path.join('etc', elem)):
            #         dir = os.path.join('etc', elem)
            #         for file in os.listdir(dir):
            #             if file.endswith(".jack"):
            #                 print(dir, file)
            #                 f = open(os.path.join(dir, file), 'r')
            #                 reader = f.read()
            #                 p = Parser(reader)
            #                 path = 'etc/writing.xml'
            #                 print(p.meal[0:10])
            #                 worker = Worker(p.meal, path)
