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
        self.cleanMode = False
        self.cleanMixDown = True
        self.verbose = False
        self.logger = "file"
        self.importMode = False
        self.targetsToImport = []
        self.interactive = False
        self.prefixDefined = False
        self.skipSteps = ""
        self.threadCount = 1
        self.overrideFile = ""
        self.compilerGroupName = ""
        self.optimizationGroupName = ""
        self.parallelGroupName = ""
        self.overrideGroup = None
        self.defines = defines.Defines()
        defines.setPrefixDefines(self.defines, '/usr/local')

    def __str__(self):
        if self.importMode:
            modeStr = "Import"
        elif self.cleanMode:
            modeStr = "Clean"
        else:
            modeStr = "Build"
        return "Options:\n\
  Mode:           " + modeStr + "\n\
  Project File:   " + self.projectFile + "\n\
  Build Dir:      " + self.buildDir + "\n\
  Download Dir:   " + self.downloadDir + "\n\
  Log Dir:        " + self.logDir + "\n\
  Clean MixDown:  " + str(self.cleanMixDown) + "\n\
  Verbose:        " + str(self.verbose) + "\n\
  Logger:         " + self.logger.capitalize() + "\n\
  Thread Count:   " + str(self.threadCount) + "\n\
  Job Count:      " + self.defines.get(defines.surround(defines.mdJobSlots[0])) + "\n\
  Skip Steps:     " + self.skipSteps + "\n\
  Override File:  " + self.overrideFile + "\n\
  Override Group Names:\n\
    Compiler:     " + self.compilerGroupName + "\n\
    Optimization: " + self.optimizationGroupName + "\n\
    Parallel:     " + self.parallelGroupName + "\n"

    def validate(self):
        if not self.__validateOptionsDir(self.buildDir) or not\
           self.__validateOptionsDir(self.downloadDir) or not\
           self.__validateOptionsDir(self.logDir):
            return False
        if self.importMode and self.cleanMode:
            logger.writeError("MixDown cannot be in both import mode and clean mode")
            return False
        if self.overrideFile == "" and (self.compilerGroupName != "" or self.optimizationGroupName != "" or self.parallelGroupName != ""):
            logger.writeError("Override group name(s) given but no override file specified.  Use command line option '-o<filename>'.")
            return False
        return True

    def __validateOptionsDir(self, path):
        if os.path.isfile(self.buildDir):
            logger.writeError("Cannot create directory by MixDown, a file by the same name already exists: " + path)
            return False
        return True

    def __processImportCommandline(self, commandline):
        if len(commandline) < 3:
            self.printUsage()
            return False

        self.verbose = True
        self.importMode = True
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
                self.targetsToImport.append(currTarget)
            else:
                logger.writeError("File not found or commandline option not understood: " + currArg)
                return False

        if len(self.targetsToImport) == 0:
            self.printUsage()
            return False

        return True

    def processCommandline(self, commandline=[]):
        if len(commandline) < 2:
            self.printUsage()
            return False

        if "--import" in commandline:
            if "--clean" in commandline:
                logger.writeError("MixDown cannot be in both import mode and clean mode")
                return False
            return self.__processImportCommandline(commandline)

        for currArg in commandline[1:]: #skip script name
            currFlag = currArg[:2].lower()
            currValue = currArg[2:]

            if currFlag == "-p":
                if not validateOptionPair(currFlag, currValue):
                    return False
                defines.setPrefixDefines(self.defines, os.path.abspath(currValue))
                self.prefixDefined = True
            elif currFlag == "-t":
                if not validateOptionPair(currFlag, currValue):
                    return False
                try:
                    count = int(currValue)
                except ValueError:
                    count = 0
                if count < 1:
                    logger.writeError("Positive numeric value needed " + definePair)
                    return False
                self.threadCount = count
            elif currFlag == "-j":
                if not validateOptionPair(currFlag, currValue):
                    return False
                try:
                    count = int(currValue)
                except ValueError:
                    count = 0
                if count < 1:
                    logger.writeError("Positive numeric value needed " + definePair)
                    return False
                #Add "-j<jobSlots>" only if user defines -j on commandline
                defines.setJobSlotsDefines(self.defines, currValue)
            elif currFlag == "-l":
                if not validateOptionPair(currFlag, currValue):
                    return False
                self.logger = str.lower(currValue)
            elif currFlag == "-b":
                if not validateOptionPair(currFlag, currValue):
                    return False
                self.buildDir = currValue
            elif currFlag == "-w":
                if not validateOptionPair(currFlag, currValue):
                    return False
                self.downloadDir = currValue
            elif currFlag == "-k":
                if not validateOption(currFlag, currValue):
                    return False
                if self.cleanMode == True:
                    logger.writeError("Command line arguments '--clean' and '-k' cannot both be used")
                    return False
                self.cleanMixDown = False
            elif currFlag == "-v":
                if not validateOption(currFlag, currValue):
                    return False
                self.verbose = True
            elif currFlag == "-s":
                if not validateOptionPair(currFlag, currValue):
                    return False
                self.skipSteps = currValue
            elif currFlag == "-o":
                if not validateOptionPair(currFlag, currValue):
                    return False
                self.overrideFile = currValue
            elif currFlag == "-g":
                if not validateOptionPair(currFlag, currValue):
                    return False
                groupsList = currValue.split(",")
                length = len(groupsList)
                if length >= 1:
                    self.compilerGroupName = groupsList[0].lower()
                if length >= 2:
                    self.optimizationGroupName = groupsList[1].lower()
                if length >= 3:
                    self.parallelGroupName = groupsList[2].lower()
            elif currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                self.printUsage()
                return False
            elif currArg.lower() == "--clean":
                if self.cleanMixDown == False:
                    logger.writeError("Command line arguments '--clean' and '-k' cannot both be used")
                    return False
                self.cleanMode = True
                self.cleanMixDown = False
            elif os.path.splitext(currArg)[1] == ".md":
                if not os.path.isfile(currArg):
                    logger.writeError("File " + currArg + " does not exist")
                    return False
                else:
                    self.projectFile = currArg
            else:
                logger.writeError("Command line argument '" + currArg + "' not understood")
                return False
        return True

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
        -j<number>    Number of build job slots\n\
        -t<number>    Number of threads used to build concurrent targets\n\
        -s<list>      Add steps to skip for individual targets\n\
           Example: -starget1:preconfig,target2:config\n\
        -o<path>      Specify path to Override Groups file\n\
        -g<Compiler>,<Debug>,<Parallel>  Specify Override Groups\n\
           Example: -gGNU,Debug,MPI\n\
           Example: -gGNU,,\n\
        -p<path>      Override prefix directory\n\
        -b<path>      Override build directory\n\
        -w<path>      Override download directory\n\
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
        -j<number>    Number of build job slots\n\
        -t<number>    Number of threads used to build concurrent targets\n\
        -b<path>      Override build directory\n\
        -w<path>      Override download directory\n\
        -l<logger>    Override default logger (Console, File, Html)\n\
    \n\
    Default Directories:\n\
    Builds:       mdBuild/\n\
    Downloads:    mdDownload/\n\
    Logs:         mdLogFiles/\n"

def validateOptionPair(flag, value):
    if value == "":
        logger.writeError(flag + " option requires a following value")
        return False
    return True

def validateOption(flag, value):
    if value != "":
        logger.writeError(flag + " option does not require a following value")
        return False
    return True
