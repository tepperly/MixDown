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

import os, sys, textwrap, unittest, mdTestUtilities

if not ".." in sys.path:
    sys.path.append("..")
import mdLogger, mdOptions, mdProject, utilityFunctions

class Test_mdProject(unittest.TestCase):
    def test_readSingleTargetProject(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            PreConfig: autoreconf -i
                                            Config: ./configure --prefix=$(_prefix)
                                            Build: make
                                            Install: make install
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            self.assertTrue(project.read(), "Project file could not be read")
            #Project
            self.assertEqual(project.name, os.path.split(projectFilePath)[1][:-3], "Project returned wrong name")
            self.assertEqual(project.path, projectFilePath, "Project returned wrong path")
            #Target a
            self.assertEqual(project.targets[0].name, "a", "Project returned wrong target 'a' name")
            self.assertEqual(project.targets[0].path, "a-1.11.tar.gz", "Project returned wrong target 'a' path")
            self.assertEqual(project.targets[0].commands["preconfig"], "autoreconf -i", "Project returned wrong target 'a' preconfig command")
            self.assertEqual(project.targets[0].commands["config"], "./configure --prefix=$(_prefix)", "Project returned wrong target 'a' config command")
            self.assertEqual(project.targets[0].commands["build"], "make", "Project returned wrong target 'a' build command")
            self.assertEqual(project.targets[0].commands["install"], "make install", "Project returned wrong target 'a' install command")
        finally:
            os.remove(projectFilePath)

    def test_readDetectDuplicateTarget(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: a
                                            Path: a-1.11.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            self.assertFalse(project.read(), "Project read should have detected duplicate target")
        finally:
            os.remove(projectFilePath)

    def test_readMultiTargetProject(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b, c
                                            PreConfig: autoreconf -i
                                            Config: ./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)
                                            Build: make
                                            Install: make install

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c
                                            PreConfig: bautoreconf -i
                                            Config: ./configure --prefix=$(_prefix) --with-c=$(_prefix)
                                            Build: bmake
                                            Install: bmake install

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            PreConfig: cautoreconf -i
                                            Config: ./configure --prefix=$(_prefix)
                                            Build: cmake
                                            Install: cmake install
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            self.assertTrue(project.read(), "Project file could not be read")
            #Project
            self.assertEqual(project.name, os.path.split(projectFilePath)[1][:-3], "Project returned wrong name")
            self.assertEqual(project.path, projectFilePath, "Project returned wrong path")
            #Target a
            self.assertEqual(project.targets[0].name, "a", "Project returned wrong target 'a' name")
            self.assertEqual(project.targets[0].path, "a-1.11.tar.gz", "Project returned wrong target 'a' path")
            self.assertEqual(project.targets[0].dependsOn, ['b', 'c'], "Project returned wrong target 'a' dependsOn")
            self.assertEqual(project.targets[0].commands["preconfig"], "autoreconf -i", "Project returned wrong target 'a' preconfig command")
            self.assertEqual(project.targets[0].commands["config"], "./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'a' config command")
            self.assertEqual(project.targets[0].commands["build"], "make", "Project returned wrong target build 'a' command")
            self.assertEqual(project.targets[0].commands["install"], "make install", "Project returned wrong target install 'a' command")
            #Target b
            self.assertEqual(project.targets[1].name, "b", "Project returned wrong target 'b' name")
            self.assertEqual(project.targets[1].path, "b-2.22.tar.gz", "Project returned wrong target 'b' path")
            self.assertEqual(project.targets[1].dependsOn, ['c'], "Project returned wrong target 'b' dependsOn")
            self.assertEqual(project.targets[1].commands["preconfig"], "bautoreconf -i", "Project returned wrong target 'b' preconfig command")
            self.assertEqual(project.targets[1].commands["config"], "./configure --prefix=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'b' config command")
            self.assertEqual(project.targets[1].commands["build"], "bmake", "Project returned wrong target 'b' build command")
            self.assertEqual(project.targets[1].commands["install"], "bmake install", "Project returned wrong target 'b' install command")
            #Target c
            self.assertEqual(project.targets[2].name, "c", "Project returned wrong target 'c' name")
            self.assertEqual(project.targets[2].path, "c-3.33.tar.gz", "Project returned wrong target 'c' path")
            self.assertEqual(project.targets[2].commands["preconfig"], "cautoreconf -i", "Project returned wrong target 'c' preconfig command")
            self.assertEqual(project.targets[2].commands["config"], "./configure --prefix=$(_prefix)", "Project returned wrong target 'c' config command")
            self.assertEqual(project.targets[2].commands["build"], "cmake", "Project returned wrong target 'c' build command")
            self.assertEqual(project.targets[2].commands["install"], "cmake install", "Project returned wrong target 'c' install command")
        finally:
            os.remove(projectFilePath)

    def test_readWriteMultiTargetProject(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b, c
                                            PreConfig: autoreconf -i
                                            Config: ./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)
                                            Build: make
                                            Install: make install

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c
                                            PreConfig: bautoreconf -i
                                            Config: ./configure --prefix=$(_prefix) --with-c=$(_prefix)
                                            Build: bmake
                                            Install: bmake install

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            PreConfig: cautoreconf -i
                                            Config: ./configure --prefix=$(_prefix)
                                            Build: cmake
                                            Install: cmake install
                                            """)
        try:
            #Read initial values
            projectOrigFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            projectOrig = mdProject.Project(projectOrigFilePath)
            self.assertTrue(projectOrig.read(), "Initial project file could not be read")

            #Write values to new file
            projectFilePath = mdTestUtilities.makeTempFile(suffix=".md")
            projectOrig.write(projectFilePath)

            #Read values from written file and test to make sure they are correct
            project = mdProject.Project(projectFilePath)
            self.assertTrue(project.read(), "Project file could not be read")
            #Project
            self.assertEqual(project.name, os.path.split(projectFilePath)[1][:-3], "Project returned wrong name")
            self.assertEqual(project.path, projectFilePath, "Project returned wrong path")
            #Target a
            self.assertEqual(project.targets[0].name, "a", "Project returned wrong target 'a' name")
            self.assertEqual(project.targets[0].path, "a-1.11.tar.gz", "Project returned wrong target 'a' path")
            self.assertEqual(project.targets[0].dependsOn, ['b', 'c'], "Project returned wrong target 'a' dependsOn")
            self.assertEqual(project.targets[0].commands["preconfig"], "autoreconf -i", "Project returned wrong target 'a' preconfig command")
            self.assertEqual(project.targets[0].commands["config"], "./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'a' config command")
            self.assertEqual(project.targets[0].commands["build"], "make", "Project returned wrong target build 'a' command")
            self.assertEqual(project.targets[0].commands["install"], "make install", "Project returned wrong target install 'a' command")
            #Target b
            self.assertEqual(project.targets[1].name, "b", "Project returned wrong target 'b' name")
            self.assertEqual(project.targets[1].path, "b-2.22.tar.gz", "Project returned wrong target 'b' path")
            self.assertEqual(project.targets[1].dependsOn, ['c'], "Project returned wrong target 'b' dependsOn")
            self.assertEqual(project.targets[1].commands["preconfig"], "bautoreconf -i", "Project returned wrong target 'b' preconfig command")
            self.assertEqual(project.targets[1].commands["config"], "./configure --prefix=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'b' config command")
            self.assertEqual(project.targets[1].commands["build"], "bmake", "Project returned wrong target 'b' build command")
            self.assertEqual(project.targets[1].commands["install"], "bmake install", "Project returned wrong target 'b' install command")
            #Target c
            self.assertEqual(project.targets[2].name, "c", "Project returned wrong target 'c' name")
            self.assertEqual(project.targets[2].path, "c-3.33.tar.gz", "Project returned wrong target 'c' path")
            self.assertEqual(project.targets[2].commands["preconfig"], "cautoreconf -i", "Project returned wrong target 'c' preconfig command")
            self.assertEqual(project.targets[2].commands["config"], "./configure --prefix=$(_prefix)", "Project returned wrong target 'c' config command")
            self.assertEqual(project.targets[2].commands["build"], "cmake", "Project returned wrong target 'c' build command")
            self.assertEqual(project.targets[2].commands["install"], "cmake install", "Project returned wrong target 'c' install command")
        finally:
            os.remove(projectFilePath)
            os.remove(projectOrigFilePath)

    def test_validateSingleTargetProjectWithSteps(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            PreConfig: autoreconf -i
                                            Config: ./configure --prefix=$(_prefix)
                                            Build: make
                                            Install: make install
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateMultiTargetProjectWithStepsAndDependancies(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b
                                            PreConfig: autoreconf -i
                                            Config: ./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)
                                            Build: make
                                            Install: make install

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c
                                            PreConfig: bautoreconf -i
                                            Config: ./configure --prefix=$(_prefix) --with-c=$(_prefix)
                                            Build: bmake
                                            Install: bmake install

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            PreConfig: cautoreconf -i
                                            Config: ./configure --prefix=$(_prefix)
                                            Build: cmake
                                            Install: cmake install
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateSingleTargetProjectWithoutSteps(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateMultiTargetProjectWithoutStepsOrDependancies(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: b
                                            Path: b-2.22.tar.gz

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateNonCyclicalProjectCase1(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateNonCyclicalProjectCase2(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b, c

                                            Name: b
                                            Path: b-2.22.tar.gz

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateNonCyclicalProjectCase3(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: b
                                            Path: b-2.22.tar.gz

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateNonCyclicalProjectCase4(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: c, b

                                            Name: b
                                            Path: b-2.22.tar.gz

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateNonCyclicalProjectCase5(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: a

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            DependsOn: b
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_validateNonCyclicalProjectCase6(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b, c

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.validate(options), "Project could not validate")
        finally:
            os.remove(projectFilePath)

    def test_detectCyclicalProjectCase1(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            DependsOn: a
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertFalse(project.validate(options), "Project validated when it should not have due to cyclical dependancy graph")
        finally:
            os.remove(projectFilePath)

    def test_detectCyclicalProjectCase2(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            DependsOn: b
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertFalse(project.validate(options), "Project validated when it should not have due to cyclical dependancy graph")
        finally:
            os.remove(projectFilePath)

    def test_detectCyclicalProjectCase3(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: a
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            self.assertFalse(project.read(), "Reading project file should have failed")
        finally:
            os.remove(projectFilePath)

    def test_detectCyclicalProjectCase4(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b

                                            Name: b
                                            Path: b-2.22.tar.gz
                                            DependsOn: c

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            DependsOn: c
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            self.assertFalse(project.read(), "Reading project file should have failed")
        finally:
            os.remove(projectFilePath)

    def test_detectProjectWithNonExistantDependancy(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertFalse(project.validate(options), "Project validated when it should not have due to non-existant dependancy")
        finally:
            os.remove(projectFilePath)

    def test_getTarget(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: b
                                            Path: b-2.22.tar.gz

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            self.assertTrue(project.read(), "Project file could not be read")
            #Targets that exist in project
            self.assertIsNotNone(project.getTarget("a"), "Target 'a' could not be found in project")
            self.assertIsNotNone(project.getTarget("b"), "Target 'b' could not be found in project")
            self.assertIsNotNone(project.getTarget("c"), "Target 'c' could not be found in project")
            self.assertIsNotNone(project.getTarget("A"), "Target 'a' could not be found in project")
            self.assertIsNotNone(project.getTarget("B "), "Target 'b' could not be found in project")
            self.assertIsNotNone(project.getTarget(" C"), "Target 'c' could not be found in project")
            #Targets that do NOT exist in project
            self.assertIsNone(project.getTarget("d"), "Target 'd' should not have been found in project")
            self.assertIsNone(project.getTarget(""), "Target '' should not have been found in project")
        finally:
            os.remove(projectFilePath)

    def test_examineSingleTarget(self):
        projectFileContents = textwrap.dedent("""
                                            Name: TestCaseA
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.examine(options), "Project failed to examine")
            self.assertEquals(project.getTarget("TestCaseA").dependancyDepth, 0, "TestCaseA had wrong dependancy depth")
            self.assertEquals(len(project.targets), 1, "Number of Targets in project is wrong")
            self.assertEquals(project.targets[0].name, "TestCaseA", "Sorting failed. TestCaseA should have been the first target.")
        finally:
            os.remove(projectFilePath)

    def test_examineMultiTargetCase1(self):
        projectFileContents = textwrap.dedent("""
                                            Name: TestCaseA
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: TestCaseB

                                            Name: TestCaseB
                                            Path: cases/simpleGraphAutoTools/TestCaseB
                                            DependsOn: TestCaseC

                                            Name: TestCaseC
                                            Path: cases/simpleGraphAutoTools/TestCaseC
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.examine(options), "Project failed to examine")
            self.assertEquals(project.getTarget("TestCaseA").dependancyDepth, 0, "TestCaseA had wrong dependancy depth")
            self.assertEquals(project.getTarget("TestCaseB").dependancyDepth, 1, "TestCaseB had wrong dependancy depth")
            self.assertEquals(project.getTarget("TestCaseC").dependancyDepth, 2, "TestCaseC had wrong dependancy depth")
            self.assertEquals(len(project.targets), 3, "Number of Targets in project is wrong")
            self.assertEquals(project.targets[0].name, "TestCaseC", "Sorting failed. TestCaseC should have been the first target.")
            self.assertEquals(project.targets[1].name, "TestCaseB", "Sorting failed. TestCaseB should have been the first target.")
            self.assertEquals(project.targets[2].name, "TestCaseA", "Sorting failed. TestCaseA should have been the first target.")
        finally:
            os.remove(projectFilePath)

    def test_examineMultiTargetCase2(self):
        projectFileContents = textwrap.dedent("""
                                            Name: TestCaseA
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: TestCaseB, TestCaseC

                                            Name: TestCaseB
                                            Path: cases/simpleGraphAutoTools/TestCaseB
                                            DependsOn: TestCaseC

                                            Name: TestCaseC
                                            Path: cases/simpleGraphAutoTools/TestCaseC
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.examine(options), "Project failed to examine")
            self.assertEquals(project.getTarget("TestCaseA").dependancyDepth, 0, "TestCaseA had wrong dependancy depth")
            self.assertEquals(project.getTarget("TestCaseB").dependancyDepth, 1, "TestCaseB had wrong dependancy depth")
            self.assertEquals(project.getTarget("TestCaseC").dependancyDepth, 2, "TestCaseC had wrong dependancy depth")
            self.assertEquals(len(project.targets), 3, "Number of Targets in project is wrong")
            self.assertEquals(project.targets[0].name, "TestCaseC", "Sorting failed. TestCaseC should have been the first target.")
            self.assertEquals(project.targets[1].name, "TestCaseB", "Sorting failed. TestCaseB should have been the first target.")
            self.assertEquals(project.targets[2].name, "TestCaseA", "Sorting failed. TestCaseA should have been the first target.")
        finally:
            os.remove(projectFilePath)

    def test_examineMultiTargetCase3(self):
        projectFileContents = textwrap.dedent("""
                                            Name: A
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: B, C

                                            Name: B
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: C

                                            Name: C
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: D

                                            Name: D
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.examine(options), "Project failed to examine")
            self.assertEquals(project.getTarget("A").dependancyDepth, 0, "A had wrong dependancy depth")
            self.assertEquals(project.getTarget("B").dependancyDepth, 1, "B had wrong dependancy depth")
            self.assertEquals(project.getTarget("C").dependancyDepth, 2, "C had wrong dependancy depth")
            self.assertEquals(project.getTarget("D").dependancyDepth, 3, "D had wrong dependancy depth")
            self.assertEquals(len(project.targets), 4, "Number of Targets in project is wrong")
            self.assertEquals(project.targets[0].name, "D", "Sorting failed. D should have been the first target.")
            self.assertEquals(project.targets[1].name, "C", "Sorting failed. C should have been the first target.")
            self.assertEquals(project.targets[2].name, "B", "Sorting failed. B should have been the first target.")
            self.assertEquals(project.targets[3].name, "A", "Sorting failed. A should have been the first target.")
        finally:
            os.remove(projectFilePath)

    def test_examineMultiTargetCase4(self):
        projectFileContents = textwrap.dedent("""
                                            Name: A
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: B, C

                                            Name: B
                                            Path: cases/simpleGraphAutoTools/TestCaseA

                                            Name: C
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.examine(options), "Project failed to examine")
            self.assertEquals(project.getTarget("A").dependancyDepth, 0, "A had wrong dependancy depth")
            self.assertEquals(project.getTarget("B").dependancyDepth, 1, "B had wrong dependancy depth")
            self.assertEquals(project.getTarget("C").dependancyDepth, 1, "C had wrong dependancy depth")
            self.assertEquals(len(project.targets), 3, "Number of Targets in project is wrong")
            self.assertEquals(project.targets[0].name, "C", "Sorting failed. C should have been the first target.")
            self.assertEquals(project.targets[1].name, "B", "Sorting failed. B should have been the first target.")
            self.assertEquals(project.targets[2].name, "A", "Sorting failed. A should have been the first target.")
        finally:
            os.remove(projectFilePath)

    def test_examineMultiTargetCase5(self):
        projectFileContents = textwrap.dedent("""
                                            Name: A
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: B, C, D

                                            Name: B
                                            Path: cases/simpleGraphAutoTools/TestCaseA

                                            Name: C
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            DependsOn: D

                                            Name: D
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            """)
        try:
            projectFilePath = mdTestUtilities.makeTempFile(projectFileContents, ".md")
            project = mdProject.Project(projectFilePath)
            options = mdOptions.Options()
            self.assertTrue(project.read(), "Project file could not be read")
            self.assertTrue(project.examine(options), "Project failed to examine")
            self.assertEquals(project.getTarget("A").dependancyDepth, 0, "A had wrong dependancy depth")
            self.assertEquals(project.getTarget("B").dependancyDepth, 1, "B had wrong dependancy depth")
            self.assertEquals(project.getTarget("C").dependancyDepth, 1, "C had wrong dependancy depth")
            self.assertEquals(project.getTarget("D").dependancyDepth, 2, "D had wrong dependancy depth")
            self.assertEquals(len(project.targets), 4, "Number of Targets in project is wrong")
            self.assertEquals(project.targets[0].name, "D", "Sorting failed. D should have been the first target.")
            self.assertEquals(project.targets[1].name, "C", "Sorting failed. C should have been the first target.")
            self.assertEquals(project.targets[2].name, "B", "Sorting failed. B should have been the first target.")
            self.assertEquals(project.targets[3].name, "A", "Sorting failed. A should have been the first target.")
        finally:
            os.remove(projectFilePath)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdProject))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()