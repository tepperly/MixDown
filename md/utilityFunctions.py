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

import fileinput

import os, Queue, re, shutil, subprocess, sys, tarfile, tempfile, urllib, urllib2, zipfile

def downloadFile(URL, downloadDir):
    filePath = os.path.join(downloadDir, URLToFilename(URL))
    if not os.path.exists(downloadDir):
        os.mkdir(downloadDir)
    urllib.urlretrieve(URL, filePath)
    if not os.path.exists(filePath):
        filePath = ""
    return filePath

def executeCommand(command, args="", workingDirectory="", verbose=False, exitOnError=False):
    try:
        lastcwd = os.getcwd()
        if workingDirectory != "":
            os.chdir(workingDirectory)
        fullCommand = command + args
        if verbose:
            print "Executing: " + fullCommand + ": Working Directory: " + workingDirectory
        errorCode = os.system(fullCommand)
        if exitOnError and errorCode != 0:
            printErrorAndExit("Command '" + fullCommand + "': exited with error code " + str(errorCode))
    finally:
        os.chdir(lastcwd)

def executeSubProcess(command, workingDirectory=tempfile.gettempdir(), outFileHandle=1, verbose=False, exitOnError=False):
    if verbose:
        print "Executing: " + command + ": Working Directory: " + workingDirectory
    #***************************************************************************************************************
    #Note: Even though python's documentation says that "shell=True" opens up a computer for malicious shell commands,
    #  it is needed to allow users to fully utilize shell commands, such as cd.  Also it does not open up any additional
    #  vulnerabilities that did not already exist by running any other build tools, such as Make or configure.
    #***************************************************************************************************************
    process = subprocess.Popen(command, stdout=outFileHandle, stderr=outFileHandle, shell=True, cwd=workingDirectory)
    process.wait()
    if exitOnError and process.returncode != 0:
        printErrorAndExit("Command '" + command + "': exited with error code " + str(process.returncode))
    return process.returncode

def findShallowestFile(startPath, fileList):
    q = Queue.Queue()
    q.put(startPath)
    while not q.empty():
        currPath = includeTrailingPathDelimiter(q.get())
        for item in os.listdir(currPath):
            itemPath = currPath + item
            if os.path.isdir(itemPath):
                q.put(itemPath)
            elif item in fileList:
                return currPath + item # success

def getBasename(path):
    basename = os.path.basename(path)
    if not os.path.isdir(path):
        i = 0
        for c in basename:
            if (c == '.') and (not i == 0):
                break
            i += 1
        basename = basename[:i]
    return basename

def haveWriteAccess(path):
    highestExistingDir = path
    while highestExistingDir != os.sep:
        if os.path.exists(highestExistingDir):
            break
        if highestExistingDir[len(highestExistingDir)-1] == os.sep:
            highestExistingDir = highestExistingDir[:-1]
        highestExistingDir = highestExistingDir[:highestExistingDir.rfind(os.sep)+1]
    if os.access(highestExistingDir, os.W_OK):
        return True
    return False

def isURL(url):
    try:
        f = urllib2.urlopen(url)
        return True
    except:
        return False

def prettyPrintList(list, header="", headerIndent="", itemIndent=""):
    retStr = headerIndent + header
    listLen = len(list)
    if listLen == 1:
        retStr = retStr + list[0]
    elif listLen > 0:
        for currItem in list:
            retStr = retStr  + "\n" + itemIndent + currItem
    return retStr

def printErrorAndExit(errorStr, filePath="", lineNumber=0):
    sys.stdout.flush()
    if filePath == "" and lineNumber == 0:
        sys.stderr.write("Error: %s\n" % (errorStr))
    elif lineNumber == 0:
        sys.stderr.write("Error: %s: %s\n" % (filePath, errorStr))
    else:
        sys.stderr.write("Error: %s (line %d): %s\n" % (filePath, lineNumber, errorStr))
    sys.stderr.flush()
    sys.exit()

def removeDir(path):
    if (path[len(path)-1:] == '/') and os.path.isfile(path[:len(path)-1]):
        raise IOError("Error: Cannot clean directory '" + path + "' : File (not directory) exists by the same name.")
    if os.path.exists(path):
        shutil.rmtree(path)

def splitFileName(fileName):
    if fileName.endswith(os.path.sep):
        basename = fileName[:-1]
    else:
        basename = fileName
    version = ""

    if basename.endswith(".tar.gz"):
        basename = basename[:-7]
    elif basename.endswith(".tar.bz2"):
        basename = basename[:-8]
    elif basename.endswith(".zip") or basename.endswith(".tar") or\
         basename.endswith(".tgz") or basename.endswith(".tbz") or\
         basename.endswith(".tb2"):
        basename = basename[:-4]

    basename = os.path.basename(basename)

    i = 0
    for c in basename:
        if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            version = basename[i:]
            basename = basename[:i]
            if basename[-1] == '-':
                basename = basename[:-1]
            break
        i += 1

    return basename, version

def stripItemsInList(value):
    retList = []
    for item in value[:]:
        retList.append(str.strip(item))
    return retList

def untar(tarPath, outPath="", stripDir=False):
    if stripDir:
        unTarOutpath = tempfile.mkdtemp()
    else:
        unTarOutpath = outPath

    tar = tarfile.open(tarPath, "r")
    for item in tar:
        #TODO: check for relative path's
        tar.extract(item, unTarOutpath)

    if stripDir:
        dirList = os.listdir(unTarOutpath)
        if len(dirList) == 1:
            src = os.path.join(unTarOutpath, dirList[0])
        else:
            src = unTarOutpath
        shutil.move(src, outPath)

def unzip(zipPath, outPath="", stripDir=False):
    if stripDir:
        unZipOutpath = tempfile.mkdtemp()
    else:
        unZipOutpath = outPath

    z = zipfile.ZipFile(zipPath)
    z.extractall(unZipOutpath)

    if stripDir:
        dirList = os.listdir(unZipOutpath)
        if len(dirList) == 1:
            src = os.path.join(unZipOutpath, dirList[0])
        else:
            src = unZipOutpath
        shutil.move(src, outPath)

def URLToFilename(url):
    if url.endswith(os.sep):
        url = url[:1]
    #This works around sourceforge not having the filename last in the url
    pattern = r"https?://(www\.)?((sf)|(sourceforge))\.net/.*/(?P<filename>[^/]+((\.tar.gz)|(\.tar)|(\.tar.bz2)|(\.tgz)|(\.tbz)|(\.tb2)|(\.zip)))/download"
    regex = re.compile(pattern)
    match = regex.search(url)
    if match != None:
        fileName = match.group("filename")
        if fileName != None and fileName != "":
            return fileName

    fileName = url[(url.rfind(os.sep)+1):]
    if url == "" or file == "":
        return "_"
    return fileName

def setVariables(filename,variableList):
    isWritten = False
    try:
        for i, line in enumerate(fileinput.input(filename, inplace = 1)):
            isWritten = False
            line = line.strip()
            for variable,value in variableList.iteritems():
                if(line.startswith(variable)):
                    sys.stdout.write(variable+" = "+value+"\n")
                    isWritten = True
            if not isWritten: 
                sys.stdout.write(line+"\n")
        return True
    except Exception, e:
        print e
        return False

def is_exe(fpath):
    """Check if a file is an executable accessible by the user"""
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

def isInstalled(program):
    """Checks if a program is installed by searching for executable files in the PATH. 

    See: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python#377028
    """
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return True

    return False
