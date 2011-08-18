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

import os, sys, unittest, mdTestUtilities

if not ".." in sys.path:
    sys.path.append("..")

from md import hg, logger, utilityFunctions

class Test_hg(unittest.TestCase):
    def test_isHgInstalled(self):
        returnValue = hg.isHgInstalled()
        self.assertEqual(returnValue, True, "Hg is not installed on your system.  All Hg tests will fail.")

    def test_isHgRepoCase1(self):
        #Case 1: Local directory that is a Hg repository
        if not hg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        #Create repository and test if is Hg repo
        tempDir = mdTestUtilities.makeTempDir()
        path = mdTestUtilities.createHgRepository(tempDir)
        try:
            self.assertTrue(hg.isHgRepo(path), "hg.isHgRepo(" + path + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempDir)
        #Test if wrong path returns false
        falsePath = "/foo/wrong/path"
        self.assertFalse(hg.isHgRepo(falsePath), "hg.isHgRepo(" + falsePath + ") should have returned false.")

    def test_isHgRepoCase2(self):
        #Case 2: URL that is a Hg repository
        if not hg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")

        path = "http://selenic.com/repo/hello"
        self.assertTrue(hg.isHgRepo(path), "hg.isHgRepo(" + path + ") should have returned true.")
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = hg.isHgRepo(falsePath)
        self.assertEqual(returnValue, False, "hg.isHgRepo(" + falsePath + ") should have returned false.")

    def test_isHgRepoCase3(self):
        #Case 3: Check for false positive with .bz2 files
        if not hg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")

        #Local file
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, path = mdTestUtilities.createBzipFile(tempDir)
            self.assertFalse(hg.isHgRepo(path), "hg.isHgRepo(" + path + ") should have returned false.")
        finally:
            utilityFunctions.removeDir(tempDir)

        #Remote file
        path = "http://www.eng.lsu.edu/mirrors/apache//apr/apr-util-1.3.10.tar.bz2"
        self.assertFalse(hg.isHgRepo(path), "hg.isHgRepo(" + path + ") should have returned false.")

    def test_isHgRepoCase4(self):
        #Case 4: Check for false positive with .gz files
        if not hg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")

        #Local file
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, path = mdTestUtilities.createGzipFile(tempDir)
            self.assertFalse(hg.isHgRepo(path), "hg.isHgRepo(" + path + ") should have returned false.")
        finally:
            utilityFunctions.removeDir(tempDir)

        #Remote file
        path = "http://www.eng.lsu.edu/mirrors/apache//apr/apr-util-1.3.10.tar.gz"
        self.assertFalse(hg.isHgRepo(path), "hg.isHgRepo(" + path + ") should have returned false.")

    def test_isHgRepo(self):
        if not hg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        #Create repository and test if is hg repo
        tempDir = mdTestUtilities.makeTempDir()
        tempRepo = mdTestUtilities.createHgRepository(tempDir)
        try:
            returnValue = hg.isHgRepo(tempRepo)
            self.assertEqual(returnValue, True, "hg.isHgRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempDir)
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = hg.isHgRepo(falsePath)
        self.assertEqual(returnValue, False, "hg.isHgRepo(" + falsePath + ") should have returned false.")

    def test_hgCheckout(self):
        if not hg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        tempDir = mdTestUtilities.makeTempDir()
        tempRepo = mdTestUtilities.createHgRepository(tempDir)
        checkedOutRepo = os.path.join(tempDir, "checkedOut")
        try:
            hg.hgCheckout(tempRepo, checkedOutRepo)
            returnValue = os.path.exists(os.path.join(checkedOutRepo, "testFile"))
            self.assertEqual(returnValue, True, "'testFile' did not exist after hg.hgCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_hg))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
