# Copyright (c) 2010-2013, Lawrence Livermore National Security, LLC
# Produced at Lawrence Livermore National Laboratory
# LLNL-CODE-462894
# All rights reserved.
#
# This file is part of MixDown. Please read the COPYRIGHT file
# for Our Notice and the LICENSE file for the GNU Lesser General Public
# License.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License (as published by
# the Free Software Foundation) version 3 dated June 2007.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
#  You should have recieved a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

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

    def _isValidIdentifierCharacter(self, value):
        if value.isalnum() or value in ['_', '-']:
            return True
        return False

    def _getToken(self, line, previousToken):
        token = Token()
        start = 0
        finish = 0
        lineLength = len(line)

        if previousToken.type == TokenType.Symbol and previousToken.value == "=":
            token.type = TokenType.String
            token.value = line
            line = ""
        elif self._isValidIdentifierCharacter(line[0]):
            token.type = TokenType.Identifier
            finish = 1
            while finish < lineLength:
                if not self._isValidIdentifierCharacter(line[finish]):
                    break
                finish += 1
            token.value = line[0:finish]
            line = line[finish:]
        elif line[0] in symbols:
            token.type = TokenType.Symbol
            token.value = line[0]
            line = line[1:]
        else:
            logger.writeError("Tokenizer failed on: " + line, filePath=self.fileName)
            return None, line

        line = line.lstrip()
        return token, line

    def tokenize(self):
        previousToken = Token()
        with open(self.fileName) as f:
            currLine, EOF = self._getLine(f)
            while not EOF:
                while currLine != "":
                    token, currLine = self._getToken(currLine, previousToken)
                    if token == None:
                        return False
                    previousToken = token
                    self.tokens.append(token)
                currLine, EOF = self._getLine(f)
            return True
