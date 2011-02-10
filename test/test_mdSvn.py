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

import os, sys, unittest, tempfile

class test_mdSvn(unittest.TestCase):
    def _createTempSvnRepository(self):
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

    def test_isSvnInstalled(self):
        returnValue = mdSvn.isSvnInstalled()
        self.assertEqual(returnValue, True, "Svn is not installed in your system, all Svn tests will fail.")

    def test_isSvnRepo(self):
        #Create repository and test if is svn repo
        tempRepo = self._createTempSvnRepository()
        try:
            returnValue = mdSvn.isSvnRepo(tempRepo)
            self.assertEqual(returnValue, True, "mdSvn.isSvnRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempRepo[6:len(tempRepo)-11]) #"file://tmp/mixdown-*/repo/trunk" -> "//tmp/mixdown-*/"
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = mdSvn.isSvnRepo(falsePath)
        self.assertEqual(returnValue, False, "mdSvn.isSvnRepo(" + falsePath + ") should have returned false.")

    def test_svnCheckout(self):
        tempDir = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        tempRepo = self._createTempSvnRepository()
        try:
            mdSvn.svnCheckout(tempRepo, tempDir)
            returnValue = os.path.exists(tempDir + "testFile")
            self.assertEqual(returnValue, True, "'testFile' did not exist after mdSvn.svnCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(tempRepo[6:len(tempRepo)-11]) #"file://tmp/mixdown-*/repo/trunk" -> "//tmp/mixdown-*/"

if __name__ == "__main__":
    sys.path.append("..")
    import mdSvn, utilityFunctions
    unittest.main()