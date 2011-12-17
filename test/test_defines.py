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

import sys, unittest

if not ".." in sys.path:
    sys.path.append("..")

from md import defines, logger

class Test_defines(unittest.TestCase):
    def test_combine(self):
        def1 = defines.Defines()
        def1.set("options", "optionsResult")
        def1.set("both", "optionsResult")
        def1.set("same", "sameResult")

        def2 = defines.Defines()
        def2.set("project", "projectResult")
        def2.set("both", "projectResultBoth")
        def2.set("same", "sameResult")

        def1.combine(def2)
        self.assertEquals(def1.get("options"), "optionsResult", "Define should have been result from def1")
        self.assertEquals(def1.get("project"), "projectResult", "Define should have been result from def2")
        self.assertEquals(def1.get("both"), "projectResultBoth", "Define should have been result from def2")
        self.assertEquals(def1.get("same"), "sameResult", "Define should have been the same result")
        self.assertEquals(def2.get("project"), "projectResult", "Define should not have changed")
        self.assertEquals(def2.get("both"), "projectResultBoth", "Define should not have changed")
        self.assertEquals(def2.get("same"), "sameResult", "Define should not have changed")

    def test_setGet(self):
        def1 = defines.Defines()
        self.assertEquals(def1.get("one"), "", "Define should have returned empty string")
        def1.set("one", "oneResult")
        self.assertEquals(def1.get("one"), "oneResult", "Define returned wrong value")
        def1.set("one", "oneResultNew")
        self.assertEquals(def1.get("one"), "oneResultNew", "Define returned wrong value")
        self.assertEquals(def1.get("one"), "oneResultNew", "Define returned wrong value after getting multiple times")
        self.assertEquals(def1.get("one"), "oneResultNew", "Define returned wrong value after getting multiple times")
        self.assertEquals(def1.get("one"), "oneResultNew", "Define returned wrong value after getting multiple times")
        def1.set("both", "bothResult")
        self.assertEquals(def1.get("both"), "bothResult", "Define returned wrong value")
        self.assertEquals(def1.get("one"), "oneResultNew", "Define returned wrong value after setting new value")

    def test_keys(self):
        def1 = defines.Defines()
        def1.set("a", "aResult")
        def1.set("b", "bResult")
        def1.set("c", "cResult")
        keys = def1.keys()
        self.assertEquals(len(keys), 3, "Length of keys returned wrong value")
        keys.sort()
        self.assertEquals(keys[0], "a", "Keys() returned wrong key")
        self.assertEquals(keys[1], "b", "Keys() returned wrong key")
        self.assertEquals(keys[2], "c", "Keys() returned wrong key")
        self.assertEquals(def1.get(keys[0]), "aResult", "Define returned wrong value when using keys")
        self.assertEquals(def1.get(keys[1]), "bResult", "Define returned wrong value when using keys")
        self.assertEquals(def1.get(keys[2]), "cResult", "Define returned wrong value when using keys")

    def test_expand(self):
        def1 = defines.Defines()
        def1.set("a", "aResult")
        def1.set("b", "bResult")
        def1.set("c", "cResult")
        self.assertEquals(def1.expand("$(a)"), "aResult", "Define returned wrong value when using expand()")
        self.assertEquals(def1.expand("$(b)"), "bResult", "Define returned wrong value when using expand()")
        self.assertEquals(def1.expand("$(c)"), "cResult", "Define returned wrong value when using expand()")

    def test_normalizeKey(self):
        self.assertEquals(defines.normalizeKey("foo"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("Foo"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("fOo"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("foO"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("FOo"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("FOO"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("fOO"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("foO"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("FOO "), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey(" FOO "), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("  FOO "), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("    FOO "), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("$(foo)"), "foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("$(foo"), "$(foo", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("foo)"), "foo)", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("(foo)"), "(foo)", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("$foo)"), "$foo)", "normalizeKey() returned wrong value")
        self.assertEquals(defines.normalizeKey("$foo"), "$foo", "normalizeKey() returned wrong value")

    def test_surround(self):
        self.assertEquals(defines.surround("foo"), "$(foo)", "surround() returned wrong value")
        self.assertEquals(defines.surround("Foo"), "$(Foo)", "surround() returned wrong value")
        self.assertEquals(defines.surround("fOo"), "$(fOo)", "surround() returned wrong value")
        self.assertEquals(defines.surround("foO"), "$(foO)", "surround() returned wrong value")
        self.assertEquals(defines.surround("FOo"), "$(FOo)", "surround() returned wrong value")
        self.assertEquals(defines.surround("FOO"), "$(FOO)", "surround() returned wrong value")
        self.assertEquals(defines.surround("fOO"), "$(fOO)", "surround() returned wrong value")
        self.assertEquals(defines.surround("foO"), "$(foO)", "surround() returned wrong value")
        self.assertEquals(defines.surround("FOO "), "$(FOO )", "surround() returned wrong value")
        self.assertEquals(defines.surround(" FOO "), "$( FOO )", "surround() returned wrong value")
        self.assertEquals(defines.surround("  FOO "), "$(  FOO )", "surround() returned wrong value")
        self.assertEquals(defines.surround("    FOO "), "$(    FOO )", "surround() returned wrong value")
        self.assertEquals(defines.surround("$(foo)"), "$($(foo))", "surround() returned wrong value")
        self.assertEquals(defines.surround("$(foo"), "$($(foo)", "surround() returned wrong value")
        self.assertEquals(defines.surround("foo)"), "$(foo))", "surround() returned wrong value")
        self.assertEquals(defines.surround("(foo)"), "$((foo))", "surround() returned wrong value")
        self.assertEquals(defines.surround("$foo)"), "$($foo))", "surround() returned wrong value")
        self.assertEquals(defines.surround("$foo"), "$($foo)", "surround() returned wrong value")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_defines))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
