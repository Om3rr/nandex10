import re
from xml.sax.saxutils import escape

### CONSTANTs
isSingleComment = re.compile("\/\/[^\n]*\n")
iDontLikeTesters = re.compile("\"[^\n\"]*\/\/[^\n\"]*\"")
isMultiComment = re.compile("\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/")
symbols = "(\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~)"
isSymbol = re.compile(symbols)
symbolWithoutSpae = re.compile('([_\-A-Za-z0-9\"])?%s([\"_\-A-Za-z0-9])?' % symbols)
symbolsAreClose = re.compile('%s?%s%s' % (symbols, symbols, symbols))
splitByStrings = re.compile('\".+\"')


def character_generator(content):
    length = len(content)
    index = 0
    while index < length:
        if content[index] == '/' and index + 1 < length:
            if content[index + 1] in ('/', '*'):
                yield content[index:index + 2]
                index += 2
                continue
        if content[index] == '*' and index + 1 < length:
            if content[index + 1] == '/':
                yield '*/'
                index += 2
        yield content[index]
        index += 1


class Parser:
    def __init__(self, content):
        self.content = ''
        self.removeComments(content)
        self.splitShelAlufim()  ### assuming that in the even places we have non-string elems
        ### in the odd places we have string elems. so [::2] will iterate over the non strings
        self.buildMeal()

    def removeComments(self, content):
        in_multi_lines_comment = False
        in_single_comment = False
        in_string = False
        for char in character_generator(content):
            if in_string:
                # if char == '\n':
                #     self.content += '\\n'
                # elif char == '\t':
                #     self.content += '\\t'
                # else:
                #     self.content += char
                self.content += char
                if char == '"':
                    in_string = False
                    self.content += '\n'
                continue
            if in_multi_lines_comment:
                if char == '*/':
                    in_multi_lines_comment = False
                continue
            elif in_single_comment:
                if char == '\n':
                    in_single_comment = False
                    self.content += char
                continue
            elif char == '/*':
                in_multi_lines_comment = True
                self.content += ' '
                continue
            elif char == '//':
                in_single_comment = True
                continue
            elif char == '"':
                in_string = True
                self.content += ' '
            self.content += char

    def remove_multiLine(self, content):
        return re.sub(isMultiComment, "", content)

    def remove_singleLines(self, content):
        finder = re.findall(iDontLikeTesters, content)
        splittedContent = re.split(iDontLikeTesters, content)
        newContent = re.sub(isSingleComment, "\n", splittedContent[0])
        for idx, elem in enumerate(splittedContent[1:]):
            newContent += finder[idx] + "\n" + re.sub(isSingleComment, "\n", elem)
        return newContent

    def arrangeSymbols(selfl, text):
        def symbolChanger(match):
            if (match.group(1) and match.group(3)):
                return "%s %s %s" % (match.group(1), match.group(2), match.group(3))
            elif (match.group(1)):
                return "%s %s" % (match.group(1), match.group(2))
            elif (match.group(3)):
                return "%s %s" % (match.group(2), match.group(3))
            else:
                return match.group(2)

        text = re.sub(symbolWithoutSpae, symbolChanger, text)  #### EACH LINE
        text = re.sub(symbolWithoutSpae, symbolChanger, text)  #### HERE
        text = re.sub(symbolsAreClose, symbolChanger, text)  ### SIGNED IN BLOODDDDD
        text = re.sub(symbolsAreClose, symbolChanger, text)
        return text

    def splitShelAlufim(self):
        findings = re.findall(splitByStrings, self.content)
        self.listOfStatements = re.split(splitByStrings, self.content)
        self.finalList = []
        for i in range(len(findings)):
            self.finalList.append(self.arrangeSymbols(self.listOfStatements[i]))
            self.finalList.append(findings[i])
        self.finalList.append(self.arrangeSymbols(self.listOfStatements[-1]))

    def buildMeal(self):
        self.meal = []
        for elem in self.finalList:
            if ("\"" in elem):
                self.meal += [(escape(elem), "StringConstant")]
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
        # escapedSymb = escape(product)
        m = isOp.match(product)
        if m:
            return product, OP
        m = isUnary.match(product)
        if m:
            return product, UNARY
        return product, SYMBOL

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
            return (product, CONSTANT)
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
