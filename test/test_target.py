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

from md import cvs, svn, git, hg, logger, options, target, utilityFunctions
import md

class Test_target(unittest.TestCase):
    def test_determineOutputPath1(self):
        option = options.Options()
        option.buildDir = "."
        targets = target.Target("foo", "/bar/paz")
        targets.outputPathSpecified = True
        targets.outputPath = "/outputPath"
        targets.outputPath = targets.determineOutputPath(option)
        self.assertEquals(targets.outputPath, "/outputPath", "Specified output path was overwritten by determineOutputPath.")

    def test_determineOutputPath2(self):
        option = options.Options()
        option.buildDir = "."
        targets = target.Target("foo", "/bar/paz")
        targets.outputPathSpecified = False
        targets.outputPath = "/outputPath/"
        targets.outputPath = targets.determineOutputPath(option)
        self.assertEquals(targets.outputPath, "./foo", "Unspecified output path was not overwritten by determineOutputPath.")

    def test_determineOutputPath3(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            option = options.Options()
            option.buildDir = "."
            option.cleanTargets = True
            targets = target.Target("foo", targetDir)
            targets.outputPath = targets.determineOutputPath(option)
            self.assertEquals(targets.outputPath, targetDir, "During cleaning found target path should not be overwritten.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_determineOutputPath4(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "foo")
            os.makedirs(targetDir)
            option = options.Options()
            option.buildDir = "."
            option.cleanTargets = True
            option.buildDir = tempDir
            targets = target.Target("foo", targetDir)
            targets.outputPath = targets.determineOutputPath(option)
            self.assertEquals(targets.outputPath, targetDir, "During cleaning found target path should not be overwritten.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validate1(self):
        option = options.Options()
        targets = target.Target("", "")
        self.assertEquals(targets.validate(option), False, "False positive returned when trying to validate target.")

    def test_validate2(self):
        option = options.Options()
        targets = target.Target("foo", "")
        self.assertEquals(targets.validate(option), False, "False positive returned when trying to validate target.")

    def test_validate3(self):
        option = options.Options()
        targets = target.Target("", "/some/path")
        self.assertEquals(targets.validate(option), False, "False positive returned when trying to validate target.")

    def test_validate4(self):
        option = options.Options()
        targets = target.Target("foo", "/some/path")
        self.assertEquals(targets.validate(option), True, "Target should have validated.")

    def test_steps(self):
        targets = target.Target("foo", "/some/path")
        targets.skipSteps = ["b"]
        self.assertEquals(targets.isStepToBeSkipped("b"), True, "Specified skipped step was not skipped")
        self.assertEquals(targets.isStepToBeSkipped("a"), False, "Specified step was skipped")

    def test_examine(self):
        option = options.Options()
        option.buildDir = "."
        option.importer = True
        targets = target.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        targets.examine(option)
        targets.expandDefines(option)
        self.assertEquals(targets.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(targets.findBuildStep("config").command, "./configure --prefix=/usr/local", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(targets.findBuildStep("build").command, "make", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(targets.findBuildStep("install").command, "make install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithJobSlots(self):
        option = options.Options()
        option.buildDir = "."
        option.importer = True
        option.processCommandline(["test", "-j4"])
        targets = target.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        targets.examine(option)
        targets.expandDefines(option)
        self.assertEquals(targets.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(targets.findBuildStep("config").command, "./configure --prefix=/usr/local", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(targets.findBuildStep("build").command, "make -j4", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(targets.findBuildStep("install").command, "make -j4 install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithDependencies(self):
        option = options.Options()
        option.buildDir = "."
        option.importer = True
        targets = target.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        targets.dependsOn = ["TestCaseB", "TestCaseC"]
        targets.examine(option)
        targets.expandDefines(option)
        self.assertEquals(targets.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(targets.findBuildStep("config").command, "./configure --prefix=/usr/local --with-TestCaseB=/usr/local --with-TestCaseC=/usr/local", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(targets.findBuildStep("build").command, "make", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(targets.findBuildStep("install").command, "make install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithDependenciesWithPrefix(self):
        option = options.Options()
        option.buildDir = "."
        option.importer = True
        option.processCommandline(["test", "-p/test/path"])
        targets = target.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        targets.dependsOn = ["TestCaseB", "TestCaseC"]
        targets.examine(option)
        targets.expandDefines(option)
        self.assertEquals(targets.findBuildStep("preconfig").command, "autoreconf -i", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        self.assertEquals(targets.findBuildStep("config").command, "./configure --prefix=/test/path --with-TestCaseB=/test/path --with-TestCaseC=/test/path", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        self.assertEquals(targets.findBuildStep("build").command, "make", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        self.assertEquals(targets.findBuildStep("install").command, "make install", "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithOnlyMakefile(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            mdTestUtilities.createBlankFile(os.path.join(targetDir, "Makefile"))
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            option.importer = True
            targets = target.Target("OnlyMakefile", targetDir)
            targets.examine(option)
            targets.expandDefines(option)
            self.assertEquals(targets.findBuildStep("preconfig").command, "", "Target with only Makefile returned a preconfig command when it should not have")
            self.assertEquals(targets.findBuildStep("config").command, "", "Target with only Makefile returned a config command when it should not have")
            self.assertEquals(targets.findBuildStep("build").command, "make", "Target with only Makefile returned wrong build command")
            self.assertEquals(targets.findBuildStep("install").command, "make install", "Target with only Makefile returned wrong install command")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_examineWithAutoTools(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            mdTestUtilities.createBlankFiles(targetDir, ["Makefile.am", "configure.ac"])
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            option.importer = True
            targets = target.Target("AutoTools", targetDir)
            targets.examine(option)
            targets.expandDefines(option)
            self.assertEquals(targets.findBuildStep("preconfig").command, "autoreconf -i", "Target with autotool files returned wrong preconfig command")
            self.assertEquals(targets.findBuildStep("config").command, "./configure --prefix=/usr/local", "Target with autotool files returned wrong config command")
            self.assertEquals(targets.findBuildStep("build").command, "make", "Target with autotool files returned wrong build command")
            self.assertEquals(targets.findBuildStep("install").command, "make install", "Target with autotool files returned wrong install command")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_examineWithAutoToolsWithPrefix(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            targetDir = os.path.join(tempDir, "targetDir")
            os.makedirs(targetDir)
            mdTestUtilities.createBlankFiles(targetDir, ["Makefile.am", "configure.ac"])
            option = options.Options()
            option.processCommandline(["test", "-p/test/prefix"])
            option.buildDir = os.path.join(tempDir, option.buildDir)
            option.importer = True
            targets = target.Target("AutoTools", targetDir)
            targets.examine(option)
            targets.expandDefines(option)
            self.assertEquals(targets.findBuildStep("preconfig").command, "autoreconf -i", "Target with autotool files returned wrong preconfig command")
            self.assertEquals(targets.findBuildStep("config").command, "./configure --prefix=/test/prefix", "Target with autotool files returned wrong config command")
            self.assertEquals(targets.findBuildStep("build").command, "make", "Target with autotool files returned wrong build command")
            self.assertEquals(targets.findBuildStep("install").command, "make install", "Target with autotool files returned wrong install command")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_target))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
