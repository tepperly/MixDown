import logger

symbols = ['=', '{', '}', ",", "*"]

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

TokenType = enum('None', 'Identifier', 'String', 'Symbol')

class Token(object):
    def __init__(self):
        self.type = TokenType.None
        self.value = ""

    def __str__(self):
        if self.type == TokenType.None:
            typeString = "None"
        elif self.type == TokenType.Identifier:
            typeString = "Identifier"
        elif self.type == TokenType.String:
            typeString = "String"
        elif self.type == TokenType.Symbol:
            typeString = "Symbol"
        return typeString + ": " + self.value

class Tokenizer(object):
    def __init__(self, fileName):
        self.tokens = []
        self.fileName = fileName

    def _getLine(self, f, previousLine=""):
        currLine = f.readline()
        if currLine == "":
            if previousLine != "":
                return previousLine, False
            return previousLine, True
        currLine = currLine.strip()
        if currLine[:1] == "#":
            currLine = ""
        if previousLine != "":
            if currLine != "":
                currLine = previousLine + " " + currLine
            else:
                currLine = previousLine
        if currLine[-1:] == "\\":
            currLine, EOF = self._getLine(f, currLine[:-1])
        return currLine, False

    def _getToken(self, line, previousToken):
        token = Token()
        start = 0
        finish = 0
        lineLength = len(line)

        if previousToken.type == TokenType.Symbol and previousToken.value == "=":
            token.type = TokenType.String
            token.value = line
            line = ""
        elif line[0].isalnum():
            token.type = TokenType.Identifier
            finish = 1
            while finish < lineLength:
                if not line[0:finish].isalnum():
                    finish -= 1
                    break
                finish += 1
            token.value = line[0:finish]
            line = line[finish:]
        elif line[0] in symbols:
            token.type = TokenType.Symbol
            token.value = line[0]
            line = line[1:]
        else:
            logger.writeError("Tokenizer failed on: " + line, filePath=self.fileName, exitProgram=True)

        line = line.lstrip()
        return token, line

    def tokenize(self):
        try:
            previousToken = Token()
            f = open(self.fileName)
            currLine, EOF = self._getLine(f)
            while not EOF:
                while currLine != "":
                    token, currLine = self._getToken(currLine, previousToken)
                    previousToken = token
                    self.tokens.append(token)
                currLine, EOF = self._getLine(f)
        finally:
            f.close()
