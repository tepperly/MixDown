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
import mdCvs, mdSvn, mdGit, mdHg, mdLogger, mdTarget, utilityFunctions

class test_mdTarget(unittest.TestCase):
    def test_extractCvs(self):
        if not mdCvs.isCvsInstalled():
            self.fail("Cvs is not installed on your system.  All Cvs tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createCvsRepository()
            target = mdTarget.Target("CvsTarget", repoPath)
            target.extract(tempDir, False)
            returnValue = os.path.exists(tempDir + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Cvs repository as its path.")

    def test_extractGit(self):
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createGitRepository()
            target = mdTarget.Target("GitTarget", repoPath)
            target.extract(tempDir, False)
            returnValue = os.path.exists(tempDir + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Git repository as its path.")

    def test_extractHg(self):
        if not mdHg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createHgRepository()
            target = mdTarget.Target("HgTarget", repoPath)
            target.extract(tempDir, False)
            returnValue = os.path.exists(tempDir + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Hg repository as its path.")

    def test_extractSvn(self):
        if not mdSvn.isSvnInstalled():
            self.fail("Svn is not installed on your system.  All Svn tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createSvnRepository()
            target = mdTarget.Target("SvnTarget", repoPath)
            target.extract(tempDir, False)
            returnValue = os.path.exists(tempDir + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tempDir)
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Svn repository as its path.")

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()