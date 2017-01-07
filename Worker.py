class Worker:
    def __init__(self, tokens):
        self.dbg = True
        self.tokens = tokens
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec}
        self.lines = list()

    def to_xml(self, path):
        foo = self.tokens.pop[0]
        foo()
        xml_file = open(path, 'w')
        for line in self.lines:
            xml_file.write(line)
        xml_file.close()

    def compile_class(self):
        self.lines.append('<class>\n')
        self.compile_identifier(1)  # class name
        next_token = self.tokens.pop()
        foo = self.types[next_token[1]]
        foo(self.tokens, next_token[0], 1)  # the open {
        next_token = self.tokens.pop()
        foo = self.types[next_token[1]]
        foo(self.tokens, next_token[0], 1)
        # run code
        self.compile_symbol()  # end
        self.lines.append('</class>')

    def compile_parameter_list(self, indentation=0):
        pass

    def compile_class_var_dec(self, indentation=0):
        self.lines.append('\t' * indentation + '<classVarDec>\n')
        indentation += 1
        self.compile_keyword_constant(indentation)  # static / field
        self.compile_keyword_constant(indentation)  # type
        keyword = self.tokens[-1][0]
        while keyword != ';':
            if keyword == ',':
                self.compile_symbol(indentation)
            else:
                self.compile_identifier(keyword)
        self.compile_symbol(indentation)
        indentation -= 1
        self.lines.append('\t' * indentation + '</classVarDec>\n')

    def compile_subroutine_dec(self, indentation=0):
        self.lines.append('\t' * indentation + '<subroutineDec>\n')
        indentation += 1
        self.compile_keyword_constant(indentation)  # static / field
        self.compile_keyword_constant(indentation)  # const / func / method
        self.compile_identifier(indentation)  # name
        self.compile_symbol(indentation)
        self.compile_parameter_list(indentation)
        self.compile_symbol(indentation)

        indentation -= 1
        self.lines.append('\t' * indentation + '</subroutineDec>\n')

    def compile_statements(self, indentation=0):
        pass

    def compile_statement(self, indentation=0):
        pass

    def compile_let_statement(self, indentation=0):
        pass

    def compile_if_statement(self, indentation=0):
        pass

    def compile_while_statement(self, indentation=0):
        pass

    def compile_do_statement(self, indentation=0):
        pass

    def compile_return_statement(self, indentation=0):
        pass

    def compile_expression(self, indentation=0):
        pass

    def compile_term(self, indentation=0):
        pass

    def compile_subroutine_call(self, indentation=0):
        keyword = self.tokens[-1]
        if keyword[0] == 'let':
            self.compile_let(indentation)

    def compile_let(self, indentation=0):
        pass

    def compile_expression_list(self, indentation=0):
        self.compile_symbol(indentation)  # (
        keyword = self.tokens[-1]
        while keyword[0] != ')':
            self.compile_expression(indentation)
            keyword = self.tokens[-1]
            self.compile_symbol(indentation)

    def compile_op(self, indentation=0):
        self.compile_term(indentation)
        self.compile_symbol(indentation)
        self.compile_term(indentation)

    def compile_unary_op(self, indentation=0):
        self.compile_symbol(indentation)
        self.compile_term(indentation)

    def compile_keyword_constant(self, indentation=0):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'keyword':
                print(str(keyword) + " != keyword")
        self.lines.append('\t' * indentation + '<keyword> ' + keyword[0] + ' </keyword>\n')

    def compile_symbol(self, indentation=0):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'symbol':
                print(str(keyword) + " != symbol")
        self.__file.write('\t' * indentation + '<symbol> ' + keyword[0] + ' </symbol>\n')

    def compile_identifier(self, indentation=0):
        keyword = self.tokens.pop()
        if self.dbg:
            if keyword[1] != 'identifier':
                print(str(keyword) + " != identifier")
        self.lines.append('\t' * indentation + '<identifier> ' + keyword[0] + ' </identifier>\n')

    def writeLine(self, tag, keyword, indentation):
        return '%s<%s> %s </%s>' % ('\t' * indentation, tag, keyword[0], tag)

    def writeSingle(self, tag, indent, toOpen=True):
        if toOpen:
            return '%s<%s>' % ('\t' * indent, tag)
        else:
            return '%s</%s>' % ('\t' * indent, tag)


if __name__ == '__main__':
    a = iter([('class', 'class'), ('Main', 'identifier'), ('{', 'symbol'), ('static', 'classVarDec'), ('int', 'type'),
              ('a', 'identifier'), (',', 'symbol'), ('b', 'identifier'), (';', 'symbol'), ('}', 'symbol')])
    f = open('/home/david/Downloads/res', 'w')
    worker = Worker(f, a)
