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

import os, shutil, sys, tempfile

if not ".." in sys.path:
    sys.path.append("..")
import utilityFunctions

testFileName = "testFile"

def createTarFile():
    tempPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    os.mkdir(tempPath + "test")
    utilityFunctions.executeSubProcess("touch test/" + testFileName, tempPath)
    utilityFunctions.executeSubProcess("tar -cf test.tar test", tempPath)
    return tempPath, "test.tar"

def createGzipFile():
    tempPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    os.mkdir(tempPath + "test")
    utilityFunctions.executeSubProcess("touch test/" + testFileName, tempPath)
    utilityFunctions.executeSubProcess("tar -czf test.tgz test", tempPath)
    return tempPath, "test.tgz"

def createBzipFile():
    tempPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    os.mkdir(tempPath + "test")
    utilityFunctions.executeSubProcess("touch test/" + testFileName, tempPath)
    utilityFunctions.executeSubProcess("tar -cjf test.tar.bz2 test", tempPath)
    return tempPath, "test.tar.bz2"

def createCvsRepository():
    tempPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    repoPath = tempPath + "repo"
    projPath = tempPath + "project"
    os.mkdir(repoPath)
    os.mkdir(projPath)

    utilityFunctions.executeSubProcess("cvs -d " + repoPath + " init", tempPath)
    utilityFunctions.executeSubProcess("touch " + testFileName, projPath)
    utilityFunctions.executeSubProcess("cvs -d " + repoPath + " -Q import -m message project vendor start", projPath)
    return repoPath

def createGitRepository():
    repoPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    utilityFunctions.executeSubProcess("git init --quiet", repoPath)
    utilityFunctions.executeSubProcess("touch " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("git add " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("git commit -m message --quiet", repoPath)
    return repoPath

def createHgRepository():
    repoPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    utilityFunctions.executeSubProcess("hg init --quiet", repoPath)
    utilityFunctions.executeSubProcess("touch " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("hg add --quiet " + testFileName, repoPath)
    utilityFunctions.executeSubProcess("hg commit -m message --quiet", repoPath)
    return repoPath

def createSvnRepository():
    tempPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    repoPath = tempPath + "repo"
    repoURL = "file://" + repoPath + "/trunk"
    projPath = tempPath + "project"
    os.mkdir(repoPath)
    os.mkdir(projPath)

    utilityFunctions.executeSubProcess("svnadmin create " + repoPath, tempPath)
    utilityFunctions.executeSubProcess("touch testFile", projPath)
    utilityFunctions.executeSubProcess("svn import --quiet --non-interactive " + projPath + " " + repoURL + " -m message", tempPath)
    return repoURL

def createBlankFile(path):
    f = open(path, 'w')
    f.write("")
    f.close()

def makeTempDir():
    return utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))

def makeTempFile(contents="", suffix=""):
    fd, name = tempfile.mkstemp(suffix, "mixdown-", text=True)
    if contents != "":
        os.write(fd, contents)
    os.close(fd)
    return name

def copyDirToTempDir(source):
    tempDir = tempfile.mktemp(prefix="mixdown-")
    shutil.copytree(source, tempDir)
    return tempDir
