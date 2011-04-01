#! /usr/bin/env python

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

import mdStrings, os, sys, tarfile, time, urllib

from mdCommands import *
from mdOptions import *
from mdProject import *
from mdTarget import *
from utilityFunctions import *
from mdLogger import *

originalLibraryPath = ""

#--------------------------------Main---------------------------------
def main():
    printProgramHeader()
    try:
        timeStart = time.time()

        project, options = setup()
        if project != None or options != None:
            for target in project.targets:
                for step in getBuildStepList():
                    succeeded = buildStepActor(step, target, options)
                    if not succeeded:
                        break
                if not succeeded:
                    break
        if options != None:
            cleanup(options)

        if project != None:
            timeFinished = time.time()
            timeElapsed = timeFinished - timeStart
            message = "\nProject " + project.name
            if succeeded:
                message += " succeeded.\n"
            else:
                message += " failed.\n"
            message += "Total time " + secondsToHMS(timeElapsed)
            Logger().writeMessage(message)
    finally:
        Logger().close()
    sys.exit()

def buildStepActor(stepName, target, options):
    Logger().reportStart(target.name, stepName)
    returnCode = None

    timeStart = time.time()

    if target.hasStep(stepName):
        outFd = Logger().getOutFd(target.name, stepName)
        command = getCommand(stepName, target, options)
        if command != "":
            returnCode = executeSubProcess(command, target.path, outFd, options.verbose)
        else:
            skipReason = "Command could not be determined by MixDown"
    else:
        skipReason = "Target specified to skip step"

    timeFinished = time.time()
    timeElapsed = timeFinished - timeStart

    if returnCode == None:
        Logger().reportSkipped(target.name, stepName, skipReason)
    elif returnCode != 0:
        Logger().reportFailure(target.name, stepName, timeElapsed, returnCode)
        return False
    else:
        Logger().reportSuccess(target.name, stepName, timeElapsed)
    return True

#--------------------------------Setup---------------------------------
def setup():
    options = Options()
    print "Processing commandline options..."
    options.processCommandline(sys.argv)
    removeDir(options.logDir)
    SetLogger(options.logger, options.logDir)
    if options.verbose:
        Logger().writeMessage(str(options))
        if not options.prefixDefined:
            Logger().writeMessage("No prefix defined, defaulting to '" + options.getDefine(mdStrings.mdDefinePrefix) + "'")

    project = Project(options.projectFile)
    if not project.read():
        return None, None

    #Clean workspaces if told to clean before
    if options.cleanBefore:
        Logger().writeMessage("Cleaning MixDown and Target output directories...")
        try:
            removeDir(options.buildDir)
            removeDir(options.downloadDir)
        except IOError, e:
            print e
            return None, None
        for currTarget in project.targets:
            if currTarget.output != "" and os.path.exists(currTarget.output):
                removeDir(currTarget.output)

    Logger().writeMessage("Converting all targets to local directories...")
    for currTarget in project.targets:
        currTarget.extract(options)

    if not project.examine(options):
        return None, None
    if not project.validate(options):
        return None, None

    prefixDefine = options.getDefine(mdStrings.mdDefinePrefix)
    if prefixDefine != "":
        strippedPrefix = stripTrailingPathDelimiter(prefixDefine)
        #TODO: only add lib64 if on 64bit machines
        libraryPaths = strippedPrefix + "/lib:" + strippedPrefix + "/lib64"
        if os.environ.has_key("LD_LIBRARY_PATH"):
            originalLibraryPath = str.strip(os.environ["LD_LIBRARY_PATH"])
            if originalLibraryPath != "":
                libraryPaths += ":" + originalLibraryPath
        os.environ["LD_LIBRARY_PATH"] = libraryPaths

    return project, options

#-----------------------------Clean up--------------------------------
def cleanup(options):
    if options.cleanAfter:
        Logger().writeMessage("Cleaning MixDown Build and Download directories...")
        try:
            removeDir(options.buildDir)
            removeDir(options.downloadDir)
        except IOError, e:
            Logger().writeError(e, exitProgram=True)

    prefixDefine = options.getDefine(mdStrings.mdDefinePrefix)
    if prefixDefine != "":
        #TODO: should this not clean up or maybe warn user to add it to their permament environment variable?
        os.environ["LD_LIBRARY_PATH"] = originalLibraryPath

#----------------------------------------------------------------------
def printProgramHeader():
    print "MixDown - A tool to simplify building\n"

def printUsageAndExit(errorStr = ""):
    printUsage(errorStr)
    sys.exit()

def printUsage(errorStr = ""):
    if errorStr != "":
        print "Error: " + errorStr + "\n"

    printProgramHeader()

    print "    Example Usage: ./MixDown.py foo.md\\\n\
\n\
    Required:\n\
    <path to .md file>   Path to MixDown project file\n\
\n\
    Optional:\n\
    -p<path>      Override prefix directory\n\
    -b<path>      Override build directory\n\
    -o<path>      Override download directory\n\
    -l<logger>    Override default logger (Console, File, Html)\n\
    -cb           Cleanup before running (deletes build and download directories)\n\
    -ca           Cleanup after deploy (deletes build and download directories)\n\
\n\
    Default Directories:\n\
    build: mdBuild/\n\
    download: mdDownload/\n"

#---------------------------------------------------------------------

if __name__ == "__main__":
    main()
