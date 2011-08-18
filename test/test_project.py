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

import os, sys, textwrap, unittest, mdTestUtilities

if not ".." in sys.path:
    sys.path.append("..")

from md import logger, options, project, utilityFunctions

class Test_project(unittest.TestCase):
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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            self.assertTrue(projects.read(), "Project file could not be read")
            #Project
            self.assertEqual(projects.name, os.path.split(projectFilePath)[1][:-3], "Project returned wrong name")
            self.assertEqual(projects.path, projectFilePath, "Project returned wrong path")
            #Target a
            self.assertEqual(projects.targets[0].name, "a", "Project returned wrong target 'a' name")
            self.assertEqual(projects.targets[0].path, "a-1.11.tar.gz", "Project returned wrong target 'a' path")
            self.assertEqual(projects.targets[0].findBuildStep("preconfig").command, "autoreconf -i", "Project returned wrong target 'a' preconfig command")
            self.assertEqual(projects.targets[0].findBuildStep("config").command, "./configure --prefix=$(_prefix)", "Project returned wrong target 'a' config command")
            self.assertEqual(projects.targets[0].findBuildStep("build").command, "make", "Project returned wrong target 'a' build command")
            self.assertEqual(projects.targets[0].findBuildStep("install").command, "make install", "Project returned wrong target 'a' install command")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_readDetectDuplicateTarget(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: a
                                            Path: a-1.11.tar.gz
                                            """)
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            self.assertFalse(projects.read(), "Project read should have detected duplicate target")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            self.assertTrue(projects.read(), "Project file could not be read")
            #Project
            self.assertEqual(projects.name, os.path.split(projectFilePath)[1][:-3], "Project returned wrong name")
            self.assertEqual(projects.path, projectFilePath, "Project returned wrong path")
            #Target a
            self.assertEqual(projects.targets[0].name, "a", "Project returned wrong target 'a' name")
            self.assertEqual(projects.targets[0].path, "a-1.11.tar.gz", "Project returned wrong target 'a' path")
            self.assertEqual(projects.targets[0].dependsOn, ['b', 'c'], "Project returned wrong target 'a' dependsOn")
            self.assertEqual(projects.targets[0].findBuildStep("preconfig").command, "autoreconf -i", "Project returned wrong target 'a' preconfig command")
            self.assertEqual(projects.targets[0].findBuildStep("config").command, "./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'a' config command")
            self.assertEqual(projects.targets[0].findBuildStep("build").command, "make", "Project returned wrong target build 'a' command")
            self.assertEqual(projects.targets[0].findBuildStep("install").command, "make install", "Project returned wrong target install 'a' command")
            #Target b
            self.assertEqual(projects.targets[1].name, "b", "Project returned wrong target 'b' name")
            self.assertEqual(projects.targets[1].path, "b-2.22.tar.gz", "Project returned wrong target 'b' path")
            self.assertEqual(projects.targets[1].dependsOn, ['c'], "Project returned wrong target 'b' dependsOn")
            self.assertEqual(projects.targets[1].findBuildStep("preconfig").command, "bautoreconf -i", "Project returned wrong target 'b' preconfig command")
            self.assertEqual(projects.targets[1].findBuildStep("config").command, "./configure --prefix=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'b' config command")
            self.assertEqual(projects.targets[1].findBuildStep("build").command, "bmake", "Project returned wrong target 'b' build command")
            self.assertEqual(projects.targets[1].findBuildStep("install").command, "bmake install", "Project returned wrong target 'b' install command")
            #Target c
            self.assertEqual(projects.targets[2].name, "c", "Project returned wrong target 'c' name")
            self.assertEqual(projects.targets[2].path, "c-3.33.tar.gz", "Project returned wrong target 'c' path")
            self.assertEqual(projects.targets[2].findBuildStep("preconfig").command, "cautoreconf -i", "Project returned wrong target 'c' preconfig command")
            self.assertEqual(projects.targets[2].findBuildStep("config").command, "./configure --prefix=$(_prefix)", "Project returned wrong target 'c' config command")
            self.assertEqual(projects.targets[2].findBuildStep("build").command, "cmake", "Project returned wrong target 'c' build command")
            self.assertEqual(projects.targets[2].findBuildStep("install").command, "cmake install", "Project returned wrong target 'c' install command")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectOrigFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projectOrig = project.Project(projectOrigFilePath)
            self.assertTrue(projectOrig.read(), "Initial project file could not be read")

            #Write values to new file
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, suffix=".md")
            projectOrig.write(projectFilePath)

            #Read values from written file and test to make sure they are correct
            projects = project.Project(projectFilePath)
            self.assertTrue(projects.read(), "Project file could not be read")
            #Project
            self.assertEqual(projects.name, os.path.split(projectFilePath)[1][:-3], "Project returned wrong name")
            self.assertEqual(projects.path, projectFilePath, "Project returned wrong path")
            #Target a
            self.assertEqual(projects.targets[0].name, "a", "Project returned wrong target 'a' name")
            self.assertEqual(projects.targets[0].path, "a-1.11.tar.gz", "Project returned wrong target 'a' path")
            self.assertEqual(projects.targets[0].dependsOn, ['b', 'c'], "Project returned wrong target 'a' dependsOn")
            self.assertEqual(projects.targets[0].findBuildStep("preconfig").command, "autoreconf -i", "Project returned wrong target 'a' preconfig command")
            self.assertEqual(projects.targets[0].findBuildStep("config").command, "./configure --prefix=$(_prefix) --with-b=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'a' config command")
            self.assertEqual(projects.targets[0].findBuildStep("build").command, "make", "Project returned wrong target build 'a' command")
            self.assertEqual(projects.targets[0].findBuildStep("install").command, "make install", "Project returned wrong target install 'a' command")
            #Target b
            self.assertEqual(projects.targets[1].name, "b", "Project returned wrong target 'b' name")
            self.assertEqual(projects.targets[1].path, "b-2.22.tar.gz", "Project returned wrong target 'b' path")
            self.assertEqual(projects.targets[1].dependsOn, ['c'], "Project returned wrong target 'b' dependsOn")
            self.assertEqual(projects.targets[1].findBuildStep("preconfig").command, "bautoreconf -i", "Project returned wrong target 'b' preconfig command")
            self.assertEqual(projects.targets[1].findBuildStep("config").command, "./configure --prefix=$(_prefix) --with-c=$(_prefix)", "Project returned wrong target 'b' config command")
            self.assertEqual(projects.targets[1].findBuildStep("build").command, "bmake", "Project returned wrong target 'b' build command")
            self.assertEqual(projects.targets[1].findBuildStep("install").command, "bmake install", "Project returned wrong target 'b' install command")
            #Target c
            self.assertEqual(projects.targets[2].name, "c", "Project returned wrong target 'c' name")
            self.assertEqual(projects.targets[2].path, "c-3.33.tar.gz", "Project returned wrong target 'c' path")
            self.assertEqual(projects.targets[2].findBuildStep("preconfig").command, "cautoreconf -i", "Project returned wrong target 'c' preconfig command")
            self.assertEqual(projects.targets[2].findBuildStep("config").command, "./configure --prefix=$(_prefix)", "Project returned wrong target 'c' config command")
            self.assertEqual(projects.targets[2].findBuildStep("build").command, "cmake", "Project returned wrong target 'c' build command")
            self.assertEqual(projects.targets[2].findBuildStep("install").command, "cmake install", "Project returned wrong target 'c' install command")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validateMultiTargetProjectWithStepsAndDependencies(self):
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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()


            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validateSingleTargetProjectWithoutSteps(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            """)
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_validateMultiTargetProjectWithoutStepsOrDependencies(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz

                                            Name: b
                                            Path: b-2.22.tar.gz

                                            Name: c
                                            Path: c-3.33.tar.gz
                                            """)
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.validate(option), "Project could not validate")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertFalse(projects.validate(option), "Project validated when it should not have due to cyclical dependency graph")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertFalse(projects.validate(option), "Project validated when it should not have due to cyclical dependency graph")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_detectCyclicalProjectCase3(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: a
                                            """)
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            self.assertFalse(projects.read(), "Reading project file should have failed")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            self.assertFalse(projects.read(), "Reading project file should have failed")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_detectProjectWithNonExistantDependency(self):
        projectFileContents = textwrap.dedent("""
                                            Name: a
                                            Path: a-1.11.tar.gz
                                            DependsOn: b
                                            """)
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertFalse(projects.validate(option), "Project validated when it should not have due to non-existant dependency")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            self.assertTrue(projects.read(), "Project file could not be read")
            #Targets that exist in project
            self.assertNotEquals(projects.getTarget("a"), None, "Target 'a' could not be found in project")
            self.assertNotEquals(projects.getTarget("b"), None, "Target 'b' could not be found in project")
            self.assertNotEquals(projects.getTarget("c"), None, "Target 'c' could not be found in project")
            self.assertNotEquals(projects.getTarget("A"), None, "Target 'a' could not be found in project")
            self.assertNotEquals(projects.getTarget("B "), None, "Target 'b' could not be found in project")
            self.assertNotEquals(projects.getTarget(" C"), None, "Target 'c' could not be found in project")
            #Targets that do NOT exist in project
            self.assertEquals(projects.getTarget("d"), None, "Target 'd' should not have been found in project")
            self.assertEquals(projects.getTarget(""), None, "Target '' should not have been found in project")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_examineSingleTarget(self):
        projectFileContents = textwrap.dedent("""
                                            Name: TestCaseA
                                            Path: cases/simpleGraphAutoTools/TestCaseA
                                            """)
        try:
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.examine(option), "Project failed to examine")
            self.assertEquals(projects.getTarget("TestCaseA").dependencyDepth, 0, "TestCaseA had wrong dependency depth")
            self.assertEquals(len(projects.targets), 1, "Number of Targets in project is wrong")
            self.assertEquals(projects.targets[0].name, "TestCaseA", "Sorting failed. TestCaseA should have been the first target.")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.examine(option), "Project failed to examine")
            self.assertEquals(projects.getTarget("TestCaseA").dependencyDepth, 0, "TestCaseA had wrong dependency depth")
            self.assertEquals(projects.getTarget("TestCaseB").dependencyDepth, 1, "TestCaseB had wrong dependency depth")
            self.assertEquals(projects.getTarget("TestCaseC").dependencyDepth, 2, "TestCaseC had wrong dependency depth")
            self.assertEquals(len(projects.targets), 3, "Number of Targets in project is wrong")
            self.assertEquals(projects.targets[0].name, "TestCaseA", "Sorting failed. TestCaseA should have been the first target.")
            self.assertEquals(projects.targets[1].name, "TestCaseB", "Sorting failed. TestCaseB should have been the first target.")
            self.assertEquals(projects.targets[2].name, "TestCaseC", "Sorting failed. TestCaseC should have been the first target.")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.examine(option), "Project failed to examine")
            self.assertEquals(projects.getTarget("TestCaseA").dependencyDepth, 0, "TestCaseA had wrong dependency depth")
            self.assertEquals(projects.getTarget("TestCaseB").dependencyDepth, 1, "TestCaseB had wrong dependency depth")
            self.assertEquals(projects.getTarget("TestCaseC").dependencyDepth, 2, "TestCaseC had wrong dependency depth")
            self.assertEquals(len(projects.targets), 3, "Number of Targets in project is wrong")
            self.assertEquals(projects.targets[0].name, "TestCaseA", "Sorting failed. TestCaseA should have been the first target.")
            self.assertEquals(projects.targets[1].name, "TestCaseB", "Sorting failed. TestCaseB should have been the first target.")
            self.assertEquals(projects.targets[2].name, "TestCaseC", "Sorting failed. TestCaseC should have been the first target.")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.examine(option), "Project failed to examine")
            self.assertEquals(projects.getTarget("A").dependencyDepth, 0, "A had wrong dependency depth")
            self.assertEquals(projects.getTarget("B").dependencyDepth, 1, "B had wrong dependency depth")
            self.assertEquals(projects.getTarget("C").dependencyDepth, 2, "C had wrong dependency depth")
            self.assertEquals(projects.getTarget("D").dependencyDepth, 3, "D had wrong dependency depth")
            self.assertEquals(len(projects.targets), 4, "Number of Targets in project is wrong")
            self.assertEquals(projects.targets[0].name, "A", "Sorting failed. A should have been the first target.")
            self.assertEquals(projects.targets[1].name, "B", "Sorting failed. B should have been the first target.")
            self.assertEquals(projects.targets[2].name, "C", "Sorting failed. C should have been the first target.")
            self.assertEquals(projects.targets[3].name, "D", "Sorting failed. D should have been the first target.")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.examine(option), "Project failed to examine")
            self.assertEquals(projects.getTarget("A").dependencyDepth, 0, "A had wrong dependency depth")
            self.assertEquals(projects.getTarget("B").dependencyDepth, 1, "B had wrong dependency depth")
            self.assertEquals(projects.getTarget("C").dependencyDepth, 1, "C had wrong dependency depth")
            self.assertEquals(len(projects.targets), 3, "Number of Targets in project is wrong")
            self.assertEquals(projects.targets[0].name, "A", "Sorting failed. A should have been the first target.")
            self.assertEquals(projects.targets[1].name, "B", "Sorting failed. B should have been the first target.")
            self.assertEquals(projects.targets[2].name, "C", "Sorting failed. C should have been the first target.")
        finally:
            utilityFunctions.removeDir(tempDir)

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
            tempDir = mdTestUtilities.makeTempDir()
            projectFilePath = mdTestUtilities.makeTempFile(tempDir, projectFileContents, ".md")
            projects = project.Project(projectFilePath)
            option = options.Options()
            option.buildDir = os.path.join(tempDir, option.buildDir)
            self.assertTrue(projects.read(), "Project file could not be read")
            self.assertTrue(projects.examine(option), "Project failed to examine")
            self.assertEquals(projects.getTarget("A").dependencyDepth, 0, "A had wrong dependency depth")
            self.assertEquals(projects.getTarget("B").dependencyDepth, 1, "B had wrong dependency depth")
            self.assertEquals(projects.getTarget("C").dependencyDepth, 1, "C had wrong dependency depth")
            self.assertEquals(projects.getTarget("D").dependencyDepth, 2, "D had wrong dependency depth")
            self.assertEquals(len(projects.targets), 4, "Number of Targets in project is wrong")
            self.assertEquals(projects.targets[0].name, "A", "Sorting failed. A should have been the first target.")
            self.assertEquals(projects.targets[1].name, "B", "Sorting failed. B should have been the first target.")
            self.assertEquals(projects.targets[2].name, "C", "Sorting failed. C should have been the first target.")
            self.assertEquals(projects.targets[3].name, "D", "Sorting failed. D should have been the first target.")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_project))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
