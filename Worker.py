class Worker:
    def __init__(self, file, tokens):
        self.__file = file
        self.tokens = tokens
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec}
        start = next(tokens)
        foo = self.types[start[1]]
        foo(tokens)

    def compile_class(self, tokens):
        self.__file.write('<lass>\n')
        next_token = next(tokens)
        self.compile_class_name(tokens, next_token[0], 1)
        next_token = next(tokens)
        foo = self.types[next_token[1]]
        foo(tokens, next_token[0], 1)  # the open {
        next_token = next(tokens)
        foo = self.types[next_token[1]]
        foo(tokens, next_token[0], 1)
        #
        self.__file.write('</class>')

    def compile_subroutine_declaration(self, tokens, indentation=0):
        pass

    def compile_parameter_list(self, tokens, indentation=0):
        pass

    def compile_subroutine_body(self, tokens, indentation=0):
        pass

    def compile_class_var_dec(self, tokens, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<classVarDec>\n')
        indentation += 1
        self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # static / field
        keyword = next(tokens)[0]
        self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # type
        keyword = next(tokens)[0]
        while keyword != ';':
            if keyword == ',':
                self.compile_symbol(tokens, keyword, indentation)
            else:
                self.__file.write('\t' * indentation + '<identifier> ' + keyword + ' </identifier>\n')
            keyword = next(tokens)[0]
        indentation -= 1
        self.__file.write('\t' * indentation + '</classVarDec>\n')

    def compile_class_name(self, tokens, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<identifier> ' + keyword + ' </identifier>\n')

    def compile_subroutine_name(self, tokens, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<subroutineDec>\n')
        indentation += 1
        while keyword != '}':  # each iteration is one subroutine
            self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # static / field
            keyword = next(tokens)[0]
            self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # const / func / method
            keyword = next(tokens)[0]
            self.__file.write('\t' * indentation + '<identifier> ' + keyword + ' </identifier>\n')  # name
            keyword = next(tokens)[0]

        indentation -= 1
        self.__file.write('\t' * indentation + '</subroutineDec>\n')

    def compile_statements(self, tokens, indentation=0):
        pass

    def compile_statement(self, tokens, indentation=0):
        pass

    def compile_let_statement(self, tokens, indentation=0):
        pass

    def compile_if_statement(self, tokens, indentation=0):
        pass

    def compile_while_statement(self, tokens, indentation=0):
        pass

    def compile_do_statement(self, tokens, indentation=0):
        pass

    def compile_return_statement(self, tokens, indentation=0):
        pass

    def compile_expression(self, tokens, indentation=0):
        pass

    def compile_term(self, tokens, indentation=0):
        pass

    def compile_subroutine_call(self, tokens, indentation=0):
        pass

    def compile_expression_list(self, tokens, indentation=0):
        pass

    def compile_op(self, tokens, indentation=0):
        pass

    def compile_unary_op(self, tokens, indentation=0):
        pass

    def compile_keyword_constant(self, tokens, indentation=0):
        pass

    def compile_symbol(self, tokens, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<symbol> ' + keyword + ' </symbol>\n')


a = iter([('class', 'class'), ('Main', 'identifier'), ('{', 'symbol'), ('static', 'classVarDec'), ('int', 'type'),
          ('a', 'identifier'), (',', 'symbol'), ('b', 'identifier'), (';', 'symbol'), ('}', 'symbol')])
f = open('/home/david/Downloads/res', 'w')
worker = Worker(f, a)
