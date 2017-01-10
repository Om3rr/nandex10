import re
from xml.sax.saxutils import escape

### CONSTANTs
isSingleComment = re.compile("\s*\/\/[^\n]*\n")
isMultiComment = re.compile("\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/")
symbols = "(\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~)"
isSymbol = re.compile(symbols)
symbolWithoutSpae = re.compile('([_\-A-Za-z0-9\"])?%s([\"_\-A-Za-z0-9])?' % symbols)
symbolsAreClose = re.compile('%s?%s%s' % (symbols, symbols, symbols))
splitByStrings = re.compile('\".+\"')


class Parser:
    def __init__(self, content):
        self.removeComments(content)
        self.arrangeSymbols()
        self.splitShelAlufim()  ### assuming that in the even places we have non-string elems
        ### in the odd places we have string elems. so [::2] will iterate over the non strings
        self.buildMeal()
        # f = open('etc/testish.txt', 'w')
        # for elem in self.meal:
        #     f.write(str(elem))
        #     f.write('\n')
        # f.close()

    def removeComments(self, content):
        content = self.remove_multiLine(content)
        self.content = self.remove_singleLines(content)

    def remove_multiLine(self,content):
        return re.sub(isMultiComment, "", content)

    def remove_singleLines(self, content):
        return re.sub(isSingleComment, "\n", content)

    def arrangeSymbols(self):
        def symbolChanger(match):
            if (match.group(1) and match.group(3)):
                return "%s %s %s" % (match.group(1), match.group(2), match.group(3))
            elif (match.group(1)):
                return "%s %s" % (match.group(1), match.group(2))
            elif (match.group(3)):
                return "%s %s" % (match.group(2), match.group(3))
            else:
                return match.group(2)

        self.content = re.sub(symbolWithoutSpae, symbolChanger, self.content)  #### EACH LINE
        self.content = re.sub(symbolWithoutSpae, symbolChanger, self.content)  #### HERE
        self.content = re.sub(symbolsAreClose, symbolChanger, self.content)  ### SIGNED IN BLOODDDDD
        self.content = re.sub(symbolsAreClose, symbolChanger, self.content)

    def splitShelAlufim(self):
        findings = re.findall(splitByStrings, self.content)
        self.listOfStatements = re.split(splitByStrings, self.content)
        self.finalList = []
        for i in range(len(findings)):
            self.finalList.append(self.listOfStatements[i])
            self.finalList.append(findings[i])
        self.finalList.append(self.listOfStatements[-1])

    def buildMeal(self):
        self.meal = []
        for elem in self.finalList:
            if ("\"" in elem):
                self.meal += [(elem[1:-1], "StringConstant")]
                continue
            products = re.split('\s+', elem)
            tempMeal = []
            for prod in products:
                if (prod == ''):
                    continue  # no meat...
                tempMeal.append(self.eat(prod))
            self.meal += tempMeal

    def eat(self, product):
        INTEGER_CONSTANT = 'integerConstant'
        STRING_CONSTANT = 'stringConstant'
        IDENTIFIER = 'identifier'
        isInteger = re.compile('\d+$')
        isIdentifier = re.compile('[A-Za-z_][A-Za-z_0-9]*$')
        isKeyword = re.compile(
            '(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)$')

        m = isKeyword.match(product)
        if (m):
            return self.parseKeyword(product)
        m = isIdentifier.match(product)
        if (m):
            return (product, IDENTIFIER)
        m = isInteger.match(product)
        if (m):
            return (product, INTEGER_CONSTANT)
        m = isSymbol.match(product)
        if (m):
            return self.parseSymbol(product)

    def parseSymbol(self, product):
        OP = 'op'
        UNARY = 'unaryOp'
        SYMBOL = 'symbol'
        isOp = re.compile('(\+|\-|\*|\/|\&|\||\<|\>|\=)$')
        isUnary = re.compile('(\-|\~)$')
        escapedSymb = escape(product)
        m = isOp.match(product)
        if (m):
            return (escapedSymb, OP)
        m = isUnary.match(product)
        if (m):
            return (escapedSymb, UNARY)
        return (escapedSymb, SYMBOL)

    def parseKeyword(self, product):
        CONSTANT = 'KeywordConstant'
        CLASS_VAR_DEC = 'classVarDec'
        VAR_DEC = 'varDec'
        TYPE = 'type'
        SUBROUTINE = 'subroutineDec'
        isConstant = re.compile('(true|false|null|this)$')
        isStatement = re.compile('(let|if|while|do|return|else)$')
        isType = re.compile('(int|char|boolean)$')
        isClassVerDec = re.compile('(static|field)$')
        isVarDec = re.compile('(var)$')
        isSubroutine = re.compile('(constructor|function|method|void)$')
        m = isConstant.match(product)
        if (m):
            return (m, CONSTANT)
        m = isStatement.match(product)
        if (m):
            return self.parseStatement(product)
        m = isType.match(product)
        if (m):
            return (product, TYPE)
        m = isClassVerDec.match(product)
        if (m):
            return (product, CLASS_VAR_DEC)
        m = isVarDec.match(product)
        if (m):
            return (product, VAR_DEC)
        m = isSubroutine.match(product)
        if (m):
            return (product, SUBROUTINE)
        return (product, 'keyword')

    def parseStatement(self, product):
        if (product == 'let'):
            return (product, 'letStatement')
        elif (product == 'while'):
            return (product, 'whileStatement')
        elif (product == 'do'):
            return (product, 'doStatement')
        elif (product == 'return'):
            return (product, 'ReturnStatement')
        return (product, 'ifStatement')







        #
        # f = open('etc/test1.jack','r')
        # reader = f.read()
        # p = Parser(reader)
