# Copyright (c) 2010, Lawrence Livermore National Security, LLC
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

import os, mdStrings, utilityFunctions

from mdLogger import *

class Options:
    def __init__(self):
        self.projectFile = ""
        self.buildDir = "mdBuild/"
        self.downloadDir = "mdDownload/"
        self.installDir = "mdInstall/"
        self.logDir = "mdLogFiles/"
        self.cleanBefore = False
        self.cleanAfter = False
        self.verbose = False
        self.logger = ""
        self.importer = False
        self._defines = dict()
        self._defines.setdefault("")

    def __str__(self):
        return "Options:\n\
  Project File: " + self.projectFile + "\n\
  Build Dir:    " + self.buildDir + "\n\
  Download Dir: " + self.downloadDir + "\n\
  Install Dir:  " + self.installDir + "\n\
  Defines:      " + str(self._defines) + "\n\
  Clean Before: " + str(self.cleanBefore) + "\n\
  Clean After:  " + str(self.cleanAfter) + "\n\
  Verbose:      " + str(self.verbose) + "\n\
  Logger:       " + self.logger.capitalize() + "\n"

    def _normalizeKey(self, key, lower=True):
        normalizedKey = key.strip()
        if lower:
            normalizedKey = normalizedKey.lower()
        if normalizedKey.startswith("$("):
            normalizedKey = normalizedKey[2:]
            if normalizedKey.endswith(")"):
                normalizedKey = normalizedKey[:-1]
            normalizedKey = normalizedKey.strip()
        return normalizedKey

    def setDefine(self, key, value):
        self._defines[self._normalizeKey(key)] = value.strip()

    def getDefine(self, key):
        normalizedKey = self._normalizeKey(key)
        strippedKey = self._normalizeKey(key, False)
        if normalizedKey in self._defines:
            value = self._defines[normalizedKey]
        elif strippedKey in os.environ:
            value = os.environ[strippedKey]
        else:
            value = ""
        return value

    @property
    def buildDir(self, value):
        self.buildDir = utilityFunctions.includeTrailingPathDelimiter(value)

    @property
    def downloadDir(self, value):
        self.downloadDir = utilityFunctions.includeTrailingPathDelimiter(value)

    @property
    def installDir(self, value):
        self.installDir = utilityFunctions.includeTrailingPathDelimiter(value)

    def expandDefines(self, inString):
        expandedString = inString
        loopCount = 0
        while expandedString.find("$(") != -1:
            if loopCount > 10:
                Logger().writeError("Define depth count (10) exceeded in string '" + inString + "'", exitProgram=True)

            strLength = len(expandedString)
            startIndex = 0
            endIndex = 0
            for i in range(strLength):
                if expandedString[i] == "$":
                    if strLength - i < 4:
                        if inString == expandedString:
                            Logger().writeError("Unterminated define found in '" + inString + "' at index " + str(i), exitProgram=True)
                        else:
                            Logger().writeError("Unterminated define found in original string '" + inString + "'\n After expanding defines, '" + expandedString + "'", exitProgram=True)
                    startIndex = i
                    break
            if startIndex != 0:
                for j in range(startIndex, strLength):
                    if expandedString[j] == ")":
                        endIndex = j
                        break
                defineName = expandedString[startIndex:endIndex+1]
                defineValue = self.getDefine(defineName)
                expandedString = expandedString.replace(defineName, defineValue)
            loopCount += 1
        expandedString = expandedString.replace("  ", " ").strip()
        return expandedString

    def processCommandline(self, commandLine = []):
        if len(commandLine) < 2:
            printUsageAndExit()

        for currArg in commandLine[1:]: #skip script name
            currFlag = str.lower(currArg[:2])
            currValue = currArg[2:]

            if currFlag == "-d":
                validateOptionPair(currFlag, currValue)
                for definePair in currValue.split(";"):
                    splitPair = definePair.split("=")
                    if len(splitPair) != 2:
                        Logger().writeError("Invalid define pair given, " + definePair, exitProgram=True)
                    if splitPair[0].lower() in self._defines:
                        Logger().writeError("Define pair already given, " + definePair, exitProgram=True)
                    self.setDefine(splitPair[0], splitPair[1])
            elif currFlag == "-p":
                validateOptionPair(currFlag, currValue)
                self.setDefine(mdStrings.mdDefinePrefix, currValue)
            elif currFlag == "-j":
                validateOptionPair(currFlag, currValue)
                self.setDefine(mdStrings.mdDefineJobSlots, currValue)
                #Add "-j<jobSlots>" only if user defines -j on commandline
                self.setDefine(mdStrings.mdMakeJobSlotsDefineName, mdStrings.mdMakeJobSlotsDefineValue)
            elif currFlag == "-l":
                validateOptionPair(currFlag, currValue)
                self.logger = str.lower(currValue)
            elif currFlag == "-b":
                validateOptionPair(currFlag, currValue)
                self.buildDir = currValue
            elif currFlag == "-o":
                validateOptionPair(currFlag, currValue)
                self.downloadDir = currValue
            elif currFlag == "-i":
                validateOptionPair(currFlag, currValue)
                self.installDir = currValue
            elif currFlag == "-c":
                validateOptionPair(currFlag, currValue)
                lowerCurrValue = str.lower(currValue)
                valueLength = len(currValue)
                if valueLength == 0:
                    Logger().writeError("Value, 'a' or 'b', expected after -c option", exitProgram=True)

                if currValue == 'a':
                    self.cleanAfter = True
                elif currValue == 'b':
                    self.cleanBefore = True
                else:
                    Logger().writeError("Unexpected value '" + currValue + "' given with -c option", exitProgram=True)
            elif currFlag == "-v":
                validateOption(currFlag, currValue)
                self.verbose = True
            elif currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                printUsageAndExit()
            elif os.path.splitext(currArg)[1] == ".md":
                if not os.path.isfile(currArg):
                    Logger().writeError("File " + currArg + " does not exist", exitProgram=True)
                else:
                    self.projectFile = currArg
            else:
                Logger().writeError("Command line argument '" + currArg + "' not understood", exitProgram=True)

def validateOptionPair(flag, value):
    if value == "":
        Logger().writeError(Flag + " option requires a following value", exitProgram=True)

def validateOption(flag, value):
    if value != "":
        Logger().writeError(Flag + " option does not require a following value", exitProgram=True)