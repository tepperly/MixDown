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
    def setUpTargetDirectory(self, filesInTarget=[]):
        self.testDir = mdTestUtilities.makeTempDir()
        for fileName in filesInTarget:
            open(os.path.join(self.testDir, fileName), 'w').close() #Create blank file
        self.options = mdOptions.Options()
        self.options.buildDir = os.path.join(self.testDir, "mdBuild")

    def tearDownTargetDirectory(self):
        if os.path.exists(self.testDir):
            utilityFunctions.removeDir(self.testDir)
        self.testDir = ""
        self.options = None

    def test_validate(self):
        options = mdOptions.Options()

        target = mdTarget.Target("", "")
        self.assertFalse(target.validate(options), "False positive returned when trying to validate target.")

        target.name = "foo"
        target.path = ""
        self.assertFalse(target.validate(options), "False positive returned when trying to validate target.")

        target.name = ""
        target.path = "/some/path"
        self.assertFalse(target.validate(options), "False positive returned when trying to validate target.")

        target.name = "foo"
        target.path = "/some/path"
        self.assertTrue(target.validate(options), "Target should have validated.")

    def test_steps(self):
        target = mdTarget.Target("foo", "/some/path")
        target.skipSteps = ["b"]
        self.assertFalse(target.hasStep("b"), "Specified skipped step was not skipped")
        self.assertTrue(target.hasStep("a"), "Specified skipped step was not skipped")

    def test_examine(self):
        options = mdOptions.Options()
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.examine(options)
        returnValue = target.commands["preconfig"] == "autoreconf -i"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        returnValue = target.commands["config"] == "./configure --prefix=/usr/local"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        returnValue = target.commands["build"] == "make"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        returnValue = target.commands["install"] == "make install"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithJobSlots(self):
        options = mdOptions.Options()
        options.processCommandline(["test", "-j4"])
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.examine(options)
        returnValue = target.commands["preconfig"] == "autoreconf -i"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        returnValue = target.commands["config"] == "./configure --prefix=/usr/local"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        returnValue = target.commands["build"] == "make -j4"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        returnValue = target.commands["install"] == "make -j4 install"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithDependancies(self):
        options = mdOptions.Options()
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.dependsOn = ["TestCaseB", "TestCaseC"]
        target.examine(options)
        returnValue = target.commands["preconfig"] == "autoreconf -i"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        returnValue = target.commands["config"] == "./configure --prefix=/usr/local --with-TestCaseB=/usr/local --with-TestCaseC=/usr/local"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        returnValue = target.commands["build"] == "make"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        returnValue = target.commands["install"] == "make install"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithDependanciesWithPrefix(self):
        options = mdOptions.Options()
        options.processCommandline(["test", "-p/test/path"])
        target = mdTarget.Target("TestCaseA", "cases/simpleGraphAutoTools/TestCaseA")
        target.dependsOn = ["TestCaseB", "TestCaseC"]
        target.examine(options)
        returnValue = target.commands["preconfig"] == "autoreconf -i"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong preconfig command")
        returnValue = target.commands["config"] == "./configure --prefix=/test/path --with-TestCaseB=/test/path --with-TestCaseC=/test/path"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong config command")
        returnValue = target.commands["build"] == "make"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong build command")
        returnValue = target.commands["install"] == "make install"
        self.assertTrue(returnValue, "'cases/simpleGraphAutoTools/TestCaseA' returned wrong install command")

    def test_examineWithOnlyMakefile(self):
        try:
            self.setUpTargetDirectory(["Makefile"])
            self.options.processCommandline(["test", "-p/test/path"])
            target = mdTarget.Target("OnlyMakefile", self.testDir)
            target.examine(self.options)
        finally:
            self.tearDownTargetDirectory()
        returnValue = target.commands["preconfig"] == ""
        self.assertTrue(returnValue, "Target with only Makefile returned a preconfig command when it should not have")
        returnValue = target.commands["config"] == ""
        self.assertTrue(returnValue, "Target with only Makefile returned a config command when it should not have")
        returnValue = target.commands["build"] == "make"
        self.assertTrue(returnValue, "Target with only Makefile returned wrong build command")
        returnValue = target.commands["install"] == "make install"
        self.assertTrue(returnValue, "Target with only Makefile returned wrong install command")

    def test_examineWithAutoTools(self):
        try:
            self.setUpTargetDirectory(["Makefile.am", "configure.ac"])
            self.options.processCommandline(["test", "-p/test/path"])
            target = mdTarget.Target("AutoTools", self.testDir)
            target.examine(self.options)
        finally:
            self.tearDownTargetDirectory()
        returnValue = target.commands["preconfig"] == "autoreconf -i"
        self.assertTrue(returnValue, "Target with autotool files returned wrong preconfig command")
        returnValue = target.commands["config"] == "./configure --prefix=/test/path"
        self.assertTrue(returnValue, "Target with autotool files returned wrong config command")
        returnValue = target.commands["build"] == "make"
        self.assertTrue(returnValue, "Target with autotool files returned wrong build command")
        returnValue = target.commands["install"] == "make install"
        self.assertTrue(returnValue, "Target with autotool files returned wrong install command")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdTarget))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()