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

from md import cvs, logger, utilityFunctions

class Test_cvs(unittest.TestCase):
    def test_isCvsInstalled(self):
        returnValue = cvs.isCvsInstalled()
        self.assertEqual(returnValue, True, "Cvs is not installed on your system.  All Cvs tests will fail.")

    def test_isCvsRepo(self):
        if not cvs.isCvsInstalled():
            self.fail("Cvs is not installed on your system.  All Cvs tests will fail.")
        #Create repository and test if is cvs repo
        tempDir = mdTestUtilities.makeTempDir()
        tempRepo = mdTestUtilities.createCvsRepository(tempDir)
        try:
            returnValue = cvs.isCvsRepo(tempRepo)
            self.assertEqual(returnValue, True, "cvs.isCvsRepo(" + tempRepo + ") should have returned true.")
        finally:
            utilityFunctions.removeDir(tempDir)
        #Test if wrong path returns false
        falsePath = "http://foo/wrong/path"
        returnValue = cvs.isCvsRepo(falsePath)
        self.assertEqual(returnValue, False, "cvs.isCvsRepo(" + falsePath + ") should have returned false.")

    def test_cvsCheckout(self):
        if not cvs.isCvsInstalled():
            self.fail("Cvs is not installed on your system.  All Cvs tests will fail.")
        tempDir = mdTestUtilities.makeTempDir()
        tempRepo = mdTestUtilities.createCvsRepository(tempDir)
        checkedOutRepo = os.path.join(tempDir, "checkedOut")
        try:
            cvs.cvsCheckout(tempRepo, checkedOutRepo)
            returnValue = os.path.exists(os.path.join(checkedOutRepo, mdTestUtilities.testFileName))
            self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after cvs.cvsCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_cvs))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
