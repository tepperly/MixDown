#! /usr/bin/env python

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

import sys, unittest
import test_mdAutoTools, test_mdCMake, test_mdCvs, test_mdGit, test_mdHg, test_mdSteps, test_mdSvn, test_mdProject, test_mdTarget

if not ".." in sys.path:
    sys.path.append("..")
import mdLogger

def main():
    suite = unittest.TestSuite()

    suite.addTest(test_mdAutoTools.suite())
    suite.addTest(test_mdCMake.suite())
    #suite.addTest(test_mdCvs.suite())
    suite.addTest(test_mdGit.suite())
    suite.addTest(test_mdHg.suite())
    suite.addTest(test_mdSteps.suite())
    suite.addTest(test_mdSvn.suite())
    suite.addTest(test_mdProject.suite())
    suite.addTest(test_mdTarget.suite())

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    main()
