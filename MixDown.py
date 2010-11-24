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

#! /usr/bin/env python

import os, sys, tarfile, urllib

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

    project, options = setup()
    for target in project.targets:
        for step in getBuildStepList():
            buildStepActor(step, target, options)
    cleanup(options)
    
    sys.exit()
    
def buildStepActor(stepName, target, options):
    Logger().reportStart(target.name, stepName)
    returnCode = None
    if target.hasStep(stepName):
        outFd = Logger().getOutFd(target.name, stepName)
        command = getCommand(stepName, target, options)
        if command != "":
            returnCode = executeSubProcess(command.split(" "), target.path, outFd, options.verbose, True)
    if returnCode == None:
        Logger().reportSkipped(target.name, stepName)
    elif returnCode != 0:
        Logger().reportFailure(target.name, stepName, returnCode, True)
    else:
        Logger().reportSuccess(target.name, stepName)    
        
#--------------------------------Setup---------------------------------
def setup():
    options = Options()
    print "Processing commandline options..."
    options.processCommandline()
    removeDir(options.logDir)
    SetLogger(options.logger, options.logDir)
    if options.verbose:
        Logger().writeMessage(str(options))
    
    #Read project file
    project = Project(options.projectFile)
    
    #Clean workspaces if told to clean before
    if options.cleanBefore:
        Logger().writeMessage("Cleaning MixDown directories...")
        try:
            removeDir(options.buildDir)
            removeDir(options.downloadDir)
            removeDir(options.installDir)
        except IOError, e:
            print e
            sys.exit()
        for currTarget in project.targets:
            if currTarget.output != "" and os.path.exists(currTarget.output):
                removeDir(currTarget.output)
                
    #Convert all targetPaths to folders (download and/or unpack if necessary)
    Logger().writeMessage("Converting all targets to local directories...")
    
    #Check for files that need to be downloaded
    for currTarget in project.targets:
        currPath = currTarget.path
        if (not os.path.isdir(currPath)) and (not os.path.isfile(currPath)) and isURL(currPath):
            if not os.path.isdir(options.downloadDir):
                os.makedirs(options.downloadDir)
            filenamePath = options.downloadDir + URLToFilename(currPath)
            urllib.urlretrieve(currPath, filenamePath)
            currTarget.path = filenamePath
    
    #Untar and add trailing path delimiter to any folders
    targetList = project.targets[:]
    targetList.reverse()
    for currTarget in targetList:
        currPath = currTarget.path
        if os.path.isdir(currPath):
            targetPaths[i] = includeTrailingPathDelimiter(currPath)
        elif os.path.isfile(currPath):
            if tarfile.is_tarfile(currPath):
                if currTarget.output == "":
                    if not os.path.isdir(options.buildDir):
                        os.makedirs(options.buildDir)
                    outDir = includeTrailingPathDelimiter(options.buildDir + splitFileName(currPath)[0])
                else:
                    outDir = currTarget.output
                untar(currPath, outDir, True)
                currTarget.path = outDir
            else:
                fileExt = os.path.splitext(currPath)[1]
                if basename.endswith(".tar.gz") or basename.endswith(".tar.bz2") or basename.endswith(".tar") or basename.endswith(".tgz") or basename.endswith(".tbz") or basename.endswith(".tb2"):
                    Logger().writeError("Given tar file '" + currPath +"' not understood by python's tarfile package", exitProgram=True)
                else:
                    Logger().writeError("Given target '" + currPath + "' not understood (folders, URLs, and tar files are acceptable)", exitProgram=True)
        else:
            Logger().writeError("Given target '" + currPath + "' does not exist", exitProgram=True)
            
    project.examine(options)

    prefixDefine = options.getDefine("prefix")
    if prefixDefine != "":
        strippedPrefix = stripTrailingPathDelimiter(prefixDefine)
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

    prefixDefine = options.getDefine("prefix")
    if prefixDefine != "":
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
    -u<path>      Override unpack folder\n\
    -l<logger>    Override default logger (Console, File, Html)\n\
    -cb           Cleanup before running (deletes unpack, build, and deploy directories)\n\
    -ca           Cleanup after deploy (deletes unpack and build directories)\n\
\n\
    Default Directories:\n\
    build: mdBuild/\n\
    deploy: mdDeploy/\n\
    unpack: mdUnpack/\n"
    
#---------------------------------------------------------------------

if __name__ == "__main__":
    main()