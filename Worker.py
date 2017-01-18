from SymbolTable import SymbolTable
from VMWriter import VMWriter


class Worker:
    def __init__(self, tokens, path):  # todo match to the current ex
        self.writer = VMWriter(path)
        self.symbol_table = SymbolTable()
        self.dbg = True
        self.tokens = tokens[::-1]
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec, 'identifier': self.compile_identifier,
                      'subroutineDec': self.compile_subroutine_dec, 'keyword': self.compile_keyword_constant,
                      'type': self.compile_keyword_constant,
                      'op': self.compile_keyword_constant, 'unaryOp': self.compile_unary_op,
                      'StringConstant': self.compile_string_constant,
                      'whileStatement': self.compile_while_statement, 'integerConstant': self.compile_integer_constant,
                      'doStatement': self.compile_do_statement, 'ReturnStatement': self.compile_return_statement,
                      'varDec': self.compile_var_dec, 'letStatement': self.compile_let,
                      'ifStatement': self.compile_if_statement,
                      'KeywordConstant': self.compile_keyword_constant}
        self.statements = {'letStatement', 'ifStatement', 'ReturnStatement', 'whileStatement', 'doStatement'}
        self.lines = []
        self.popped = ['', '']
        self.indentation = 0
        self.path = path
        self.compile_class()
        self.to_xml()

    def to_xml(self):  # todo remove after done wrote the others function
        # print(self.path)
        xml_file = open(self.path, 'w')
        for line in self.lines:
            xml_file.write(line)
        xml_file.close()

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):  # todo change to this ex
        self.writeSingle('class')
        self.compile_keyword_constant()  # class name
        self.compile_identifier()  # class name
        self.untilBracket(inClass=True)
        self.writeSingle('class', False)

    # var' type varName (',' varName)* ';'
    def compile_var_dec(self):  # todo implement
        self.writeSingle('varDec')
        self.compile_keyword_constant()
        if self.next()[0] == 'Array':
            self.compile_identifier()
        else:
            self.compile_type()
        self.compile_identifier()
        if self.next()[0] == ',':
            while self.next()[0] == ',':
                self.compile_symbol()
                self.compile_identifier()
        self.compile_symbol()
        self.writeSingle('varDec', False)

    # ( (type varName) (',' type varName)*)?
    def compile_parameter_list(self):  # todo implement
        self.writeSingle('parameterList')
        if self.next()[0] == ')':
            return self.writeSingle('parameterList', False)
        self.compile_type()  # type
        self.compile_identifier()  # varName (first)
        while self.next()[0] == ',':
            self.compile_symbol()
            self.compile_type()
            self.compile_identifier()
        self.writeSingle('parameterList', False)

    # ('static' | 'field' ) type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        line = '%s %s %s' % (self.pop()[0], self.pop()[0], self.pop()[0])
        # self.writeSingle('classVarDec')
        # self.compile_keyword_constant()
        # self.compile_type()
        # self.compile_identifier()
        while self.next()[0] == ',':
            line += '%s %s' % (self.pop()[1], self.pop()[0])
            # self.compile_symbol()
            # self.compile_identifier()
        line += self.pop()[0]
        self.symbol_table.define(line)
        # self.compile_symbol()
        # self.writeSingle('classVarDec', False)

    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName
    # '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):  # todo implement
        self.writeSingle('subroutineDec')
        self.compile_keyword_constant()  # # const / func / method
        self.compile_type()
        self.compile_identifier()  # name
        self.compile_symbol()
        self.compile_parameter_list()
        self.compile_symbol()
        self.writeSingle('subroutineBody')
        self.untilBracket()
        self.writeSingle('subroutineBody', False)
        self.writeSingle('subroutineDec', False)

    def untilBracket(self, inClass=False):  # todo change to this ex
        self.compile_symbol()
        key = self.next()
        state_opened = False
        while key[0] != '}':
            if key[0] != 'var':
                if not inClass and not state_opened:
                    state_opened = True
                    self.writeSingle('statements')
            self.types[key[1]]()
            key = self.next()
        if not inClass and not state_opened:
            self.writeSingle('statements')
        if not inClass:
            self.writeSingle('statements', False)
        self.compile_symbol()

    def compile_statements(self, key):  # todo change to this ex
        self.writeSingle('statements')
        while key[1] in self.statements:
            self.types[key[1]]()
            key = self.next()
        self.writeSingle('statements', False)

    # if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compile_if_statement(self):  # todo change to this ex
        self.writeSingle('ifStatement')
        self.compile_keyword_constant()  # if
        self.compile_symbol()  # (
        self.compile_expression()  # expression
        self.compile_symbol()  # )
        self.untilBracket()
        if self.next()[0] == 'else':
            self.compile_keyword_constant()
            self.untilBracket()  # todo add the index of label
        self.writeSingle('ifStatement', False)

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while_statement(self):
        start = self.writer.generate_label(self.pop()[0])
        end = self.writer.generate_label('end_while')
        self.writer.write_label(start)
        self.pop()
        # self.writeSingle('whileStatement')
        # self.compile_keyword_constant()
        # self.compile_symbol()
        self.pop()
        self.compile_expression()
        self.writer.write_arithmetic('~')
        self.writer.write_if(end)
        # self.compile_symbol()
        self.untilBracket()
        self.writer.write_go_to(start)
        # self.writeSingle('whileStatement', False)
        self.writer.write_label(end)

    # 'do' subroutineCall ';'
    def compile_do_statement(self):  # todo change to this ex
        self.writeSingle('doStatement')
        self.compile_keyword_constant()
        self.compile_subroutine_call()
        self.compile_symbol()
        self.writeSingle('doStatement', False)

    # 'return' expression? ';'
    def compile_return_statement(self):
        # self.writeSingle('returnStatement')
        self.pop()
        # self.compile_keyword_constant()
        if self.next()[0] != ';':
            self.compile_expression()
        # self.compile_symbol()
        # self.writeSingle('returnStatement', False)
        self.pop()
        self.writer.write_return()

    # term (op term)*
    def compile_expression(self):  # todo change to this ex
        self.writeSingle('expression')
        self.compile_term()
        while self.next()[1] in ['op', 'unaryOp']:
            self.compile_op()
            self.compile_term()
        self.writeSingle('expression', False)

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):  # todo change to this ex
        self.writeSingle('term')
        if self.next()[1] in ['op', 'unaryOp']:
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
        if self.next()[0] == '[':
            self.compile_symbol()
            self.compile_expression()
            self.compile_symbol()
        self.writeSingle('term', False)

    def isNextSubRoutineCall(self):  # todo change to this ex -- if necessary
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

    def compile_subroutine_call(self):  # todo change to this ex
        self.compile_identifier()
        if self.next()[0] == '.':  # cass of expression
            self.compile_symbol()
            self.compile_identifier()
        self.compile_symbol()  # {
        self.compile_expression_list()
        self.compile_symbol()

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):  # todo change to this ex
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
    def compile_expression_list(self):  # todo change to this ex
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

    def compile_op(self):  # todo change to this ex
        self.compile_symbol()

    def compile_unary_op(self):  # todo change to this ex
        self.compile_symbol()

    def compile_keyword_constant(self):  # todo change to this ex
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'keyword':
                pass
        self.writeLine(keyword[0], 'keyword')

    def compile_symbol(self):  # todo change to this ex
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'symbol':
                pass
        self.writeLine(keyword[0], 'symbol')

    def compile_identifier(self):  # todo change to this ex
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'identifier':
                pass
        self.writeLine(keyword[0], 'identifier')

    def compile_type(self):  # todo change to this ex
        keyword = self.tokens.pop()
        var_type = 'keyword'
        if keyword[1] == 'identifier':
            var_type = 'identifier'
        self.writeLine(keyword[0], var_type)

    def compile_integer_constant(self):
        keyword = self.tokens.pop()
        self.writer.write_push('constant', int(keyword[0]))
        # self.writeLine(keyword[0], 'integerConstant')

    # don't pop the string to any location.
    def compile_string_constant(self):
        self.writer.write_call('String.new ', 1)
        keyword = self.tokens.pop()
        string = keyword[0]
        string = string.replace('\r', '\\r')
        for char in string:
            self.writer.write_push('constant', ord(char))
            self.writer.write_call('String.appendChar', 2)
            # self.writeLine(string[1:-1], 'stringConstant')

    def writeLine(self, keyword, tag):  # todo remove when done
        self.lines.append('%s<%s> %s </%s>\n' % ('  ' * self.indentation, tag, keyword, tag))

    def writeSingle(self, tag, toOpen=True):  # todo remove when done
        if toOpen:
            s = '%s<%s>\n' % ('  ' * self.indentation, tag)
            self.indentation += 1
            self.lines.append(s)
        else:
            self.lines.append('%s</%s>\n' % ('  ' * self.indentation, tag))

    def next(self):
        if len(self.tokens) == 0:
            self.to_xml()
            exit()
        return self.tokens[-1]

    def pop(self):
        if len(self.tokens) == 0:
            self.to_xml()
            exit()
        self.popped = self.tokens.pop()
        return self.popped

    def printLines(self):  # todo remove when done
        for i in range(len(self.lines) - 30, len(self.lines)):
            print(self.lines[i][:-1])
            self.indentation -= 1
