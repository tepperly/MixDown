# Copyright (c) 2010-2012, Lawrence Livermore National Security, LLC
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

from md import logger, options, profiler, utilityFunctions

class Test_profiler(unittest.TestCase):
    def test_findExecutables01(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            exes = profiler.findExecutables([(tempDir, False)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables02(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            exes = profiler.findExecutables([(tempDir, True)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables03(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, False)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables04(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, True)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables05(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, False)], ["gcc"])
            self.assertEquals(len(exes), 0, "profiler.findExecutables did not find the right amount of executables")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables06(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, True)], ["gcc"])
            self.assertEquals(len(exes), 0, "profiler.findExecutables did not find the right amount of executables")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_profiler))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
