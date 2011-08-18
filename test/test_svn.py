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

from md import logger, svn, utilityFunctions

class Test_svn(unittest.TestCase):
    def test_isSvnInstalled(self):
        returnValue = svn.isSvnInstalled()
        self.assertEqual(returnValue, True, "Svn is not installed on your system.  All Svn tests will fail.")

    def test_isSvnRepo(self):
        if not svn.isSvnInstalled():
            self.fail("Svn is not installed on your system.  All Svn tests will fail.")
        #Create repository and test if is svn repo
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempRepo = mdTestUtilities.createSvnRepository(tempDir)
            returnValue = svn.isSvnRepo(tempRepo)
            self.assertEqual(returnValue, True, "svn.isSvnRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempDir)
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = svn.isSvnRepo(falsePath)
        self.assertEqual(returnValue, False, "svn.isSvnRepo(" + falsePath + ") should have returned false.")

    def test_svnCheckout(self):
        if not svn.isSvnInstalled():
            self.fail("Svn is not installed on your system.  All Svn tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempRepo = mdTestUtilities.createSvnRepository(tempDir)
            checkedOutRepo = os.path.join(tempDir, "checkedOut")
            svn.svnCheckout(tempRepo, checkedOutRepo)
            returnValue = os.path.exists(os.path.join(checkedOutRepo, mdTestUtilities.testFileName))
            self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after svn.svnCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_svn))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
