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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_hg))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
