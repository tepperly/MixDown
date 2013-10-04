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

import os
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
        self.name = []
        self.defines = defines.Defines()

    def __str__(self):
        retStr = ", ".join(self.name) + " {\n"
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
        self.name = child.name
        for key in child:
            self[key] = child[key]
        for key in child.defines:
            self.defines[key] = child.defines[key]

def readGroups(filename):
    if not os.path.exists(filename):
        logger.writeError("Given Override file path did not exist. Check your -o command-line option.", filePath=filename)
        return None
    groups = list()
    overrideGroup = None
    tokenizer = Tokenizer(filename)
    if not tokenizer.tokenize():
        return None
    tokens = tokenizer.tokens
    i = 0
    lengthOfTokens = len(tokens)

    while i < lengthOfTokens:
        #Syntax start: <name>[, <name>]*
        overrideGroup = OverrideGroup()
        while not (tokens[i].type == TokenType.Symbol and tokens[i].value == '{'):
            if len(overrideGroup.name) > 50:
                logger.writeError("Override group name exceeded limit (50).", filePath=filename)
                return None

            if tokens[i].type == TokenType.Identifier:
                overrideGroup.name.append(tokens[i].value.lower())
                i += 1
                if i >= lengthOfTokens:
                    logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
                    return None

                if tokens[i].type == TokenType.Symbol and tokens[i].value == '{':
                    #End of override group name syntax hit
                    break
                elif tokens[i].type == TokenType.Symbol and tokens[i].value == ',':
                    i += 1
                    if i >= lengthOfTokens:
                        logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename)
                        return None
                else:
                    logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename)
                    return None
            else:
                logger.writeError("Expected Override group name, got '" + tokens[i].value + "'", filePath=filename)
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

        overrideGroupNames = ", ".join(overrideGroup)
        for group in groups:
            if ", ".join(group.name) == overrideGroupNames:
                logger.writeError("Duplicate override group name found: " + overrideGroupNames, filePath=options.overrideFile)
                return None
        groups.append(overrideGroup)
    return groups

def selectGroups(groups, options):
    finalGroup = OverrideGroup()

    for nameLength in range(1, len(options.overrideGroupNames)+1):
        increasingGroupName = ", ".join(options.overrideGroupNames[:nameLength])
        for currGroup in groups:
            if len(currGroup.name) != nameLength:
                continue
            currGroupName = ", ".join(currGroup.name)
            if currGroupName == increasingGroupName:
                finalGroup.combine(currGroup)
                break

    return finalGroup
