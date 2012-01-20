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

from md import logger, overrides, utilityFunctions

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_overrides))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
