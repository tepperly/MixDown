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

import os, socket, sys, unittest, mdTestUtilities
if not ".." in sys.path:
    sys.path.append("..")

from md import logger, utilityFunctions

class Test_MixDownShort(unittest.TestCase):
    def test_cmakeHello(self):
        try:
            mixDownPath = os.path.abspath("..")
            origPath = os.environ["PATH"]
            os.environ["PATH"] = mixDownPath + ":" + origPath

            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello")
            importRC = utilityFunctions.executeSubProcess("MixDown --import " + os.path.join(tempDir, "main") + " " + os.path.join(tempDir, "hello1"), tempDir)
            self.assertEquals(os.path.exists(os.path.join(tempDir, "main.md")), True, "MixDown project file does not exist after importing CMake Hello test case.")
            buildRC = utilityFunctions.executeSubProcess("MixDown main.md -ptestPrefix", tempDir)
            cleanRC = utilityFunctions.executeSubProcess("MixDown --clean main.md", tempDir)
            self.assertEquals(importRC, 0, "CMake Hello test case failed import.")
            self.assertEquals(buildRC, 0, "CMake Hello test case failed build.")
            self.assertEquals(cleanRC, 0, "CMake Hello test case failed clean.")
            prefix = os.path.join(tempDir, "testPrefix")
            binDir = os.path.join(prefix, "bin")
            libDir = os.path.join(prefix, "lib")
            self.assertEquals(os.path.exists(os.path.join(binDir, "hello")), True, "Executable does not exist after building CMake Hello test case.")
            self.assertEquals(os.path.exists(os.path.join(libDir, "libhello1.a")), True, "Library does not exist after building CMake Hello test case.")
        finally:
            utilityFunctions.removeDir(tempDir)
            os.environ["PATH"] = origPath

    def test_AutoToolsSimpleGraph(self):
        try:
            mixDownPath = os.path.abspath("..")
            origPath = os.environ["PATH"]
            os.environ["PATH"] = mixDownPath + ":" + origPath

            tempDir = mdTestUtilities.copyDirToTempDir("cases/simpleGraphAutoTools")
            importRC = utilityFunctions.executeSubProcess("MixDown --import " + os.path.join(tempDir, "TestCaseA") + " " + os.path.join(tempDir, "TestCaseB") + " " + os.path.join(tempDir, "TestCaseC") + " " + os.path.join(tempDir, "TestCaseD"), tempDir)
            self.assertEquals(os.path.exists(os.path.join(tempDir, "TestCaseA.md")), True, "MixDown project file does not exist after importing AutoTools Simple Graph test case.")
            buildRC = utilityFunctions.executeSubProcess("MixDown TestCaseA.md -ptestPrefix", tempDir)
            cleanRC = utilityFunctions.executeSubProcess("MixDown --clean TestCaseA.md", tempDir)
            self.assertEquals(importRC, 0, "AutoTools Simple Graph test case failed import.")
            self.assertEquals(buildRC, 0, "AutoTools Simple Graph test case failed build.")
            self.assertEquals(cleanRC, 0, "AutoTools Simple Graph test case failed clean.")
            prefix = os.path.join(tempDir, "testPrefix")
            binDir = os.path.join(prefix, "bin")
            self.assertEquals(os.path.exists(os.path.join(binDir, "TestCaseA")), True, "Executable A does not exist after building AutoTools Simple Graph test case.")
            self.assertEquals(os.path.exists(os.path.join(binDir, "TestCaseB")), True, "Executable B does not exist after building AutoTools Simple Graph test case.")
            self.assertEquals(os.path.exists(os.path.join(binDir, "TestCaseC")), True, "Executable C does not exist after building AutoTools Simple Graph test case.")
            self.assertEquals(os.path.exists(os.path.join(binDir, "TestCaseD")), True, "Executable D does not exist after building AutoTools Simple Graph test case.")
        finally:
            utilityFunctions.removeDir(tempDir)
            os.environ["PATH"] = origPath

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_MixDownShort))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
