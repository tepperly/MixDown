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

class OverrideGroup(dict):
    def __init__(self):
        self.compiler = ""
        self.optimization = ""
        self.parallel = ""
        self.defines = defines.Defines()

    def __str__(self):
        retStr = self.compiler + ", " + self.optimization + ", " + self.parallel + " {\n"
        for key in self.keys():
            retStr += "    " + key + " = " + self[key] + "\n"
        for key in self.defines.keys():
            retStr += "    " + key + " = " + self.defines[key] + "\n"
        retStr += "}\n"
        return retStr

    def __contains__(self, key):
        return defines.normalizeKey(key) in self.keys()

    def __setitem__(self, key, value):
        super(OverrideGroup, self).__setitem__(defines.normalizeKey(key), value.strip())

    def __getitem__(self, key):
        normalizedKey = defines.normalizeKey(key)
        if normalizedKey in self:
            return super(OverrideGroup, self).__getitem__(defines.normalizeKey(key))
        else:
            return None

    def combine(self, child):
        self.compiler = child.compiler
        self.optimization = child.optimization
        self.parallel = child.parallel
        for key in child:
            self[key] = child[key]
        for key in child.defines:
            self.defines[key] = child.defines[key]

def readGroups(filename):
    groups = list()
    overrideGroup = None
    tokenizer = Tokenizer(filename)
    if not tokenizer.tokenize():
        return None
    tokens = tokenizer.tokens
    i = 0
    lengthOfTokens = len(tokens)

    while i < lengthOfTokens:
        #Syntax start: <compiler group name>, <optimization group name>, <parallel group name>
        if tokens[i].type == TokenType.Identifier:
            overrideGroup = OverrideGroup()
            overrideGroup.compiler = tokens[i].value
        else:
            logger.writeError("Expected Compiler Override group name '" + tokens[i].value + "'", filePath=filename)
            return None
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
            return None

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename)
            return None
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
            return None

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.optimization = tokens[i].value
        else:
            logger.writeError("Expected either Optimization Override group name or '*' got '" + tokens[i].value + "'", filePath=filename)
            return None
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
            return None

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename)
            return None
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
            return None

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.parallel = tokens[i].value
        else:
            logger.writeError("Expected either Parallel Override group name or '*' got '" + tokens[i].value + "'", filePath=filename)
            return None
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
            return None
        #Syntax end

        #Syntax start:
        #{
        #  <Identifier> = <string>
        #   ...
        #  <Identifier> = <string>
        #}
        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == '{'):
            logger.writeError("Expected '{' got '" + tokens[i].value + "'", filePath=filename)
            return None
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
            return None

        while True:
            if tokens[i].type == TokenType.Symbol and tokens[i].value == '}':
                i += 1
                break
            overrideName = ""
            overrideValue = ""

            #Syntax start:  <Identifier> = <string>
            if not tokens[i].type == TokenType.Identifier:
                logger.writeError("Expected Override identifier got '" + tokens[i].value + "'", filePath=filename)
                return None
            overrideNameOriginal = tokens[i].value
            overrideName = tokens[i].value.lower()
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
                return None

            if not (tokens[i].type == TokenType.Symbol and tokens[i].value == '='):
                logger.writeError("Expected '=' got '" + tokens[i].value + "'", filePath=filename)
                return None
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
                return None

            if not tokens[i].type == TokenType.String:
                logger.writeError("Expected Override value string got '" + tokens[i].value + "'", filePath=filename)
                return None
            overrideString = tokens[i].value
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
                return None

            #Compiler Overrides
            if overrideName in reservedOverrides:
                overrideGroup[overrideName] = overrideString
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

    if options.compilerGroupName == '*' and options.optimizationGroupName == '*' and options.parallelGroupName == '*':
        logger.writeError("Invalid override group name : *, *, *")
        return None
    if options.compilerGroupName == '*' or (options.optimizationGroupName == '*' and options.parallelGroupName != '*'):
        logger.writeError("Invalid override group name : " + options.compilerGroupName + ", " + options.optimizationGroupName + ", " + options.parallelGroupName\
                          + "\n*'s can only be used to the right and not to the left of a defined override group name.")
        return None

    for group in groups:
        if (group.compiler.lower() == options.compilerGroupName and group.compiler != "*")\
           and group.optimization == '*'\
           and group.parallel == '*':
            if compilerGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ",* ,*", filePath=options.overrideFile)
                return None
            finalGroup.combine(group)
            compilerGroupSet = True
    if compilerGroupSet == False and options.compilerGroupName != '*':
        logger.writeError("Compiler override group not found: " + options.compilerGroupName, filePath=options.overrideFile)
        return None

    for group in groups:
        if (group.compiler.lower() == options.compilerGroupName and group.compiler != "*")\
           and (group.optimization.lower() == options.optimizationGroupName and group.optimization != "*")\
           and group.parallel == '*':
            if optimizationGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ", " + group.optimization + ",*", filePath=options.overrideFile)
                return None
            finalGroup.combine(group)
            optimizationGroupSet = True
    if optimizationGroupSet == False and options.optimizationGroupName != '*':
        logger.writeError("Optimization override group not found: " + options.optimizationGroupName, filePath=options.overrideFile)
        return None

    for group in groups:
        if (group.compiler.lower() == options.compilerGroupName and group.compiler != "*")\
           and (group.optimization.lower() == options.optimizationGroupName and group.optimization != "*")\
           and (group.parallel.lower() == options.parallelGroupName and group.parallel != "*"):
            if parallelGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ", " + group.optimization + ", " + group.parallel, filePath=options.overrideFile)
                return None
            finalGroup.combine(group)
            parallelGroupSet = True
    if parallelGroupSet == False and options.parallelGroupName != '*':
        logger.writeError("Parallel override group not found: " + options.parallelGroupName, filePath=options.overrideFile)
        return None


    return finalGroup
