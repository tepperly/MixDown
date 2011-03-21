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
import mdGit, mdLogger, utilityFunctions

class Test_mdGit(unittest.TestCase):
    def test_isGitInstalled(self):
        returnValue = mdGit.isGitInstalled()
        self.assertEqual(returnValue, True, "Git is not installed on your system.  All Git tests will fail.")

    def test_isGitRepoCase1(self):
        #Case 1: Local directory that is a git repository
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")
        #Create repository and test if is git repo
        path = mdTestUtilities.createGitRepository()
        try:
            self.assertTrue(mdGit.isGitRepo(path), "mdGit.isGitRepo(" + path + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(path)
        #Test if wrong path returns false
        falsePath = "/foo/wrong/path"
        self.assertFalse(mdGit.isGitRepo(falsePath), "mdGit.isGitRepo(" + falsePath + ") should have returned false.")

    def test_isGitRepoCase2(self):
        #Case 2: URL that is a git repository
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")

        path = "http://github.com/tepperly/MixDown.git"
        self.assertTrue(mdGit.isGitRepo(path), "mdGit.isGitRepo(" + path + ") should have returned true.")
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = mdGit.isGitRepo(falsePath)
        self.assertEqual(returnValue, False, "mdGit.isGitRepo(" + falsePath + ") should have returned false.")

    def test_isGitRepoCase3(self):
        #Case 3: Check for false positive with .bz2 files
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")

        #Local file
        try:
            tarDir, path = mdTestUtilities.createBzipFile()
            self.assertFalse(mdGit.isGitRepo(path), "mdGit.isGitRepo(" + path + ") should have returned false.")
        finally:
            utilityFunctions.removeDir(tarDir)

        #Remote file
        path = "http://www.eng.lsu.edu/mirrors/apache//apr/apr-util-1.3.10.tar.bz2"
        self.assertFalse(mdGit.isGitRepo(path), "mdGit.isGitRepo(" + path + ") should have returned false.")

    def test_isGitRepoCase4(self):
        #Case 4: Check for false positive with .gz files
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")

        #Local file
        try:
            tarDir, path = mdTestUtilities.createGzipFile()
            self.assertFalse(mdGit.isGitRepo(path), "mdGit.isGitRepo(" + path + ") should have returned false.")
        finally:
            utilityFunctions.removeDir(tarDir)

        #Remote file
        path = "http://www.eng.lsu.edu/mirrors/apache//apr/apr-util-1.3.10.tar.gz"
        self.assertFalse(mdGit.isGitRepo(path), "mdGit.isGitRepo(" + path + ") should have returned false.")

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdGit))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()