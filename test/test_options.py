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

    def test_processCommandline05(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            url = "http://www.webdav.org/neon/neon-0.29.5.tar.gz"
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)
            directory = os.path.join(tempDir, "c")
            os.mkdir(directory)

            testOptions = options.Options()
            commandline = "MixDown --import " + url + " " + tarPath + " " + directory
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 3, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "neon", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, url, "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[2].name, "c", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[2].path, directory, "Target had wrong name")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline06(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown --import " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline07(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown --import " + tarPath + " " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 2, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].path, tarPath, "Target had wrong name")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline08(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown " + tarPath + " --import"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline09(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown " + tarPath + " --import --clean"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should have processed correctly")
            self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline10(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown " + tarPath + " --import --clean " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should have processed correctly")
            self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
            self.assertEquals(testOptions.projectFile, "", "projectFile should not have been set")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline11(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown " + tarPath + " " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command line should have processed correctly")
            self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
            self.assertEquals(testOptions.projectFile, "", "projectFile should not have been set")
        finally:
            utilityFunctions.removeDir(tempDir)

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
