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

class test_mdGit(unittest.TestCase):
    def _createTempGitRepository(self):
        repoPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        utilityFunctions.executeSubProcess("git init --quiet", repoPath)
        utilityFunctions.executeSubProcess("touch testFile", repoPath)
        utilityFunctions.executeSubProcess("git add testFile", repoPath)
        utilityFunctions.executeSubProcess("git commit -m message --quiet", repoPath)
        return repoPath

    def test_isGitInstalled(self):
        returnValue = mdGit.isGitInstalled()
        self.assertEqual(returnValue, True, "Git is not installed in your system, all Git tests will fail.")

    def test_isGitRepo(self):
        #Create repository and test if is git repo
        tempRepo = self._createTempGitRepository()
        try:
            returnValue = mdGit.isGitRepo(tempRepo)
            self.assertEqual(returnValue, True, "mdGit.isGitRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempRepo)
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = mdGit.isGitRepo(falsePath)
        self.assertEqual(returnValue, False, "mdGit.isGitRepo(" + falsePath + ") should have returned false.")

    def test_gitCheckout(self):
        tempDir = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        tempRepo = self._createTempGitRepository()
        try:
            mdGit.gitCheckout(tempRepo, tempDir)
            returnValue = os.path.exists(tempDir + "testFile")
            self.assertEqual(returnValue, True, "'testFile' did not exist after mdGit.gitCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(tempRepo)

if __name__ == "__main__":
    sys.path.append("..")
    import mdGit, utilityFunctions
    unittest.main()

