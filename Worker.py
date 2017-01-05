class Worker:
    def __init__(self, file, tokens):
        self.dbg = True
        self.__file = file
        self.tokens = tokens
        self.types = {'symbol': self.compile_symbol, 'class': self.compile_class,
                      'classVarDec': self.compile_class_var_dec}
        start = next(tokens)
        self.lines = list()
        foo = self.types[start[1]]
        foo()

    def compile_class(self, tokens):
        self.__file.write('<class>\n')
        next_token = self.tokens.pop()
        self.compile_class_name(self.tokens, next_token[0], 1)
        next_token = self.tokens.pop()
        foo = self.types[next_token[1]]
        foo(self.tokens, next_token[0], 1)  # the open {
        next_token = self.tokens.pop()
        foo = self.types[next_token[1]]
        foo(self.tokens, next_token[0], 1)
        #
        self.__file.write('</class>')

    def compile_parameter_list(self, indentation=0):
        pass

    def compile_class_var_dec(self, tokens, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<classVarDec>\n')
        indentation += 1
        self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # static / field
        keyword = self.tokens.pop()
        self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # type
        keyword = self.tokens.pop()
        while keyword != ';':
            if keyword == ',':
                self.compile_symbol(keyword, indentation)
            else:
                self.__file.write('\t' * indentation + '<identifier> ' + keyword + ' </identifier>\n')
            keyword = self.tokens.pop()
        self.compile_symbol(self.tokens.pop(), indentation)
        indentation -= 1
        self.__file.write('\t' * indentation + '</classVarDec>\n')

    def compile_class_name(self, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<identifier> ' + keyword + ' </identifier>\n')

    def compile_subroutine_dec(self, keyword, indentation=0):
        self.__file.write('\t' * indentation + '<subroutineDec>\n')
        indentation += 1
        self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # static / field
        keyword = next(self.tokens)[0]
        self.__file.write('\t' * indentation + '<keyword> ' + keyword + ' </keyword>\n')  # const / func / method
        keyword = next(self.tokens)[0]
        self.__file.write('\t' * indentation + '<identifier> ' + keyword + ' </identifier>\n')  # name
        self.compile_symbol(self.tokens,indentation)
        self.compile_parameter_list(indentation)
        self.compile_symbol(next(self.tokens)[0])

        indentation -= 1
        self.__file.write('\t' * indentation + '</subroutineDec>\n')

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
        pass

    def compile_expression_list(self, keyword, indentation=0):
        self.compile_symbol(keyword,indentation)
        keyword = self.tokens.pop()[0]
        while(keyword != ','):
            self.compile_expression(keyword, indentation)
            keyword = self.tokens.pop()[0]
        self.compile_symbol(keyword, indentation)

    def compile_op(self, indentation=0):
        self.compile_term(indentation)
        self.compile_symbol(indentation)
        self.compile_term(indentation)

    def compile_unary_op(self, indentation=0):
        self.compile_symbol(indentation)
        self.compile_term(indentation)

    def compile_keyword_constant(self, indentation=0):
        keyword = self.tokens.pop()
        if (self.dbg):
            if (keyword[1] != 'symbol'):
                print(str(keyword) + " != symbol")
        self.__file.write('\t' * indentation + '<keyword> ' + keyword[0] + ' </keyword>\n')

    def compile_symbol(self, indentation=0):
        keyword = self.tokens.pop()
        if (self.dbg):
            if (keyword[1] != 'symbol'):
                print(str(keyword) + " != symbol")
        self.__file.write('\t' * indentation + '<symbol> ' + keyword[0] + ' </symbol>\n')

    def compile_identifier(self, indentation=0):
        keyword = self.tokens.pop()
        if(self.dbg):
            if(keyword[1] != 'identifier'):
                print(str(keyword)+" != identifier")
        self.__file.write('\t' * indentation + '<identifier> ' + keyword[0] + ' </identifier>\n')


a = iter([('class', 'class'), ('Main', 'identifier'), ('{', 'symbol'), ('static', 'classVarDec'), ('int', 'type'),
          ('a', 'identifier'), (',', 'symbol'), ('b', 'identifier'), (';', 'symbol'), ('}', 'symbol')])
f = open('/home/david/Downloads/res', 'w')
worker = Worker(f, a)
