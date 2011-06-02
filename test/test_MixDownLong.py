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

import os, socket, sys, unittest, mdTestUtilities
if not ".." in sys.path:
    sys.path.append("..")
import mdLogger, utilityFunctions

class Test_MixDownLong(unittest.TestCase):
    def test_cmakeHello(self):
        try:
            tempDir = mdTestUtilities.copyDirToTempDir("cases/cmake/hello")
            importRC = utilityFunctions.executeSubProcess("MixDown --import " + os.path.join(tempDir, "main") + " " + os.path.join(tempDir, "hello1"), tempDir)
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

    def test_subversion(self):
        if socket.gethostname() == "tux316.llnl.gov":
            pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_MixDownLong))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()