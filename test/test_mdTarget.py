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

class test_mdTarget(unittest.TestCase):
    def setUp(self):
        self.testDir = mdTestUtilities.makeTempDir()
        self.options = mdOptions.Options()
        self.options.buildDir = self.testDir + "mdBuild"

    def tearDown(self):
        if os.path.exists(self.testDir):
            utilityFunctions.removeDir(self.testDir)
        self.testDir = ""

    def test_extractCvs(self):
        if not mdCvs.isCvsInstalled():
            self.fail("Cvs is not installed on your system.  All Cvs tests will fail.")
        try:
            repoPath = mdTestUtilities.createCvsRepository()
            target = mdTarget.Target("CvsTarget", repoPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(extracted, True, "Cvs repository failed to extract.")
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Cvs repository as its path.")

    def test_extractGit(self):
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")
        try:
            repoPath = mdTestUtilities.createGitRepository()
            target = mdTarget.Target("GitTarget", repoPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path+ mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(extracted, True, "Git repository failed to extract.")
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Git repository as its path.")

    def test_extractHg(self):
        if not mdHg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        try:
            repoPath = mdTestUtilities.createHgRepository()
            target = mdTarget.Target("HgTarget", repoPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(extracted, True, "Hg repository failed to extract.")
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Hg repository as its path.")

    def test_extractSvn(self):
        if not mdSvn.isSvnInstalled():
            self.fail("Svn is not installed on your system.  All Svn tests will fail.")
        try:
            repoPath = mdTestUtilities.createSvnRepository()
            target = mdTarget.Target("SvnTarget", repoPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(repoPath)
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Svn repository as its path.")

    def test_extractTar(self):
        try:
            tarDir, tarName = mdTestUtilities.createTarFile()
            tarPath = tarDir + tarName
            target = mdTarget.Target("TarTarget", tarPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tarDir)
        self.assertEqual(extracted, True, "Tar file failed to extract.")
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Tar file as its path.")

    def test_extractBzip(self):
        try:
            tarDir, tarName = mdTestUtilities.createBzipFile()
            tarPath = tarDir + tarName
            target = mdTarget.Target("BzipTarget", tarPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tarDir)
        self.assertEqual(extracted, True, "BZip file failed to extract.")
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Bzip file as its path.")

    def test_extractGzip(self):
        try:
            tarDir, tarName = mdTestUtilities.createGzipFile()
            tarPath = tarDir + tarName
            target = mdTarget.Target("GzipTarget", tarPath)
            extracted = target.extract(self.options, False)
            returnValue = os.path.exists(target.path + mdTestUtilities.testFileName)
        finally:
            utilityFunctions.removeDir(tarDir)
        self.assertEqual(extracted, True, "Gzip file failed to extract.")
        self.assertEqual(returnValue, True, "'" + mdTestUtilities.testFileName + "' did not exist after extracting a target with a Gzip file as its path.")

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()