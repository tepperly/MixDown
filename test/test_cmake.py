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

from md import cmake, logger, utilityFunctions

class Test_cmake(unittest.TestCase):
    def test_isCMakeProject1(self):
        self.assertTrue(cmake.isCMakeProject("cases/cmake/hello/hello1"), "Failed to detect CMake project.")
        self.assertTrue(cmake.isCMakeProject("cases/cmake/hello/main"), "Failed to detect CMake project.")
        self.assertFalse(cmake.isCMakeProject("cases/simpleGraphAutoTools/TestCaseA"), "False positive when given CMake project.")

    def test_isCMakeProject2(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = os.path.join(tempDir, "CMakeLists.txt")
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(cmake.isCMakeProject(tempDir), "Failed to detect CMake project.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getInstallDir1(self):
        installDir = cmake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir2(self):
        installDir = cmake.getInstallDir("cmake -DCMAKE_PREFIX_PATH=/usr/foo -DCMAKE_INSTALL_PREFIX=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir3(self):
        installDir = cmake.getInstallDir("cmake -DCMAKE_PREFIX_PATH=/usr/foo -DCMAKE_INSTALL_PREFIX=/usr/local ../")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir4(self):
        installDir = cmake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX=someRelativePath")
        self.assertEquals(installDir, "someRelativePath", "Wrong install directory returned.")

    def test_getInstallDir5(self):
        installDir = cmake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX=")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir6(self):
        installDir = cmake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX= -DCMAKE_PREFIX_PATH=/usr/foo")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir7(self):
        installDir = cmake.getInstallDir("test && .cmake -DCMAKE_INSTALL_PREFIX= -DCMAKE_PREFIX_PATH=/usr/foo")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir8(self):
        #False positive
        installDir = cmake.getInstallDir("./cmake --prefix=foobarbaz")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir9(self):
        #False positive
        installDir = cmake.getInstallDir("./configure -DCMAaKE_PREaFIX_aPATH=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir10(self):
        #False positive
        installDir = cmake.getInstallDir("./configure -CMAKE_PREFIX_PATH=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir11(self):
        #False positive
        installDir = cmake.getInstallDir("-DCMAKE_PREFIX_PATH=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getDependencies1(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/main")
            dependencies = cmake.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, ['hello1'], "Wrong dependencies found in CMake project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies2(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/hello1")
            dependencies = cmake.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, [], "Wrong dependencies found in CMake project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependencies3(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/ogre3dBuildFilesOnly")
            dependencies = cmake.getDependencies(tempDir, verbose=False)
            dependencies.sort()
            self.assertEquals(dependencies, ['boost', 'carbon', 'cg', 'cocoa',
                                             'cppunit', 'd3d10', 'd3d11', 'd3d9', 'd3dcompiler', 'd3dx10',
                                             'd3dx11', 'd3dx9', 'directx', 'dl', 'doxygen', 'dxerr', 'dxgi',
                                             'dxguid', 'freeimage', 'freetype', 'iokit', 'iphonesdk', 'ois',
                                             'opengl', 'opengles', 'opengles2', 'pkgconfig', 'poco', 'tbb',
                                             'x11', 'xaw', 'zlib', 'zzip'],
                              "Wrong dependencies found in CMake project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependenciesFalse1(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseA")
            dependencies = cmake.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, None, "Wrong dependencies found in CMake project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_getDependenciesFalse2(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseB")
            dependencies = cmake.getDependencies(tempDir, verbose=False)
            self.assertEquals(dependencies, None, "Wrong dependencies found in CMake project")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_cmake))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
