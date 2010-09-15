#! /usr/bin/env python

import os, sys, tarfile, urllib

from mdOptions import *
from mdProject import *
from mdTarget import *
from utilityFunctions import *
from mdPreConfigure import *
from mdConfigure import *
from mdBuild import *

#--------------------------------Main---------------------------------
def main():
    printProgramHeader()

    project, options = setup()
    preConfigure(project, options)
    configure(project, options)
    build(project, options)
    deploy(project, options)    
    cleanup(options)
    
    sys.exit()
        
#--------------------------------Setup---------------------------------
def setup():
    options = Options()
    print "Processing commandline options..."
    options.processCommandline()
    if options.getVerbose():
        print options

    #Clean workspaces if told to clean before
    if options.getCleanBefore():
        print "Cleaning MixDown directories..."
        try:
            removeDir(options.getBuildDir())
            removeDir(options.getDownloadDir())
            removeDir(options.getInstallDir())
        except IOError, e:
            print e
            sys.exit()
    if not os.path.isdir(options.getBuildDir()):
        os.makedirs(options.getBuildDir())
    if not os.path.isdir(options.getDownloadDir()):
        os.makedirs(options.getDownloadDir())
    if not os.path.isdir(options.getInstallDir()):
        os.makedirs(options.getInstallDir())
    
    #Read project file
    project = Project(options.getProjectFile())
    
    #Convert all targetPaths to folders (download and/or unpack if necessary)
    print "Converting all targets to local directories..."

    #Check for files that need to be downloaded
    for currTarget in project.getTargets():
        currPath = currTarget.getPath()
        if (not os.path.isdir(currPath)) and (not os.path.isfile(currPath)) and isURL(currPath):
            filenamePath = options.getDownloadDir() + URLToFilename(currPath)
            urllib.urlretrieve(currPath, filenamePath)
            currTarget.setPath(filenamePath)
    
    #Untar and add trailing path delimiter to any folders
    for currTarget in project.getTargets():
        currPath = currTarget.getPath()
        if os.path.isdir(currPath):
            targetPaths[i] = includeTrailingPathDelimiter(currPath)
        elif os.path.isfile(currPath):
            if tarfile.is_tarfile(currPath):
                basename = splitFileName(currPath)[0]
                tarOutputFolder = includeTrailingPathDelimiter(options.getBuildDir() + basename)
                untar(currPath, tarOutputFolder, True)
                currTarget.setPath(tarOutputFolder)
            else:
                fileExt = os.path.splitext(currPath)[1]
                if basename.endswith(".tar.gz") or basename.endswith(".tar.bz2") or basename.endswith(".tar") or basename.endswith(".tgz") or basename.endswith(".tbz") or basename.endswith(".tb2"):
                    printErrorAndExit("Given tar file '" + currPath +"' not understood by python's tarfile package")
                else:
                    printErrorAndExit("Given target '" + currPath + "' not understood (folders, URLs, and tar files are acceptable)")
        else:
            printErrorAndExit("Given target '" + currPath + "' does not exist")
            
    for currTarget in project.getTargets():
        currTarget.examine()

    return project, options

#------------------------------Deploy---------------------------------
def deploy(project, options):
    print "TODO: deploy not implemented yet"
    
#-----------------------------Clean up--------------------------------
def cleanup(options):
    if options.getCleanAfter():
        print "Cleaning MixDown Build and Download directories..."
        try:
            removeDir(options.getBuildDir())
            removeDir(options.getDownloadDir())
        except IOError, e:
            print e
            sys.exit()

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
    -b<path>      Override build directory\n\
    -d<path>      Override deploy directory\n\
    -u<path>      Override unpack folder\n\
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
