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
import md.mdCMake, md.mdLogger, md.utilityFunctions

class Test_mdCMake(unittest.TestCase):
    def test_isCMakeProject1(self):
        self.assertTrue(md.mdCMake.isCMakeProject("cases/cmake/hello/hello1"), "Failed to detect CMake project.")
        self.assertTrue(md.mdCMake.isCMakeProject("cases/cmake/hello/main"), "Failed to detect CMake project.")
        self.assertFalse(md.mdCMake.isCMakeProject("cases/simpleGraphAutoTools/TestCaseA"), "False positive when given CMake project.")

    def test_isCMakeProject2(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = os.path.join(tempDir, "CMakeLists.txt")
            mdTestUtilities.createBlankFile(tempFile)
            self.assertTrue(md.mdCMake.isCMakeProject(tempDir), "Failed to detect CMake project.")
        finally:
            md.utilityFunctions.removeDir(tempDir)

    def test_getInstallDir1(self):
        installDir = md.mdCMake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir2(self):
        installDir = md.mdCMake.getInstallDir("cmake -DCMAKE_PREFIX_PATH=/usr/foo -DCMAKE_INSTALL_PREFIX=/usr/local")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir3(self):
        installDir = md.mdCMake.getInstallDir("cmake -DCMAKE_PREFIX_PATH=/usr/foo -DCMAKE_INSTALL_PREFIX=/usr/local ../")
        self.assertEquals(installDir, "/usr/local", "Wrong install directory returned.")

    def test_getInstallDir4(self):
        installDir = md.mdCMake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX=someRelativePath")
        self.assertEquals(installDir, "someRelativePath", "Wrong install directory returned.")

    def test_getInstallDir5(self):
        installDir = md.mdCMake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX=")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir6(self):
        installDir = md.mdCMake.getInstallDir("cmake -DCMAKE_INSTALL_PREFIX= -DCMAKE_PREFIX_PATH=/usr/foo")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir7(self):
        installDir = md.mdCMake.getInstallDir("test && .cmake -DCMAKE_INSTALL_PREFIX= -DCMAKE_PREFIX_PATH=/usr/foo")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir8(self):
        #False positive
        installDir = md.mdCMake.getInstallDir("./cmake --prefix=foobarbaz")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir9(self):
        #False positive
        installDir = md.mdCMake.getInstallDir("./configure -DCMAaKE_PREaFIX_aPATH=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir10(self):
        #False positive
        installDir = md.mdCMake.getInstallDir("./configure -CMAKE_PREFIX_PATH=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getInstallDir11(self):
        #False positive
        installDir = md.mdCMake.getInstallDir("-DCMAKE_PREFIX_PATH=temp/")
        self.assertEquals(installDir, "", "Wrong install directory returned.")

    def test_getDependancies1(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/main")
            dependancies = md.mdCMake.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, ['hello1'], "Wrong dependancies found in CMake project")
        finally:
            md.utilityFunctions.removeDir(tempDir)

    def test_getDependancies2(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello/hello1")
            dependancies = md.mdCMake.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, [], "Wrong dependancies found in CMake project")
        finally:
            md.utilityFunctions.removeDir(tempDir)

    def test_getDependancies3(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/ogre3dBuildFilesOnly")
            dependancies = md.mdCMake.getDependancies(tempDir, verbose=False)
            dependancies.sort()
            self.assertEquals(dependancies, ['boost', 'carbon', 'cg', 'cocoa',
                                             'cppunit', 'd3d10', 'd3d11', 'd3d9', 'd3dcompiler', 'd3dx10',
                                             'd3dx11', 'd3dx9', 'directx', 'dl', 'doxygen', 'dxerr', 'dxgi',
                                             'dxguid', 'freeimage', 'freetype', 'iokit', 'iphonesdk', 'ois',
                                             'opengl', 'opengles', 'opengles2', 'pkgconfig', 'poco', 'tbb',
                                             'x11', 'xaw', 'zlib', 'zzip'],
                              "Wrong dependancies found in CMake project")
        finally:
            md.utilityFunctions.removeDir(tempDir)

    def test_getDependanciesFalse1(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseA")
            dependancies = md.mdCMake.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, None, "Wrong dependancies found in CMake project")
        finally:
            md.utilityFunctions.removeDir(tempDir)

    def test_getDependanciesFalse2(self):
        #False positive
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools/TestCaseB")
            dependancies = md.mdCMake.getDependancies(tempDir, verbose=False)
            self.assertEquals(dependancies, None, "Wrong dependancies found in CMake project")
        finally:
            md.utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdCMake))
    return suite

if __name__ == "__main__":
    md.mdLogger.SetLogger("Console")
    unittest.main()
