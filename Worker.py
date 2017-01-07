from Parser import Parser
class Worker:
    def __init__(self, tokens, path):
        self.dbg = True
        self.tokens = tokens[::-1]
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec, 'identifier': self.compile_identifier}
        self.lines = []
        self.ident = 0
        self.compile_class()

    def to_xml(self):
        foo = self.tokens.pop[0]
        foo()
        xml_file = open(path, 'w')
        for line in self.lines:
            xml_file.write(line)
        xml_file.close()

    def compile_class(self):
        self.lines.append('<class>\n')
        self.ident+=1
        self.compile_identifier()  # class name
        self.compile_identifier()  # class name
        self.compile_symbol()  # class name
        foo = self.types[self.next()[1]]
        foo()  # the open {
        foo = self.types[self.next()[1]]
        foo()
        # run code
        self.compile_symbol()  # end
        self.lines.append('</class>')
        print(self.lines)

    def compile_parameter_list(self):
        pass

    def compile_class_var_dec(self):
        self.lines.append('\t' * self.ident + '<classVarDec>\n')
        self.ident += 1
        self.compile_keyword_constant(self.ident)  # static / field
        self.compile_keyword_constant(self.ident)  # type
        keyword = self.tokens[-1][0]
        while keyword != ';':
            if keyword == ',':
                self.compile_symbol()
            else:
                self.compile_identifier(keyword)
        self.compile_symbol()
        self.ident -= 1
        self.lines.append('\t' * self.ident + '</classVarDec>\n')

    def compile_subroutine_dec(self):
        self.lines.append('\t' * self.ident + '<subroutineDec>\n')
        self.ident += 1
        self.compile_keyword_constant()  # static / field
        self.compile_keyword_constant()  # const / func / method
        self.compile_identifier()  # name
        self.compile_symbol()
        self.compile_parameter_list()
        self.compile_symbol()

        self.ident -= 1
        self.lines.append('\t' * self.ident + '</subroutineDec>\n')

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
        pass

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
        self.lines.append('\t' * self.ident + '<keyword> ' + keyword[0] + ' </keyword>\n')

    def compile_symbol(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'symbol':
                print(str(keyword) + " != symbol")
        self.lines.append('\t' * self.ident + '<symbol> ' + keyword[0] + ' </symbol>\n')

    def compile_identifier(self):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'identifier':
                print(str(keyword) + " != identifier")
        self.lines.append('\t' * self.ident + '<identifier> ' + keyword[0] + ' </identifier>\n')

    def writeLine(self, tag, keyword):
        return '%s<%s> %s </%s>' % ('\t' * self.ident, tag, keyword[0], tag)

    def writeSingle(self, tag, indent, toOpen=True):
        if toOpen:
            return '%s<%s>' % ('\t' * indent, tag)
        else:
            return '%s</%s>' % ('\t' * indent, tag)

    def next(self):
        return self.tokens[-1]

    def pop(self):
        return self.tokens.pop()


if __name__ == '__main__':
    f = open('etc/test1.jack', 'r')
    reader = f.read()
    p = Parser(reader)
    path = 'etc/writing.xml'
    worker = Worker(p.meal, path)
