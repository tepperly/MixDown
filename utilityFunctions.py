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

import os, Queue, shutil, sys, tarfile, tempfile, urllib2, subprocess

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

def executeSubProcess(command, workingDirectory="/tmp", outFileHandle=1, verbose=False, exitOnError=False):
    if verbose:
        print "Executing: " + command + ": Working Directory: " + workingDirectory
    tempArgs = command.split(" ")
    args = []
    for arg in tempArgs:
        arg = arg.strip()
        if arg != "":
            args.append(arg)
    process = subprocess.Popen(args, stdout=outFileHandle, stderr=outFileHandle, cwd=workingDirectory)
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

def includeTrailingPathDelimiter(path):
    if (not path[len(path)-1:] == '/') and (not os.path.isfile(path)):
        return path + '/'
    return path

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
    sys.stdin.flush()
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
    basename = fileName
    version = ""

    if basename.endswith(".tar.gz"):
        basename = basename[:-7]
    elif basename.endswith(".tar.bz2"):
        basename = basename[:-8]
    elif basename.endswith(".tar") or basename.endswith(".tgz") or basename.endswith(".tbz") or basename.endswith(".tb2"):
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

def stripTrailingPathDelimiter(path):
    if (path[len(path)-1:] == '/'):
        return path[:len(path)-1]
    return path

def untar(tarPath, outPath = "", stripDir=False):
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
            src = includeTrailingPathDelimiter(unTarOutpath) + dirList[0]
        else:
            src = includeTrailingPathDelimiter(unTarOutpath)
        shutil.move(src, outPath)

def URLToFilename(url):
    filename = url[(str.rfind(url, "/")+1):]
    if url == "" or file == "":
        return "_"
    return filename

