from Parser import Parser
class Worker:
    def __init__(self, tokens, path):
        self.dbg = True
        self.tokens = tokens[::-1]
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec, 'identifier': self.compile_identifier,
                      'subroutineDec':self.compile_subroutine_dec, 'keyword':self.compile_keyword_constant, 'type':self.compile_keyword_constant,
                      'op':self.compile_op, 'unaryOp':self.compile_unary_op, 'StringConstant':self.compile_term}
        self.lines = []
        self.ident = 0
        self.path = path
        self.compile_class()
        self.to_xml()


    def to_xml(self):
        xml_file = open(self.path, 'w')
        for line in self.lines:
            xml_file.write(line)
        xml_file.close()

    def compile_class(self):
        print(self.tokens[::-1])
        self.writeSingle('class')
        self.compile_identifier()  # class name
        self.compile_identifier()  # class name
        self.untilBracket()
        self.writeSingle('class',False)

    def compile_parameter_list(self):
        pass

    def compile_class_var_dec(self):
        self.writeSingle('classVarDec')
        self.ident += 1
        self.compile_keyword_constant()  # static / field
        self.compile_keyword_constant()  # type
        keyword = self.next()[0]
        while keyword != ';':
            if keyword == ',':
                self.compile_symbol()
            else:
                self.compile_identifier()
        self.compile_symbol()
        self.writeSingle('classVarDec',False)

    def compile_subroutine_dec(self):
        self.writeSingle('subroutineDec')
        self.compile_keyword_constant()  # static / field
        self.compile_keyword_constant()  # const / func / method
        self.compile_identifier()  # name
        self.compile_symbol()
        self.compile_parameter_list()
        self.compile_symbol()
        self.untilBracket()
        self.writeSingle('subroutineDec', False)

    def untilBracket(self):
        self.compile_symbol()
        key = self.next()
        while(key[0] != '}'):
            self.types[key[1]]()
            key = self.next()
        self.compile_symbol()

    def compile_statements(self):
        pass

    def compile_statement(self):
        pass

    def compile_let_statement(self):
        pass

    def compile_if_statement(self):
        pass

    def compile_while_statement(self):
        pass

    def compile_do_statement(self):
        pass

    def compile_return_statement(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        self.pop()

    def compile_subroutine_call(self):
        keyword = self.tokens[-1]
        if keyword[0] == 'let':
            self.compile_let()

    def compile_let(self):
        pass

    def compile_expression_list(self):
        self.compile_symbol()  # (
        keyword = self.tokens[-1]
        while keyword[0] != ')':
            self.compile_expression()
            keyword = self.tokens[-1]
            self.compile_symbol()

    def compile_op(self):
        self.compile_term()
        self.compile_symbol()
        self.compile_term()

    def compile_unary_op(self):
        self.compile_symbol()
        self.compile_term()

    def compile_keyword_constant(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'keyword':
                print(str(keyword) + " != keyword")
        self.writeLine(keyword[0], keyword[1])

    def compile_symbol(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'symbol':
                print(str(keyword) + " != symbol")
        self.writeLine(keyword[0], keyword[1])

    def compile_identifier(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'identifier':
                print(str(keyword) + " != identifier")
        self.writeLine(keyword[0],keyword[1])

    def writeLine(self, keyword, tag):
        self.lines.append('%s<%s> %s </%s>\n' % ('\t' * self.ident, tag, keyword, tag))

    def writeSingle(self, tag, toOpen=True):
        if toOpen:
            s =  '%s<%s>\n' % ('\t' * self.ident, tag)
            self.ident += 1
            self.lines.append(s)
        else:
            self.ident -=1
            self.lines.append('%s</%s>\n' % ('\t' * self.ident, tag))

    def next(self):
        return self.tokens[-1]

    def pop(self):
        return self.tokens.pop()


if __name__ == '__main__':
    f = open('etc/ArrayTest/Main.jack', 'r')
    reader = f.read()
    p = Parser(reader)
    path = 'etc/writing.xml'
    worker = Worker(p.meal, path)
