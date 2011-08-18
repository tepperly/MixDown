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

from md import autoTools, logger, utilityFunctions

class Test_autoTools(unittest.TestCase):
    def test_generateConfigureFiles(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseA")
            success = autoTools.generateConfigureFiles(tempDir, "testCaseTarget", False)
            self.assertEquals(success, True, "Unable to generate configure files.")
            self.assertEquals(os.path.exists(os.path.join(tempDir, "configure")), True, "Configure files did not exist after calling generateConfigureFiles.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject1(self):
        self.assertTrue(autoTools.isAutoToolsProject("cases/simpleGraphAutoTools/TestCaseA"), "Failed to detect AutoTools project.")
        self.assertFalse(autoTools.isAutoToolsProject("cases/cmake/hello/main"), "False positive when given CMake project.")

    def test_isAutoToolsProject2(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = os.path.join(tempDir, "configure")
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(autoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject3(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = os.path.join(tempDir, "configure.in")
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(autoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_isAutoToolsProject4(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = os.path.join(tempDir, "configure.ac")
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(autoTools.isAutoToolsProject(tempDir), "Failed to detect AutoTools project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getInstallDir1(self):
        installDir = autoTools.getInstallDir("configure --prefix=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir2(self):
        installDir = autoTools.getInstallDir("./configure --prefix=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir3(self):
        installDir = autoTools.getInstallDir("./configure --prefix=/usr/local --with-A=/usr/local/a")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir4(self):
        installDir = autoTools.getInstallDir("./configure --prefix=foobarbaz")
        self.assertEquals(installDir, "foobarbaz", "Wrong install directory returned.")

    def test_getInstallDir5(self):
        installDir = autoTools.getInstallDir("./configure --prefix=")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir6(self):
        installDir = autoTools.getInstallDir("./configure --prefix= --with-A=/usr/local/a")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir7(self):
        installDir = autoTools.getInstallDir("test && ./configure --prefix= --with-A=/usr/local/a")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir8(self):
        #False positive
        installDir = autoTools.getInstallDir("./cmake --prefix=foobarbaz")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir9(self):
        #False positive
        installDir = autoTools.getInstallDir("./configure --prefixasdf=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir10(self):
        #False positive
        installDir = autoTools.getInstallDir("./configure --with-prefix=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir11(self):
        #False positive
        installDir = autoTools.getInstallDir("--with-prefix=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getDependencies1(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseA")
            success = autoTools.generateConfigureFiles(tempDir, "testCaseTarget", False)
            self.assertEquals(success, True, "Unable to generate build files.")
            dependencies = autoTools.getDependencies(tempDir, verbose=False)
            dependencies.sort()
            self.assertEquals(dependencies, ['testcaseb', 'testcasec'], "Wrong dependencies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies2(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseB")
            success = autoTools.generateConfigureFiles(tempDir, "testCaseTarget", False)
            self.assertEquals(success, True, "Unable to generate build files.")
            dependencies = autoTools.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, ['testcasec'], "Wrong dependencies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies3(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseC")
            success = autoTools.generateConfigureFiles(tempDir, "testCaseTarget", False)
            self.assertEquals(success, True, "Unable to generate build files.")
            dependencies = autoTools.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, ['testcased'], "Wrong dependencies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies4(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseD")
            success = autoTools.generateConfigureFiles(tempDir, "testCaseTarget", False)
            self.assertEquals(success, True, "Unable to generate build files.")
            dependencies = autoTools.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, [], "Wrong dependencies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies5(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/main")
            dependencies = autoTools.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, None, "Wrong dependencies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies6(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/hello1")
            dependencies = autoTools.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, None, "Wrong dependencies found in AutoTools project")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_autoTools))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
