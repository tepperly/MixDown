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

import os, sys, unittest, mdTestUtilities

if not ".." in sys.path:
    sys.path.append("..")
import mdGit, utilityFunctions

class test_mdGit(unittest.TestCase):
    def test_isGitInstalled(self):
        returnValue = mdGit.isGitInstalled()
        self.assertEqual(returnValue, True, "Git is not installed on your system.  All Git tests will fail.")

    def test_isGitRepo(self):
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")
        #Create repository and test if is git repo
        tempRepo = mdTestUtilities.createGitRepository()
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
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")
        tempDir = mdTestUtilities.makeTempDir()
        tempRepo = mdTestUtilities.createGitRepository()
        try:
            mdGit.gitCheckout(tempRepo, tempDir)
            returnValue = os.path.exists(tempDir + mdTestUtilities.testFileName)
            self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after mdGit.gitCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(tempRepo)

if __name__ == "__main__":
    unittest.main()

