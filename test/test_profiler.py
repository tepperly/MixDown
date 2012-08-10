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

from md import logger, options, overrides, profiler, utilityFunctions

class Test_profiler(unittest.TestCase):
    def test_findExecutables01(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            exes = profiler.findExecutables([(tempDir, False)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables02(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            exes = profiler.findExecutables([(tempDir, True)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables03(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, False)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables04(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.makeFileExecutable(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, True)], ["gcc"])
            self.assertEquals(len(exes), 1, "profiler.findExecutables did not find the right amount of executables")
            self.assertEquals(exes[0], testExe, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables05(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, False)], ["gcc"])
            self.assertEquals(len(exes), 0, "profiler.findExecutables did not find the right amount of executables")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables06(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            testExe = os.path.join(tempDir, "gcc")
            mdTestUtilities.createBlankFile(testExe)
            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            exes = profiler.findExecutables([(tempDir, True)], ["gcc"])
            self.assertEquals(len(exes), 0, "profiler.findExecutables did not find the right amount of executables")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_findExecutables07(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()

            mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))

            aDir = os.path.join(tempDir, 'a')
            aGccExe = os.path.join(aDir, "gcc")
            mdTestUtilities.createBlankFile(aGccExe)
            mdTestUtilities.makeFileExecutable(aGccExe)

            bDir = os.path.join(tempDir, 'b')
            bIccExe = os.path.join(bDir, "icc")
            mdTestUtilities.createBlankFile(bIccExe)
            mdTestUtilities.makeFileExecutable(bIccExe)

            acDir = os.path.join(os.path.join(tempDir, 'a'), 'c')
            acIccExe = os.path.join(acDir, "icc")
            mdTestUtilities.createBlankFile(acIccExe)
            mdTestUtilities.makeFileExecutable(acIccExe)

            exes = profiler.findExecutables([(tempDir, True)], ["icc", "gcc"])
            self.assertEquals(len(exes), 3, "profiler.findExecutables did not find the right amount of executables")
            self.assertTrue(aGccExe in exes, "profiler.findExecutables did not find the right executable")
            self.assertTrue(bIccExe in exes, "profiler.findExecutables did not find the right executable")
            self.assertTrue(acIccExe in exes, "profiler.findExecutables did not find the right executable")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_addGnuOptimizationGroup01(self):
        compilerGroup = overrides.OverrideGroup()

        groups = []
        groups.append(compilerGroup)

        profiler.addGnuOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 1, "profiler.addGnuOptimazationGroup should not have added any more groups")

    def test_addGnuOptimizationGroup02(self):
        compilerGroup = overrides.OverrideGroup()
        compilerGroup.compiler = "GNU"
        compilerGroup.optimization = "*"
        compilerGroup.parallel = "*"
        compilerGroup["ccompiler"] = "gcc"
        compilerGroup["cxxcompiler"] = "g++"
        compilerGroup["objccompiler"] = "gobjc"
        compilerGroup["objcxxcompiler"] = "gobjc"
        compilerGroup["cpreprocessor"] = "cpp"
        compilerGroup["objccpreprocessor"] = "cpp"
        compilerGroup["objcxxpreprocessor"] = "cpp"
        compilerGroup["fcompiler"] = "gfortran"
        compilerGroup["f77compiler"] = "g77"

        groups = []
        groups.append(compilerGroup)

        profiler.addGnuOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 3, "profiler.addGnuOptimazationGroup should have added 2 more groups")
        self.assertEquals(groups[0].compiler, "GNU", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0].optimization, "*", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0].parallel, "*", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["ccompiler"], "gcc", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["cxxcompiler"], "g++", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["objccompiler"], "gobjc", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["objcxxcompiler"], "gobjc", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["cpreprocessor"], "cpp", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["objccpreprocessor"], "cpp", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["objcxxpreprocessor"], "cpp", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["fcompiler"], "gfortran", "profiler.addGnuOptimazationGroup should not have altered this value")
        self.assertEquals(groups[0]["f77compiler"], "g77", "profiler.addGnuOptimazationGroup should not have altered this value")

        gccDebugFlags = "-g -O0 -Wall"
        self.assertEquals(groups[1].compiler, "GNU", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1].optimization, "debug", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1].parallel, "*", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["cflags"], gccDebugFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["cxxflags"], gccDebugFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["objcflags"], gccDebugFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["objcxxflags"], gccDebugFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["cppflags"], "-Wall", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["fflags"], "-Wall", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[1]["f77flags"], "-Wall", "profiler.addGnuOptimazationGroup returned wrong value")

        gccReleaseFlags = "-O2 -Wall"
        self.assertEquals(groups[2].compiler, "GNU", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2].optimization, "release", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2].parallel, "*", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["cflags"], gccReleaseFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["cxxflags"], gccReleaseFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["objcflags"], gccReleaseFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["objcxxflags"], gccReleaseFlags, "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["cppflags"], "-Wall", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["fflags"], "-Wall", "profiler.addGnuOptimazationGroup returned wrong value")
        self.assertEquals(groups[2]["f77flags"], "-Wall", "profiler.addGnuOptimazationGroup returned wrong value")

    def test_addIntelOptimizationGroup01(self):
        compilerGroup = overrides.OverrideGroup()

        groups = []
        groups.append(compilerGroup)

        profiler.addIntelOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 1, "profiler.addIntelOptimizationGroup should not have added any more groups")

    def test_addIntelOptimizationGroup02(self):
        compilerGroup = overrides.OverrideGroup()
        compilerGroup.compiler = "INTEL"
        compilerGroup.optimization = "*"
        compilerGroup.parallel = "*"
        compilerGroup["ccompiler"] = "icc"
        compilerGroup["cxxcompiler"] = "icc"
        compilerGroup["cpreprocessor"] = "cpp"
        compilerGroup["fcompiler"] = "ifort"
        compilerGroup["f77compiler"] = "ifc"

        groups = []
        groups.append(compilerGroup)

        profiler.addIntelOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 3, "profiler.addIntelOptimizationGroup should have added 2 more groups")
        self.assertEquals(groups[0].compiler, "INTEL", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0].optimization, "*", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0].parallel, "*", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["ccompiler"], "icc", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["cxxcompiler"], "icc", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["cpreprocessor"], "cpp", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["fcompiler"], "ifort", "profiler.addIntelOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["f77compiler"], "ifc", "profiler.addIntelOptimizationGroup should not have altered this value")

        iccDebugFlags = "-debug full -O0 -Wall"
        self.assertEquals(groups[1].compiler, "INTEL", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1].optimization, "debug", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1].parallel, "*", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cflags"], iccDebugFlags, "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cxxflags"], iccDebugFlags, "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cppflags"], "-Wall", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["fflags"], "-O0 -warn all", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["f77flags"], "-O0 -warn all", "profiler.addIntelOptimizationGroup returned wrong value")

        iccReleaseFlags = "-debug none -O2 -Wall"
        self.assertEquals(groups[2].compiler, "INTEL", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2].optimization, "release", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2].parallel, "*", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cflags"], iccReleaseFlags, "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cxxflags"], iccReleaseFlags, "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cppflags"], "-Wall", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["fflags"], "-O2 -warn all", "profiler.addIntelOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["f77flags"], "-O2 -warn all", "profiler.addIntelOptimizationGroup returned wrong value")

    def test_addPathscaleOptimizationGroup01(self):
        compilerGroup = overrides.OverrideGroup()

        groups = []
        groups.append(compilerGroup)

        profiler.addPathscaleOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 1, "profiler.addPathscaleOptimizationGroup should not have added any more groups")

    def test_addPathscaleOptimizationGroup02(self):
        compilerGroup = overrides.OverrideGroup()
        compilerGroup.compiler = "PATHSCALE"
        compilerGroup.optimization = "*"
        compilerGroup.parallel = "*"
        compilerGroup["ccompiler"] = "pathcc"
        compilerGroup["cxxcompiler"] = "pathCC"
        compilerGroup["cpreprocessor"] = "cpp"
        compilerGroup["fcompiler"] = "pathf95"
        compilerGroup["f77compiler"] = "pathf95"

        groups = []
        groups.append(compilerGroup)

        profiler.addPathscaleOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 3, "profiler.addPathscaleOptimizationGroup should have added 2 more groups")
        self.assertEquals(groups[0].compiler, "PATHSCALE", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0].optimization, "*", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0].parallel, "*", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["ccompiler"], "pathcc", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["cxxcompiler"], "pathCC", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["cpreprocessor"], "cpp", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["fcompiler"], "pathf95", "profiler.addPathscaleOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["f77compiler"], "pathf95", "profiler.addPathscaleOptimizationGroup should not have altered this value")

        pathDebugFlags = "-g -O0 -Wall"
        self.assertEquals(groups[1].compiler, "PATHSCALE", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1].optimization, "debug", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1].parallel, "*", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cflags"], pathDebugFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cxxflags"], pathDebugFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cppflags"], "-Wall", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["fflags"], pathDebugFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["f77flags"], pathDebugFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")

        pathReleaseFlags = "-O2 -Wall"
        self.assertEquals(groups[2].compiler, "PATHSCALE", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2].optimization, "release", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2].parallel, "*", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cflags"], pathReleaseFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cxxflags"], pathReleaseFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cppflags"], "-Wall", "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["fflags"], pathReleaseFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["f77flags"], pathReleaseFlags, "profiler.addPathscaleOptimizationGroup returned wrong value")

    def test_addPortlandGroupOptimizationGroup01(self):
        compilerGroup = overrides.OverrideGroup()

        groups = []
        groups.append(compilerGroup)

        profiler.addPortlandGroupOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 1, "profiler.addPortlandGroupOptimizationGroup should not have added any more groups")

    def test_addPortlandGroupOptimizationGroup02(self):
        compilerGroup = overrides.OverrideGroup()
        compilerGroup.compiler = "PORTLANDGROUP"
        compilerGroup.optimization = "*"
        compilerGroup.parallel = "*"
        compilerGroup["ccompiler"] = "pgcc"
        compilerGroup["cxxcompiler"] = "pgCC"
        compilerGroup["cpreprocessor"] = "cpp"
        compilerGroup["fcompiler"] = "pgf95"
        compilerGroup["f77compiler"] = "pgf77"

        groups = []
        groups.append(compilerGroup)

        profiler.addPortlandGroupOptimizationGroup(groups, compilerGroup)
        self.assertEquals(len(groups), 3, "profiler.addPortlandGroupOptimizationGroup should have added 2 more groups")
        self.assertEquals(groups[0].compiler, "PORTLANDGROUP", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0].optimization, "*", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0].parallel, "*", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["ccompiler"], "pgcc", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["cxxcompiler"], "pgCC", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["cpreprocessor"], "cpp", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["fcompiler"], "pgf95", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")
        self.assertEquals(groups[0]["f77compiler"], "pgf77", "profiler.addPortlandGroupOptimizationGroup should not have altered this value")

        portlandDebugFlags = "-g -O0"
        self.assertEquals(groups[1].compiler, "PORTLANDGROUP", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1].optimization, "debug", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1].parallel, "*", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cflags"], portlandDebugFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cxxflags"], portlandDebugFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["cppflags"], "-Wall", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["fflags"], portlandDebugFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[1]["f77flags"], portlandDebugFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")

        portlandReleaseFlags = "-O2"
        self.assertEquals(groups[2].compiler, "PORTLANDGROUP", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2].optimization, "release", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2].parallel, "*", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cflags"], portlandReleaseFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cxxflags"], portlandReleaseFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["cppflags"], "-Wall", "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["fflags"], portlandReleaseFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")
        self.assertEquals(groups[2]["f77flags"], portlandReleaseFlags, "profiler.addPortlandGroupOptimizationGroup returned wrong value")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_profiler))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
