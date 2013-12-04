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

import os, socket, sys, tempfile
import defines, logger, target, utilityFunctions

class Options(object):
    def __init__(self):
        self.projectFile = ""
        self.buildDir = "mdBuild"
        self.downloadDir = "mdDownload"
        self.logDir = "mdLogFiles"
        self.restart = False
        self.statusLogPath = ""
        self.profileMode = False
        self.cleanMode = False
        self.importMode = False
        self.cleanMixDown = True
        self.verbose = False
        self.logger = "file"
        self.targetsToBuild = []
        self.targetsToImport = []
        self.interactive = False
        self.prefixDefined = False
        self.skipSteps = ""
        self.threadCount = 1
        self.overrideFile = ""
        self.overrideGroupNames = []
        self.overrideGroup = None
        self.overrideSearchPath = []
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
  Mode:                 " + modeStr + "\n\
  Project File:         " + self.projectFile + "\n\
  Build Dir:            " + self.buildDir + "\n\
  Download Dir:         " + self.downloadDir + "\n\
  Log Dir:              " + self.logDir + "\n\
  Clean MixDown:        " + str(self.cleanMixDown) + "\n\
  Restart build:        " + str(self.restart) + "\n\
  Verbose:              " + str(self.verbose) + "\n\
  Logger:               " + self.logger.capitalize() + "\n\
  Thread Count:         " + str(self.threadCount) + "\n\
  Job Count:            " + self.defines[defines.surround(defines.mdJobSlots[0])] + "\n\
  Skip Steps:           " + self.skipSteps + "\n\
  Override File:        " + self.overrideFile + "\n\
  Override Group Names: " + ", ".join(self.overrideGroupNames) + "\n"

    def setStatusLogPath(self, prefix, projectName):
        tempDir = os.path.join(tempfile.gettempdir(), 'mixdown')
        projectIdentifier = os.path.join(prefix, projectName).replace(os.path.sep, '%')
        self.statusLogPath = os.path.join(tempDir, projectIdentifier)

    def validate(self):
        if not self.__validateOptionsDir(self.buildDir) or not\
           self.__validateOptionsDir(self.downloadDir) or not\
           self.__validateOptionsDir(self.logDir):
            return False
        if self.importMode and self.cleanMode:
            logger.writeError("MixDown cannot be in both import mode and clean mode")
            return False
        if self.overrideFile == "" and len(self.overrideGroupNames) == 0:
            logger.writeError("Override group name(s) given but no override file specified.  Use command-line option '-o<filename>'.")
            return False
        if self.overrideFile != "" and len(self.overrideGroupNames) == 0:
            logger.writeError("Override file given but no override group(s) specified.  Use command-line option '-g<Name>[,<Name>...]'.")
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

        for currArg in commandline[1:]:
            if currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                self.printUsage()
                return False
            elif currArg == "--import":
                continue
            elif utilityFunctions.isURL(currArg) or os.path.isfile(currArg) or os.path.isdir(currArg):
                name = target.targetPathToName(currArg)
                if name == "":
                    return False
                currTarget = target.Target(name, currArg)
                self.targetsToImport.append(currTarget)
                continue

            currFlag = currArg[:2].lower()
            currValue = currArg[2:]

            if currFlag in ("-p", "-l", "-n", "-j", "-b", "-w", "-k", "-o", "-g", "-f"):
                logger.writeError("Command-line option is not allowed in import mode: " + currArg)
                return False
            if currFlag == "-i":
                if not validateOption(currFlag, currValue):
                    return False
                self.interactive = True
            elif currFlag == "-v":
                if not validateOption(currFlag, currValue):
                    return False
                self.verbose = True
            else:
                logger.writeError("File not found or command-line option not understood: " + currArg)
                return False

        if len(self.targetsToImport) == 0:
            self.printUsage()
            logger.writeError("No packages given when MixDown is in import mode")
            return False

        return True

    def __processProfileCommandline(self, commandline):
        if len(commandline) < 2:
            self.printUsage()
            return False

        self.verbose = True
        for currArg in commandline[1:]:
            if currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                self.printUsage()
                return False
            elif currArg == "--profile":
                continue

            currFlag = currArg[:2].lower()
            currValue = currArg[2:]

            if currFlag in ("-p", "-l", "-n", "-j", "-b", "-w", "-k", "-o", "-g", "-i", "-v", "-f"):
                logger.writeError("Command-line option is not allowed in profile mode: " + currArg)
                return False
            elif currFlag == "-d":
                if not validateOptionPair(currFlag, currValue):
                    return False
                paths = currValue.split(",")
                for path in paths:
                    self.overrideSearchPath.append((path, False))
            elif currFlag == "-r":
                if not validateOptionPair(currFlag, currValue):
                    return False
                paths = currValue.split(",")
                for path in paths:
                    self.overrideSearchPath.append((path, True))
            elif os.path.splitext(currArg)[1] == ".mdo":
                if os.path.isfile(currArg):
                    logger.writeError("Given override file name already exists: " + currArg)
                    return False
                self.overrideFile = currArg
            else:
                logger.writeError("File not found or command-line option not understood: " + currArg)
                return False

        if len(self.overrideSearchPath) == 0:
            self.overrideSearchPath = [("/usr/local/bin", False), ("/usr/bin", False)]
        if self.overrideFile == "":
            self.overrideFile = os.path.join(os.getcwd(), socket.gethostname() + ".mdo")

        return True

    def processCommandline(self, commandline=[]):
        if len(commandline) < 2:
            self.printUsage()
            return False

        #Find mode
        for arg in commandline[1:]: #skip script name
            loweredArg = arg.lower()
            if loweredArg == "--import":
                self.importMode = True
            elif loweredArg == "--clean":
                self.cleanMode = True
                self.cleanMixDown = False
            elif loweredArg == "--profile":
                self.profileMode = True

        if (self.cleanMode and (self.profileMode or self.importMode)) or\
           (self.profileMode and (self.importMode or self.cleanMode)):
                logger.writeError("MixDown cannot be in both two command-line modes at the same time. Run 'MixDown --help' for instructions.")
                return False

        if self.profileMode:
            return self.__processProfileCommandline(commandline)
        if self.importMode:
            return self.__processImportCommandline(commandline)

        for currArg in commandline[1:]: #skip script name
            #Handle all options that don't follow -<letter><option>
            if currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                self.printUsage()
                return False
            elif os.path.splitext(currArg)[1] == ".md":
                if not os.path.isfile(currArg):
                    logger.writeError("Project file " + currArg + " does not exist")
                    return False
                else:
                    self.projectFile = currArg
                    continue
            elif currArg.lower() == "--clean":
                continue

            #Handle all options that follow -<letter><option>
            currFlag = currArg[:2].lower()
            currValue = currArg[2:]

            if currFlag in ("-i"):
                logger.writeError("Command-line option is not allowed in build or clean mode: " + currArg)
                return False
            elif currFlag == "-p":
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
                #Add "-j<jobSlots>" only if user defines -j on command-line
                defines.setJobSlotsDefines(self.defines, currValue)
            elif currFlag == "-l":
                if not validateOptionPair(currFlag, currValue):
                    return False
                self.logger = str.lower(currValue)
            elif currFlag == "-r":
                if not validateOption(currFlag, currValue):
                    return False
                self.restart = True
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
                if self.cleanMode:
                    logger.writeError("Command-line arguments '--clean' and '-k' cannot both be used at the same time")
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
            elif currFlag == "-n":
                if not validateOptionPair(currFlag, currValue):
                    return False
                names = currValue.split(",")
                if len(names) == 0:
                    logger.writeError("Build target names command-line option used but no names specified.")
                    return False
                for name in names:
                    currName = name.lower().strip()
                    if currName == "":
                        logger.writeError("Empty build target name given on command-line (option '-n')")
                        return False
                    self.targetsToBuild.append(currName)
            elif currFlag == "-g":
                if not validateOptionPair(currFlag, currValue):
                    return False
                names = currValue.split(",")
                if len(names) == 0:
                    logger.writeError("Override group command-line option used but no names specified.")
                    return False
                for name in names:
                    currName = name.lower().strip()
                    if currName == "":
                        logger.writeError("Empty override group name given on command-line (option '-g')")
                        return False
                    self.overrideGroupNames.append(currName)
            else:
                logger.writeError("Command-line argument '" + currArg + "' not understood")
                return False

        return True

    def printUsageAndExit(self, errorStr=""):
        self.printUsage(errorStr)
        sys.exit()

    def printUsage(self, errorStr=""):
        if errorStr != "":
            print "Error: " + errorStr + "\n"

        print "\
    Profile Mode: \n\
        Example Usage: mixdown --profile\n\
    \n\
        Required:\n\
        --profile                 Toggle Profile mode\n\
    \n\
        Optional:\n\
        -d<list>      List of non-recursive search directories (comma-delimited)\n\
           Example: -d/home/foo/bin,/usr/local/bin\n\
        -r            List of recursive search directories (comma-delimited)\n\
           Example: -r/home/foo/bin,/usr/local/bin\n\
        <.mdo output file>   Path to outputted MixDown override group file\n\
    \n\
    Import Mode: \n\
        Example Usage: mixdown --import foo.tar.gz http://path/to/bar\n\
    \n\
        Required:\n\
        --import                  Toggle Import mode\n\
        <package location list>   Space delimited list of package locations\n\
    \n\
        Optional:\n\
        -i            Interactive Mode\n\
        -v            Verbose Mode\n\
    \n\
    Build Mode (Default): \n\
        Example Usage: mixdown foo.md\n\
    \n\
        Required:\n\
        <path to .md file>   Path to MixDown project file\n\
    \n\
        Optional:\n\
        -v            Verbose Mode\n\
        -r            Restart build on failed step or changed step\n\
        -j<number>    Number of build job slots\n\
        -t<number>    Number of threads used to build concurrent targets\n\
        -n<list>      Name of specific targets to build\n\
           Example: -nFoo,bar\n\
        -s<list>      Add steps to skip for individual targets\n\
           Example: -starget1:preconfig,target2:config\n\
        -o<path>      Specify path to Override Groups file\n\
        -g<Name>[,<Name>...]  Specify Override Groups\n\
           Example: -gGNU,Debug,MPI\n\
           Example: -gGNU\n\
        -p<path>      Override prefix directory\n\
        -b<path>      Override build directory\n\
        -w<path>      Override download directory\n\
        -l<logger>    Override default logger (Console, File, Html)\n\
        -k            Keeps previously existing MixDown directories\n\
    \n\
    Clean Mode: \n\
        Example Usage: mixdown --clean foo.md\n\
    \n\
        Required:\n\
        --clean              Toggle Clean mode\n\
        <path to .md file>   Path to MixDown project file\n\
    \n\
        Optional:\n\
        -v            Verbose Mode\n\
        -j<number>    Number of build job slots\n\
        -t<number>    Number of threads used to build concurrent targets\n\
        -s<list>      Add steps to skip for individual targets\n\
           Example: -starget1:preconfig,target2:config\n\
        -o<path>      Specify path to Override Groups file\n\
        -g<Name>[,<Name>...]  Specify Override Groups\n\
           Example: -gGNU,Debug,MPI\n\
           Example: -gGNU\n\
        -p<path>      Override prefix directory\n\
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
