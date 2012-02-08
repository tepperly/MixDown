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

from md import defines, options, logger, utilityFunctions

class Test_options(unittest.TestCase):
    def test_processCommandline01(self):
        testOptions = options.Options()
        commandline = "MixDown --clean --import"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")

    def test_processCommandline02(self):
        testOptions = options.Options()
        commandline = "MixDown --clean"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")

    def test_processCommandline03(self):
        testOptions = options.Options()
        commandline = "MixDown --import"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")

    def test_processCommandline04(self):
        testOptions = options.Options()
        commandline = "MixDown"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")

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
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 3, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "neon", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, url, "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[2].name, "c", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[2].path, directory, "Target had wrong name")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline06(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown --import " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline07(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown --import " + tarPath + " " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 2, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[1].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline08(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown " + tarPath + " --import"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline09(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown " + tarPath + " --import --clean"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
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
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
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
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
            self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
            self.assertEquals(testOptions.projectFile, "", "projectFile should not have been set")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline12(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)

            testOptions = options.Options()
            commandline = "MixDown --import -otestOverrides -gfail,hopefully,please"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
            self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
            self.assertEquals(testOptions.overrideFile, "", "overrideFile should not have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "", "compilerGroupName should not have been set")
            self.assertEquals(testOptions.optimizationGroupName, "", "optimizationGroupName should not have been set")
            self.assertEquals(testOptions.parallelGroupName, "", "parallelGroupName should not have been set")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline13(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)

            testOptions = options.Options()
            commandline = "MixDown --import -otestOverrides"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
            self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
            self.assertEquals(testOptions.overrideFile, "", "overrideFile should not have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "", "compilerGroupName should not have been set")
            self.assertEquals(testOptions.optimizationGroupName, "", "optimizationGroupName should not have been set")
            self.assertEquals(testOptions.parallelGroupName, "", "parallelGroupName should not have been set")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline14(self):
        testOptions = options.Options()
        commandline = "MixDown --import -sapr:preconfig"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.skipSteps, "", "skipSteps should not have been set")

    def test_processCommandline15(self):
        testOptions = options.Options()
        commandline = "MixDown --import -k"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.cleanMixDown, True, "cleanMixDown should not have been set")

    def test_processCommandline16(self):
        testOptions = options.Options()
        commandline = "MixDown --import -v"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.verbose, True, "verbose should have been set")

    def test_processCommandline17(self):
        testOptions = options.Options()
        commandline = "MixDown --import -wtest"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.downloadDir, "mdDownload", "downloadDir should not have been set")

    def test_processCommandline18(self):
        testOptions = options.Options()
        commandline = "MixDown --import -btest"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.buildDir, "mdBuild", "buildDir should not have been set")

    def test_processCommandline19(self):
        testOptions = options.Options()
        commandline = "MixDown --import -j9"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.defines[defines.surround(defines.mdJobSlots[0])], "", "cleanMixDown should not have been set")

    def test_processCommandline20(self):
        testOptions = options.Options()
        commandline = "MixDown --import -lconsole"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.logger, "file", "logger should not have been set")

    def test_processCommandline21(self):
        testOptions = options.Options()
        commandline = "MixDown --import -ptest"
        self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
        self.assertEquals(testOptions.targetsToImport, [], "targetsToImport should have not been set")
        self.assertEquals(testOptions.defines[defines.surround(defines.mdPrefix[0])], "/usr/local", "prefix should not have been set")

    def test_processCommandline22(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown -v -i --import " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.verbose, True, "verbose should have been set")
            self.assertEquals(testOptions.interactive, True, "interactive should have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline23(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown -v --import " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.verbose, True, "verbose should have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline24(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarFile = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarFile)

            testOptions = options.Options()
            commandline = "MixDown -i --import " + tarPath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(len(testOptions.targetsToImport), 1, "Number of targets to import was wrong")
            self.assertEquals(testOptions.targetsToImport[0].name, "test", "Target had wrong name")
            self.assertEquals(testOptions.targetsToImport[0].path, tarPath, "Target had wrong name")
            self.assertEquals(testOptions.interactive, True, "interactive should have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline25(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown -o" + overrideFilePath + " -ga,b,c " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(testOptions.overrideFile, overrideFilePath, "overrideFile should have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "a", "compilerGroupName should have been set")
            self.assertEquals(testOptions.optimizationGroupName, "b", "optimizationGroupName should have been set")
            self.assertEquals(testOptions.parallelGroupName, "c", "parallelGroupName should have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline26(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown -o" + overrideFilePath + " -ga,b, " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(testOptions.overrideFile, overrideFilePath, "overrideFile should have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "a", "compilerGroupName should have been set")
            self.assertEquals(testOptions.optimizationGroupName, "b", "optimizationGroupName should have been set")
            self.assertEquals(testOptions.parallelGroupName, "", "parallelGroupName should not have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline27(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown -o" + overrideFilePath + " -ga,,c " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(testOptions.overrideFile, overrideFilePath, "overrideFile should have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "a", "compilerGroupName should have been set")
            self.assertEquals(testOptions.optimizationGroupName, "", "optimizationGroupName should not have been set")
            self.assertEquals(testOptions.parallelGroupName, "c", "parallelGroupName should have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline28(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown -o" + overrideFilePath + " -g,b,c " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(testOptions.overrideFile, overrideFilePath, "overrideFile should have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "", "compilerGroupName should not have been set")
            self.assertEquals(testOptions.optimizationGroupName, "b", "optimizationGroupName should have been set")
            self.assertEquals(testOptions.parallelGroupName, "c", "parallelGroupName should have been set")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_processCommandline29(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            overrideFilePath = os.path.join(tempDir, "testOverrides")
            mdTestUtilities.createBlankFile(overrideFilePath)
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown -o" + overrideFilePath + " -g,, " + projectFilePath
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), False, "Command-line should not have processed correctly")
            self.assertEquals(testOptions.overrideFile, overrideFilePath, "overrideFile should have been set")
            self.assertEquals(testOptions.overrideGroup, None, "overrideGroup should not have been set")
            self.assertEquals(testOptions.compilerGroupName, "", "compilerGroupName should have been set")
            self.assertEquals(testOptions.optimizationGroupName, "", "optimizationGroupName should have been set")
            self.assertEquals(testOptions.parallelGroupName, "", "parallelGroupName should have been set")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validate01(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown " + projectFilePath + " -ptestPrefix -v -otestOverrides -ggcc,debug,parallel"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(testOptions.validate(), True, "Command-line options should have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validate02(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = os.path.join(tempDir, "test.md")
            mdTestUtilities.createBlankFile(projectFilePath)

            testOptions = options.Options()
            commandline = "MixDown " + projectFilePath + " -ptestPrefix -v -ggcc,debug,parallel"
            self.assertEquals(testOptions.processCommandline(commandline.split(" ")), True, "Command-line should have processed correctly")
            self.assertEquals(testOptions.validate(), False, "Command-line options should not have validated")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_options))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
