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

class test_mdHg(unittest.TestCase):
    def _createTempHgRepository(self):
        repoPath = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        utilityFunctions.executeSubProcess("hg init --quiet", repoPath)
        utilityFunctions.executeSubProcess("touch testFile", repoPath)
        utilityFunctions.executeSubProcess("hg add --quiet testFile", repoPath)
        utilityFunctions.executeSubProcess("hg commit -m message --quiet", repoPath)
        return repoPath

    def test_isHgInstalled(self):
        returnValue = mdHg.isHgInstalled()
        self.assertEqual(returnValue, True, "Hg is not installed in your system, all Hg tests will fail.")

    def test_isHgRepo(self):
        #Create repository and test if is hg repo
        tempRepo = self._createTempHgRepository()
        try:
            returnValue = mdHg.isHgRepo(tempRepo)
            self.assertEqual(returnValue, True, "mdHg.isHgRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempRepo)
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = mdHg.isHgRepo(falsePath)
        self.assertEqual(returnValue, False, "mdHg.isHgRepo(" + falsePath + ") should have returned false.")

    def test_hgCheckout(self):
        tempDir = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
        tempRepo = self._createTempHgRepository()
        try:
            mdHg.hgCheckout(tempRepo, tempDir)
            returnValue = os.path.exists(tempDir + "testFile")
            self.assertEqual(returnValue, True, "'testFile' did not exist after mdHg.hgCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(tempRepo)

if __name__ == "__main__":
    sys.path.append("..")
    import mdHg, utilityFunctions
    unittest.main()

