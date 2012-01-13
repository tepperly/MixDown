# Copyright (c) 2010-2012, Lawrence Livermore National Security, LLC
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

from tokenizer import Tokenizer, TokenType
import defines, logger

reservedOverrides = ["ccompiler",        "cflags",    "cdefines",
                     "cpreprocessor",    "cppflags",
                     "cxxcompiler",      "cxxflags",
                     "fcompiler",        "fflags",    "flibs",
                     "f77compiler",      "f77flags",  "f77libs",
                     "objccompiler",     "objcflags",
                     "objcpreprocessor",
                     "objcxxcompiler",   "objcxxflags"
                     "objcxxpreprocessor",
                     "linkerflags", "linkerflagsexe", "linkerflagsshared", "linkerflagsmodule",
                     ]

class OverrideGroup(object):
    def __init__(self):
        self.compiler = ""
        self.optimization = ""
        self.parallel = ""
        self.overrides = dict()
        self.defines = dict()

    def combine(self, child):
        self.compiler = child.compiler
        self.optimization = child.optimization
        self.parallel = child.parallel
        for override in child.overrides.keys():
            self.overrides[override] = child.overrides[override]
        for define in child.defines.keys():
            self.defines[define] = child.defines[define]

    def hasOverride(self, override):
        return self.overrides.has_key(override.lower())

    def getOverride(self, override):
        key = override.lower()
        if self.overrides.has_key(key):
            return self.overrides[key]
        else:
            return None

    def setOverride(self, override, value):
        self.overrides[override.lower()] = value

def readGroups(filename):
    groups = list()
    overrideGroup = None
    tokenizer = Tokenizer(filename)
    tokenizer.tokenize()
    tokens = tokenizer.tokens
    i = 0
    lengthOfTokens = len(tokens)

    while i < lengthOfTokens:
        #Syntax start: <compiler group name>, <optimization group name>, <parallel group name>
        if tokens[i].type == TokenType.Identifier:
            overrideGroup = OverrideGroup()
            overrideGroup.compiler = tokens[i].value
        else:
            logger.writeError("Expected Compiler Override group name '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.optimization = tokens[i].value
        else:
            logger.writeError("Expected either Optimization Override group name or '*' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.parallel = tokens[i].value
        else:
            logger.writeError("Expected either Parallel Override group name or '*' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)
        #Syntax end

        #Syntax start:
        #{
        #  <Identifier> = <string>
        #   ...
        #  <Identifier> = <string>
        #}
        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == '{'):
            logger.writeError("Expected '{' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        while True:
            if tokens[i].type == TokenType.Symbol and tokens[i].value == '}':
                i += 1
                break
            overrideName = ""
            overrideValue = ""

            #Syntax start:  <Identifier> = <string>
            if not tokens[i].type == TokenType.Identifier:
                logger.writeError("Expected Override identifier got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
            overrideNameOriginal = tokens[i].value
            overrideName = tokens[i].value.lower()
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

            if not (tokens[i].type == TokenType.Symbol and tokens[i].value == '='):
                logger.writeError("Expected '=' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

            if not tokens[i].type == TokenType.String:
                logger.writeError("Expected Override value string got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
            overrideString = tokens[i].value
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

            #Compiler Overrides
            if overrideName in reservedOverrides:
                overrideGroup.setOverride(overrideName, overrideString)
            else:
                overrideGroup.defines[overrideName] = overrideString
            #Syntax end

        #Syntax end

        groups.append(overrideGroup)
    return groups

def selectGroups(groups, options):
    compilerGroupSet = False
    optimizationGroupSet = False
    parallelGroupSet = False
    finalGroup = OverrideGroup()

    for group in groups:
        if group.compiler.lower() == options.compilerGroupName and group.optimization == '*' and group.parallel == '*':
            if compilerGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ",* ,*", filePath=options.overrideFile, exitProgram=True)
            finalGroup = group
            compilerGroupSet = True
    for group in groups:
        if group.optimization.lower() == options.optimizationGroupName:
            if optimizationGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ", " + group.optimization + ",*", filePath=options.overrideFile, exitProgram=True)
            finalGroup.combine(group)
            optimizationGroupSet = True
    for group in groups:
        if group.parallel.lower() == options.parallelGroupName:
            if parallelGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ", " + group.optimization + group.parallel, filePath=options.overrideFile, exitProgram=True)
            finalGroup.combine(group)
            parallelGroupSet = True

    options.overrideGroup = finalGroup
    defines.setOverrideDefines(options, finalGroup)
