# Copyright (c) 2010-2011, Lawrence Livermore National Security, LLC
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

import os, sys
import defines, logger, target, utilityFunctions

class Options(object):
    def __init__(self):
        self.projectFile = ""
        self.buildDir = "mdBuild"
        self.downloadDir = "mdDownload"
        self.logDir = "mdLogFiles"
        self.cleanTargets = False
        self.cleanMixDown = True
        self.verbose = False
        self.logger = "file"
        self.importer = False
        self.interactive = False
        self.prefixDefined = False
        self.skipSteps = ""
        self._defines = dict()
        self._defines.setdefault("")
        defines.setPrefixDefines(self, '/usr/local')
        #defines.setCompilerDefines(self, '/usr/bin/gcc', '/usr/bin/g++', '/usr/bin/cpp')
        #defines.setCompilerDefines(self, '/home/white238/bin/gcc', '/home/white238/bin/g++')
        #defines.setCompilerDefines(self, '/home/white238/projects/gcc4.6.1/testPrefix/bin/gcc', '/home/white238/projects/gcc4.6.1/testPrefix/bin/g++', '/home/white238/projects/gcc4.6.1/testPrefix/bin/cpp')

    def __str__(self):
        return "Options:\n\
  Project File:  " + self.projectFile + "\n\
  Build Dir:     " + self.buildDir + "\n\
  Download Dir:  " + self.downloadDir + "\n\
  Log Dir:       " + self.logDir + "\n\
  Defines:       " + str(self._defines) + "\n\
  Import:        " + str(self.importer) + "\n\
  Clean Targets: " + str(self.cleanTargets) + "\n\
  Clean MixDown: " + str(self.cleanMixDown) + "\n\
  Verbose:       " + str(self.verbose) + "\n\
  Logger:        " + self.logger.capitalize() + "\n"

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

    def expandDefines(self, inString):
        expandedString = inString
        loopCount = 0
        while expandedString.find("$(") != -1:
            if loopCount > 10:
                logger.writeError("Define depth count (10) exceeded in string '" + inString + "'", exitProgram=True)

            strLength = len(expandedString)
            startIndex = 0
            endIndex = 0
            for i in range(strLength):
                if expandedString[i] == "$":
                    if strLength - i < 4:
                        if inString == expandedString:
                            logger.writeError("Unterminated define found in '" + inString + "' at index " + str(i), exitProgram=True)
                        else:
                            logger.writeError("Unterminated define found in original string '" + inString + "'\n After expanding defines, '" + expandedString + "'", exitProgram=True)
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

    def validateBuildDir(self):
        if os.path.isfile(self.buildDir):
            logger.writeError("Cannot create build directory, a file by the same name already exists", exitProgram=True)
        elif not os.path.isdir(self.buildDir):
            os.makedirs(self.buildDir)

    def validateDownloadDir(self):
        if os.path.isfile(self.downloadDir):
            logger.writeError("Cannot create download directory, a file by the same name already exists", exitProgram=True)
        elif not os.path.isdir(self.downloadDir):
            os.makedirs(self.downloadDir)

    def __processImportCommandline(self, commandline):
        if len(commandline) < 3:
            self.printUsageAndExit()

        targetsToImport = []
        self.verbose = True
        self.importer = True
        for currArg in commandline[1:]:
            if currArg == "--import":
                continue
            elif currArg.lower() == "-i":
                self.interactive = True
            elif currArg.lower() == "-v":
                self.verbose = True
            elif utilityFunctions.isURL(currArg) or os.path.isfile(currArg) or os.path.isdir(currArg):
                name = target.targetPathToName(currArg)
                currTarget = target.Target(name, currArg)
                targetsToImport.append(currTarget)
            else:
                logger.writeError("Could not understand given commandline option: " + currArg, exitProgram=True)

        if len(targetsToImport) == 0:
            self.printUsageAndExit()

        return targetsToImport

    def processCommandline(self, commandline=[]):
        if len(commandline) < 2:
            self.printUsageAndExit()

        if "--import" in commandline:
            return self.__processImportCommandline(commandline)

        for currArg in commandline[1:]: #skip script name
            currFlag = str.lower(currArg[:2])
            currValue = currArg[2:]

            if currFlag == "-d":
                validateOptionPair(currFlag, currValue)
                for definePair in currValue.split(";"):
                    splitPair = definePair.split("=")
                    if len(splitPair) != 2:
                        logger.writeError("Invalid define pair given, " + definePair, exitProgram=True)
                    if splitPair[0].lower() in self._defines:
                        logger.writeError("Define pair already given, " + definePair, exitProgram=True)
                    self.setDefine(splitPair[0], splitPair[1])
            elif currFlag == "-p":
                validateOptionPair(currFlag, currValue)
                defines.setPrefixDefines(self, os.path.abspath(currValue))
                self.prefixDefined = True
            elif currFlag == "-j":
                validateOptionPair(currFlag, currValue)
                #Add "-j<jobSlots>" only if user defines -j on commandline
                defines.setJobSlotsDefines(self, currValue)
            elif currFlag == "-l":
                validateOptionPair(currFlag, currValue)
                self.logger = str.lower(currValue)
            elif currFlag == "-b":
                validateOptionPair(currFlag, currValue)
                self.buildDir = currValue
            elif currFlag == "-o":
                validateOptionPair(currFlag, currValue)
                self.downloadDir = currValue
            elif currFlag == "-k":
                validateOptionPair(currFlag, currValue)
                if self.cleanTargets == True:
                    logger.writeError("Command line arguments '--clean' and '-k' cannot both be used", exitProgram=True)
                self.cleanMixDown = False
            elif currFlag == "-v":
                validateOption(currFlag, currValue)
                self.verbose = True
            elif currFlag == "-s":
                validateOptionPair(currFlag, currValue)
                self.skipSteps = currValue
            elif currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                self.printUsageAndExit()
            elif currFlag == "-c" or currArg.lower() == "--clean":
                if currFlag == "-c":
                    validateOption(currFlag, currValue)
                if self.cleanMixDown == False:
                    logger.writeError("Command line arguments '--clean' and '-k' cannot both be used", exitProgram=True)
                self.cleanTargets = True
                self.cleanMixDown = False
            elif os.path.splitext(currArg)[1] == ".md":
                if not os.path.isfile(currArg):
                    logger.writeError("File " + currArg + " does not exist", exitProgram=True)
                else:
                    self.projectFile = currArg
            else:
                logger.writeError("Command line argument '" + currArg + "' not understood", exitProgram=True)

    def printUsageAndExit(self, errorStr=""):
        self.printUsage(errorStr)
        sys.exit()

    def printUsage(self, errorStr=""):
        if errorStr != "":
            print "Error: " + errorStr + "\n"

        print "\
    Import Mode: \n\
        Example Usage: MixDown --import foo.tar.gz http://path/to/bar\n\
    \n\
        Required:\n\
        --import                  Toggle Import mode\n\
        <package location list>   Space delimited list of package locations\n\
    \n\
    Build Mode (Default): \n\
        Example Usage: MixDown foo.md\n\
    \n\
        Required:\n\
        <path to .md file>   Path to MixDown project file\n\
    \n\
        Optional:\n\
        -s<list>      Add steps to skip for individual targets\n\
           Example: -starget1:preconfig;target2:config\n\
        -p<path>      Override prefix directory\n\
        -b<path>      Override build directory\n\
        -o<path>      Override download directory\n\
        -l<logger>    Override default logger (Console, File, Html)\n\
        -k            Keeps previously existing MixDown directories\n\
    \n\
    Clean Mode: \n\
        Example Usage: MixDown --clean foo.md\n\
    \n\
        Required:\n\
        --clean              Toggle Clean mode\n\
        <path to .md file>   Path to MixDown project file\n\
    \n\
        Optional:\n\
        -b<path>      Override build directory\n\
        -o<path>      Override download directory\n\
        -l<logger>    Override default logger (Console, File, Html)\n\
    \n\
    Default Directories:\n\
    Builds:       mdBuild/\n\
    Downloads:    mdDownload/\n\
    Logs:         mdLogFiles/\n"

def validateOptionPair(flag, value):
    if value == "":
        logger.writeError(flag + " option requires a following value", exitProgram=True)

def validateOption(flag, value):
    if value != "":
        logger.writeError(flag + " option does not require a following value", exitProgram=True)
