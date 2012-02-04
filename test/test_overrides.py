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

from md import logger, overrides, options, utilityFunctions

class Test_overrides(unittest.TestCase):
    def test_setGetOverrides1(self):
        group = overrides.OverrideGroup()
        self.assertEquals(group.getOverride("test"), None, "Non-existant override should have returned None")

    def test_setGetOverrides2(self):
        group = overrides.OverrideGroup()
        group.setOverride("test", "value")
        self.assertEquals(group.getOverride("test"), "value", "override did not returned correct value")

    def test_setGetOverrides3(self):
        group = overrides.OverrideGroup()
        group.setOverride("test", "value")
        self.assertEquals(group.getOverride("test"), "value", "override did not returned correct value")
        group.setOverride("test", "newvalue")
        self.assertEquals(group.getOverride("test"), "newvalue", "override did not returned correct value")

    def test_hasOverrides1(self):
        group = overrides.OverrideGroup()
        group.setOverride("test", "value")
        self.assertEquals(group.hasOverride("test"), True, "hasOverride did not returned correct value")

    def test_hasOverrides2(self):
        group = overrides.OverrideGroup()
        self.assertEquals(group.hasOverride("test"), False, "hasOverride did not returned correct value")

    def test_hasOverrides3(self):
        group = overrides.OverrideGroup()
        group.setOverride("test", "value")
        self.assertEquals(group.hasOverride("testasdf"), False, "hasOverride did not returned correct value")

    def test_combine1(self):
        group1 = overrides.OverrideGroup()
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")

        group2 = overrides.OverrideGroup()
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")

        group1.combine(group2)
        self.assertEquals(group1.hasOverride("test"), True, "After combine() hasOverride() did not returned correct value")
        self.assertEquals(group1.getOverride("test"), "value2", "After combine() getOverride() did not returned correct value")
        self.assertEquals(group1.hasOverride("group1Only"), True, "After combine() hasOverride() did not returned correct value")
        self.assertEquals(group1.getOverride("group1Only"), "group1OnlyValue", "After combine() getOverride() did not returned correct value")
        self.assertEquals(group1.hasOverride("group2Only"), True, "After combine() hasOverride() did not returned correct value")
        self.assertEquals(group1.getOverride("group2Only"), "group2OnlyValue", "After combine() getOverride() did not returned correct value")
        self.assertEquals(group2.hasOverride("test"), True, "After combine() hasOverride() did not returned correct value")
        self.assertEquals(group2.getOverride("test"), "value2", "After combine() getOverride() did not returned correct value")
        self.assertEquals(group2.hasOverride("group2Only"), True, "After combine() hasOverride() did not returned correct value")
        self.assertEquals(group2.getOverride("group2Only"), "group2OnlyValue", "After combine() getOverride() did not returned correct value")
        self.assertEquals(group2.hasOverride("group1Only"), False, "After combine() hasOverride() did not returned correct value")
        self.assertEquals(group2.getOverride("group1Only"), None, "After combine() getOverride() did not returned correct value")

    def test_selectGroups01(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "optimization1"
        mdOptions.parallelGroupName = "*"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertNotEquals(finalGroup, None, "selectGroups() failed to return a group")
        self.assertEquals(finalGroup.count(), 3, "After selectGroups() override count was wrong")
        self.assertEquals(finalGroup.hasOverride("test"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("test"), "value2", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group1Only"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group1Only"), "group1OnlyValue", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group2Only"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group2Only"), "group2OnlyValue", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("test"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("test"), "value2", "After selectGroups() did not returned correct value")

    def test_selectGroups02(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "*"
        mdOptions.parallelGroupName = "*"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup.count(), 2, "After selectGroups() override count was wrong")
        self.assertNotEquals(finalGroup, None, "selectGroups() failed to return a group")
        self.assertEquals(finalGroup.hasOverride("test"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("test"), "value1", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group1Only"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group1Only"), "group1OnlyValue", "After selectGroups() did not returned correct value")

    def test_selectGroups03(self):
        #regression test whether selectGroups alters original groups
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "optimization1"
        mdOptions.parallelGroupName = "*"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(group1.count(), 2, "After selectGroups(), group1 was incorrectly altered")
        self.assertEquals(group1.hasOverride("test"), True, "After selectGroups(), group1 was incorrectly altered")
        self.assertEquals(group1.getOverride("test"), "value1", "After selectGroups(), group1 was incorrectly altered")
        self.assertEquals(group1.hasOverride("group1Only"), True, "After selectGroups(), group1 was incorrectly altered")
        self.assertEquals(group1.getOverride("group1Only"), "group1OnlyValue", "After selectGroups(), group1 was incorrectly altered")
        self.assertEquals(group2.count(), 2, "After selectGroups(), group2 was incorrectly altered")
        self.assertEquals(group2.hasOverride("test"), True, "After selectGroups(), group2 was incorrectly altered")
        self.assertEquals(group2.getOverride("test"), "value2", "After selectGroups(), group2 was incorrectly altered")
        self.assertEquals(group2.hasOverride("group2Only"), True, "After selectGroups(), group2 was incorrectly altered")
        self.assertEquals(group2.getOverride("group2Only"), "group2OnlyValue", "After selectGroups(), group2 was incorrectly altered")

    def test_selectGroups04(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "optimization1"
        mdOptions.parallelGroupName = "parallel1"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2and3", "group2and3Value")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup.count(), 5, "After selectGroups() override count was wrong")
        self.assertNotEquals(finalGroup, None, "selectGroups() failed to return a group")
        self.assertEquals(finalGroup.hasOverride("test"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("test"), "value3", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group1Only"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group1Only"), "group1OnlyValue", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group2Only"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group2Only"), "group2OnlyValue", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group2and3"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group2and3"), "group2and3Value", "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.hasOverride("group3Only"), True, "After selectGroups() did not returned correct value")
        self.assertEquals(finalGroup.getOverride("group3Only"), "group3OnlyValue", "After selectGroups() did not returned correct value")

    def test_selectGroups05(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "*"
        mdOptions.optimizationGroupName = "optimization1"
        mdOptions.parallelGroupName = "parallel1"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

    def test_selectGroups06(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "*"
        mdOptions.parallelGroupName = "parallel1"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

    def test_selectGroups07(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "*"
        mdOptions.optimizationGroupName = "*"
        mdOptions.parallelGroupName = "*"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

    def test_selectGroups08(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compilerDOESNOTEXIST"
        mdOptions.optimizationGroupName = "*"
        mdOptions.parallelGroupName = "*"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

    def test_selectGroups09(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "optimizationDOESNOTEXIST"
        mdOptions.parallelGroupName = "*"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

    def test_selectGroups10(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compiler1"
        mdOptions.optimizationGroupName = "optimization1"
        mdOptions.parallelGroupName = "parallelDOESNOTEXIST"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

    def test_selectGroups11(self):
        mdOptions = options.Options()
        mdOptions.compilerGroupName = "compilerDOESNOTEXIST"
        mdOptions.optimizationGroupName = "optimizationDOESNOTEXIST"
        mdOptions.parallelGroupName = "parallelDOESNOTEXIST"
        mdOptions.overrideFile = "testNOREALFILE"

        groupList = []

        group1 = overrides.OverrideGroup()
        group1.compiler = "compiler1"
        group1.optimization = "*"
        group1.parallel = "*"
        group1.setOverride("test", "value1")
        group1.setOverride("group1Only", "group1OnlyValue")
        groupList.append(group1)

        group2 = overrides.OverrideGroup()
        group2.compiler = "compiler1"
        group2.optimization = "optimization1"
        group2.parallel = "*"
        group2.setOverride("test", "value2")
        group2.setOverride("group2Only", "group2OnlyValue")
        groupList.append(group2)

        group3 = overrides.OverrideGroup()
        group3.compiler = "compiler1"
        group3.optimization = "optimization1"
        group3.parallel = "parallel1"
        group3.setOverride("test", "value3")
        group3.setOverride("group2and3", "group2and3Value")
        group3.setOverride("group3Only", "group3OnlyValue")
        groupList.append(group3)

        finalGroup = overrides.selectGroups(groupList, mdOptions)
        self.assertEquals(finalGroup, None, "selectGroups() should have failed to return a group")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_overrides))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
