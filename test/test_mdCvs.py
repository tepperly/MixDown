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

class test_mdCvs(unittest.TestCase):
    def _createTempCvsRepository(self):
        tempPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        repoPath = tempPath + "repo"
        projPath = tempPath + "project"
        os.mkdir(repoPath)
        os.mkdir(projPath)

        utilityFunctions.executeSubProcess("cvs -d " + repoPath + " init", tempPath)
        utilityFunctions.executeSubProcess("touch testFile", projPath)
        utilityFunctions.executeSubProcess("cvs -d " + repoPath + " -q import -m message project vendor start", projPath)
        return repoPath

    def test_isCvsInstalled(self):
        returnValue = mdCvs.isCvsInstalled()
        self.assertEqual(returnValue, True, "Cvs is not installed in your system, all Cvs tests will fail.")

    def test_isCvsRepo(self):
        #Create repository and test if is cvs repo
        tempRepo = self._createTempCvsRepository()
        try:
            returnValue = mdCvs.isCvsRepo(tempRepo)
            self.assertEqual(returnValue, True, "mdCvs.isCvsRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempRepo)
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = mdCvs.isCvsRepo(falsePath)
        self.assertEqual(returnValue, False, "mdCvs.isCvsRepo(" + falsePath + ") should have returned false.")

    def _test_cvsCheckout(self):
        tempDir = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        tempRepo = self._createTempCvsRepository()
        try:
            mdCvs.cvsCheckout(tempRepo, tempDir)
            returnValue = os.path.exists(tempDir + "testFile")
            self.assertEqual(returnValue, True, "'testFile' did not exist after mdCvs.cvsCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(tempRepo)

if __name__ == "__main__":
    sys.path.append("..")
    import mdCvs, utilityFunctions
    unittest.main()