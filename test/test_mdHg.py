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
import mdHg, utilityFunctions

class test_mdHg(unittest.TestCase):
    def test_isHgInstalled(self):
        returnValue = mdHg.isHgInstalled()
        self.assertEqual(returnValue, True, "Hg is not installed on your system.  All Hg tests will fail.")

    def test_isHgRepo(self):
        if not mdHg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        #Create repository and test if is hg repo
        tempRepo = mdTestUtilities.createHgRepository()
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
        if not mdHg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        tempDir = mdTestUtilities.makeTempDir()
        tempRepo = mdTestUtilities.createHgRepository()
        try:
            mdHg.hgCheckout(tempRepo, tempDir)
            returnValue = os.path.exists(tempDir + "testFile")
            self.assertEqual(returnValue, True, "'testFile' did not exist after mdHg.hgCheckout(" + tempRepo + ") was called.")
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(tempRepo)

if __name__ == "__main__":
    unittest.main()

