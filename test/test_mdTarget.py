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
import mdCvs, mdSvn, mdGit, mdHg, mdLogger, mdOptions, mdTarget, utilityFunctions

class Test_mdTarget(unittest.TestCase):
    def test_determineOutputPath1(self):
        options = mdOptions.Options()
        options.buildDir = "."
        target = mdTarget.Target("foo", "/bar/paz")
        target.outputPathSpecified = True
        target.outputPath = "/outputPath"
        target.outputPath = target.determineOutputPath(options)
        self.assertEquals(target.outputPath, "/outputPath", "Specified output path was overwritten by determineOutputPath.")

    def test_determineOutputPath2(self):
        options = mdOptions.Options()
        options.buildDir = "."
        target = mdTarget.Target("foo", "/bar/paz")
        target.outputPathSpecified = False
        target.outputPath = "/outputPath/"
        target.outputPath = target.determineOutputPath(options)
        self.assertEquals(target.outputPath, "./foo", "Unspecified output path was not overwritten by determineOutputPath.")

    def test_determineOutputPath3(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            options = mdOptions.Options()
            options.buildDir = "."
            options.cleanTargets = True
            target = mdTarget.Target("foo", targetDir)
            target.outputPath = target.determineOutputPath(options)
            self.assertEquals(target.outputPath, targetDir, "During cleaning found target path should not be overwritten.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_determineOutputPath4(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "foo")
            os.makedirs(targetDir)
            options = mdOptions.Options()
            options.buildDir = "."
            options.cleanTargets = True
            options.buildDir = tempDir
            target = mdTarget.Target("foo", targetDir)
            target.outputPath = target.determineOutputPath(options)
            self.assertEquals(target.outputPath, targetDir, "During cleaning found target path should not be overwritten.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validate1(self):
        options = mdOptions.Options()
        target = mdTarget.Target("", "")
        self.assertEquals(target.validate(options), False, "False positive returned when trying to validate target.")

    def test_validate2(self):
        options = mdOptions.Options()
        target = mdTarget.Target("foo", "")
        self.assertEquals(target.validate(options), False, "False positive returned when trying to validate target.")

    def test_validate3(self):
        options = mdOptions.Options()
        target = mdTarget.Target("", "/some/path")
        self.assertEquals(target.validate(options), False, "False positive returned when trying to validate target.")

    def test_validate4(self):
        options = mdOptions.Options()
        target = mdTarget.Target("foo", "/some/path")
        self.assertEquals(target.validate(options), True, "Target should have validated.")

    def test_steps(self):
        target = mdTarget.Target("foo", "/some/path")
        target.skipSteps = ["b"]
        self.assertEquals(target.isStepToBeSkipped("b"), True, "Specified skipped step was not skipped")
        self.assertEquals(target.isStepToBeSkipped("a"), False, "Specified step was skipped")

    def test_examine(self):
        options = mdOptions.Options()
        options.buildDir = "."
        options.importer = True
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.examine(options)
        target.expandDefines(options)
        self.assertEquals(target.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(target.findBuildStep("config").command, "./configure --prefix=/usr/local", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(target.findBuildStep("build").command, "make", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(target.findBuildStep("install").command, "make install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithJobSlots(self):
        options = mdOptions.Options()
        options.buildDir = "."
        options.importer = True
        options.processCommandline(["test", "-j4"])
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.examine(options)
        target.expandDefines(options)
        self.assertEquals(target.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(target.findBuildStep("config").command, "./configure --prefix=/usr/local", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(target.findBuildStep("build").command, "make -j4", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(target.findBuildStep("install").command, "make -j4 install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithDependancies(self):
        options = mdOptions.Options()
        options.buildDir = "."
        options.importer = True
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.dependsOn = ["TestCaseB", "TestCaseC"]
        target.examine(options)
        target.expandDefines(options)
        self.assertEquals(target.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(target.findBuildStep("config").command, "./configure --prefix=/usr/local --with-TestCaseB=/usr/local --with-TestCaseC=/usr/local", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(target.findBuildStep("build").command, "make", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(target.findBuildStep("install").command, "make install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithDependanciesWithPrefix(self):
        options = mdOptions.Options()
        options.buildDir = "."
        options.importer = True
        options.processCommandline(["test", "-p/test/path"])
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.dependsOn = ["TestCaseB", "TestCaseC"]
        target.examine(options)
        target.expandDefines(options)
        self.assertEquals(target.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(target.findBuildStep("config").command, "./configure --prefix=/test/path --with-TestCaseB=/test/path --with-TestCaseC=/test/path", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(target.findBuildStep("build").command, "make", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(target.findBuildStep("install").command, "make install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithOnlyMakefile(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            mdTestUtilities.createBlankFile(os.path.join(targetDir, "Makefile"))
            options = mdOptions.Options()
            options.buildDir = os.path.join(tempDir, options.buildDir)
            options.importer = True
            target = mdTarget.Target("OnlyMakefile", targetDir)
            target.examine(options)
            target.expandDefines(options)
            self.assertEquals(target.findBuildStep("preconfig").command, "", "Target with only Makefile returned a preconfig command when it should not have")
            self.assertEquals(target.findBuildStep("config").command, "", "Target with only Makefile returned a config command when it should not have")
            self.assertEquals(target.findBuildStep("build").command, "make", "Target with only Makefile returned wrong build command")
            self.assertEquals(target.findBuildStep("install").command, "make install", "Target with only Makefile returned wrong install command")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_examineWithAutoTools(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            mdTestUtilities.createBlankFiles(targetDir, ["Makefile.am", "configure.ac"])
            options = mdOptions.Options()
            options.buildDir = os.path.join(tempDir, options.buildDir)
            options.importer = True
            target = mdTarget.Target("AutoTools", targetDir)
            target.examine(options)
            target.expandDefines(options)
            self.assertEquals(target.findBuildStep("preconfig").command, "autoreconf -i", "Target with autotool files returned wrong preconfig command")
            self.assertEquals(target.findBuildStep("config").command, "./configure --prefix=/usr/local", "Target with autotool files returned wrong config command")
            self.assertEquals(target.findBuildStep("build").command, "make", "Target with autotool files returned wrong build command")
            self.assertEquals(target.findBuildStep("install").command, "make install", "Target with autotool files returned wrong install command")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_examineWithAutoToolsWithPrefix(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            mdTestUtilities.createBlankFiles(targetDir, ["Makefile.am", "configure.ac"])
            options = mdOptions.Options()
            options.processCommandline(["test", "-p/test/prefix"])
            options.buildDir = os.path.join(tempDir, options.buildDir)
            options.importer = True
            target = mdTarget.Target("AutoTools", targetDir)
            target.examine(options)
            target.expandDefines(options)
            self.assertEquals(target.findBuildStep("preconfig").command, "autoreconf -i", "Target with autotool files returned wrong preconfig command")
            self.assertEquals(target.findBuildStep("config").command, "./configure --prefix=/test/prefix", "Target with autotool files returned wrong config command")
            self.assertEquals(target.findBuildStep("build").command, "make", "Target with autotool files returned wrong build command")
            self.assertEquals(target.findBuildStep("install").command, "make install", "Target with autotool files returned wrong install command")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdTarget))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()