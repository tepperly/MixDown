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
import mdAutoTools, mdLogger, utilityFunctions

class Test_mdAutoTools(unittest.TestCase):
    def test_isAutoToolsProject1(self):
        self.assertTrue(mdAutoTools.isAutoToolsProject("cases/simpleGraphAutoTools/TestCaseA"), "Failed to detect AutoTools project.")
        self.assertFalse(mdAutoTools.isAutoToolsProject("cases/cmake/hello/main"), "False positive when given CMake project.")

    def test_isAutoToolsProject2(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = utilityFunctions.includeTrailingPathDelimiter(tempDir) + "configure"
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(mdAutoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject3(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = utilityFunctions.includeTrailingPathDelimiter(tempDir) + "configure.in"
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(mdAutoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject4(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = utilityFunctions.includeTrailingPathDelimiter(tempDir) + "configure.ac"
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(mdAutoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getInstallDir(self):
        installDir = mdAutoTools.getInstallDir("configure --prefix=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --prefix=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --prefix=/usr/local --with-A=/usr/local/a")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --prefix=foobarbaz")
        self.assertEquals(installDir, "foobarbaz", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --prefix=")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --prefix= --with-A=/usr/local/a")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

        #Check for false positives
        installDir = mdAutoTools.getInstallDir("./cmake --prefix=foobarbaz")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --prefixasdf=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("./configure --with-prefix=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

        installDir = mdAutoTools.getInstallDir("--with-prefix=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdAutoTools))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()