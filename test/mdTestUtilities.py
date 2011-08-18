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

import os, shutil, sys, tempfile

if not ".." in sys.path:
    sys.path.append("..")

from md import utilityFunctions

testFileName = "testFile"

def createTarFile(tempDir):
    tarDir = os.path.join(tempDir, "tar")
    os.mkdir(tarDir)
    utilityFunctions.executeSubProcess("touch tar/" + testFileName, tempDir)
    utilityFunctions.executeSubProcess("tar -cf test.tar tar", tempDir)
    return tarDir, "test.tar"

def createGzipFile(tempDir):
    tarDir = os.path.join(tempDir, "tar")
    os.mkdir(tarDir)
    utilityFunctions.executeSubProcess("touch tar/" + testFileName, tempDir)
    utilityFunctions.executeSubProcess("tar -czf test.tgz tar", tempDir)
    return tarDir, "test.tgz"

def createBzipFile(tempDir):
    tarDir = os.path.join(tempDir, "tar")
    os.mkdir(tarDir)
    utilityFunctions.executeSubProcess("touch tar/" + testFileName, tempDir)
    utilityFunctions.executeSubProcess("tar -cjf test.tar.bz2 tar", tempDir)
    return tarDir, "test.tar.bz2"

def createZipFile(tempDir):
    zipDir = os.path.join(tempDir, "zip")
    os.mkdir(zipDir)
    utilityFunctions.executeSubProcess("touch zip/" + testFileName, tempDir)
    utilityFunctions.executeSubProcess("zip -q -r test.zip ./zip", tempDir)
    return zipDir, "test.zip"

def createCvsRepository(tempDir):
    repoPath = os.path.join(tempDir, "repo")
    projPath = os.path.join(tempDir, "project")
    os.mkdir(repoPath)
    os.mkdir(projPath)

    utilityFunctions.executeSubProcess("cvs -d " + repoPath + " init", tempDir)
    utilityFunctions.executeSubProcess("touch " + testFileName, projPath)
    utilityFunctions.executeSubProcess("cvs -d " + repoPath + " -Q import -m message project vendor start", projPath)
    return repoPath

def createGitRepository(tempDir):
    repoPath = os.path.join(tempDir, "repo")
    os.mkdir(repoPath)
    utilityFunctions.executeSubProcess("git init --quiet", repoPath)
    utilityFunctions.executeSubProcess("touch " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("git add " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("git commit -m message --quiet", repoPath)
    return repoPath

def createHgRepository(tempDir):
    repoPath = os.path.join(tempDir, "repo")
    os.mkdir(repoPath)
    utilityFunctions.executeSubProcess("hg init --quiet", repoPath)
    utilityFunctions.executeSubProcess("touch " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("hg add --quiet " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("hg commit -m message --quiet", repoPath)
    return repoPath

def createSvnRepository(tempDir):
    repoPath = os.path.join(tempDir, "repo")
    os.mkdir(repoPath)
    repoURL = "file://" + repoPath + "/trunk"
    projPath = os.path.join(tempDir, "project")
    os.mkdir(projPath)

    utilityFunctions.executeSubProcess("svnadmin create " + repoPath, tempDir)
    utilityFunctions.executeSubProcess("touch testFile", projPath)
    utilityFunctions.executeSubProcess("svn import --quiet --non-interactive " + projPath + " " + repoURL + " -m message", tempDir)
    return repoURL

def createBlankFile(path):
    open(path, 'w').close()

def createBlankFiles(path, fileList):
    for fileName in fileList:
        open(os.path.join(path, fileName), 'w').close()

def makeTempDir():
    return tempfile.mkdtemp(prefix="mixdown-")

def makeTempFile(directory, contents="", suffix=""):
    fd, name = tempfile.mkstemp(suffix, "mixdown-", directory, text=True)
    if contents != "":
        os.write(fd, contents)
    os.close(fd)
    return name

def copyDirToTempDir(source):
    tempDir = tempfile.mktemp(prefix="mixdown-")
    shutil.copytree(source, tempDir)
    return tempDir
