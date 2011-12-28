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

from md import options, logger, utilityFunctions

class Test_options(unittest.TestCase):
    def test_processCommandline01(self):
        testOptions = options.Options()
        commandline = "MixDown --clean --import"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should not have processed correctly")

    def test_processCommandline02(self):
        testOptions = options.Options()
        commandline = "MixDown --clean"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should not have processed correctly")

    def test_processCommandline03(self):
        testOptions = options.Options()
        commandline = "MixDown --import"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should not have processed correctly")

    def test_processCommandline04(self):
        testOptions = options.Options()
        commandline = "MixDown"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should not have processed correctly")

    def test_validate01(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown " + projectFilePath + " -ptestPrefix -v -otestOverrides -ggcc,debug,parallel"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command line should have processed correctly")
            self.assertEquals(testOptions.validate(), True, "Command line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validate02(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown " + projectFilePath + " -ptestPrefix -v -ggcc,debug,parallel"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command line should have processed correctly")
            self.assertEquals(testOptions.validate(), False, "Commandline options should not have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_options))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
