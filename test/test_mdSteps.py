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

import os, sys, tarfile, unittest, mdTestUtilities

if not ".." in sys.path:
    sys.path.append("..")
import mdGit, mdHg, mdLogger, mdPython, mdSteps, mdSvn, utilityFunctions

def createPythonCallInfo(currentPath="", outputPath="", downloadDir=""):
    pci = mdPython.PythonCallInfo()
    pci.success = False
    pci.currentPath = currentPath
    pci.outputPath = outputPath
    pci.downloadDir = downloadDir
    pci.logger = mdLogger.Logger()
    return pci

class Test_mdSteps(unittest.TestCase):
    def _test_fetchCvs(self):
        if not mdCvs.isCvsInstalled():
            self.fail("Cvs is not installed on your system.  All Cvs tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createCvsRepository(tempDir)
            pci = createPythonCallInfo(repoPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            testFilePath = os.path.join(pci.outputPath, mdTestUtilities.testFileName)
            self.assertEqual(pci.success, True, "Cvs repository failed to fetch.")
            self.assertEqual(os.path.exists(testFilePath), True, "'" + mdTestUtilities.testFileName + "' did not exist after fetching a Cvs repository.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchGit(self):
        if not mdGit.isGitInstalled():
            self.fail("Git is not installed on your system.  All Git tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createGitRepository(tempDir)
            pci = createPythonCallInfo(repoPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            testFilePath = os.path.join(pci.outputPath, mdTestUtilities.testFileName)
            self.assertEqual(pci.success, True, "Hg repository failed to fetch.")
            self.assertEqual(os.path.exists(testFilePath), True, "'" + mdTestUtilities.testFileName + "' did not exist after fetching a Git repository.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchHg(self):
        if not mdHg.isHgInstalled():
            self.fail("Hg is not installed on your system.  All Hg tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createHgRepository(tempDir)
            pci = createPythonCallInfo(repoPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            testFilePath = os.path.join(pci.outputPath, mdTestUtilities.testFileName)
            self.assertEqual(pci.success, True, "Hg repository failed to fetch.")
            self.assertEqual(os.path.exists(testFilePath), True, "'" + mdTestUtilities.testFileName + "' did not exist after fetching a Hg repository.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchSvn(self):
        if not mdSvn.isSvnInstalled():
            self.fail("Svn is not installed on your system.  All Svn tests will fail.")
        try:
            tempDir = mdTestUtilities.makeTempDir()
            repoPath = mdTestUtilities.createSvnRepository(tempDir)
            pci = createPythonCallInfo(repoPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            testFilePath = os.path.join(pci.outputPath, mdTestUtilities.testFileName)
            self.assertEqual(pci.success, True, "Svn repository failed to fetch.")
            self.assertEqual(os.path.exists(testFilePath), True, "'" + mdTestUtilities.testFileName + "' did not exist after fetching a Svn repository.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchTar(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarName = mdTestUtilities.createTarFile(tempDir)
            tarPath = os.path.join(tempDir, tarName)
            pci = createPythonCallInfo(tarPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            self.assertEqual(pci.success, True, "Local tar file failed to fetch.")
            self.assertEqual(os.path.exists(pci.currentPath), True, "Tar file did not exist after fetching.")
            self.assertEqual(tarfile.is_tarfile(pci.currentPath), True, "Tar file was not a tar file after fetching.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchBzip(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarName = mdTestUtilities.createBzipFile(tempDir)
            tarPath = os.path.join(tempDir, tarName)
            pci = createPythonCallInfo(tarPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            self.assertEqual(pci.success, True, "Local Bzip file failed to fetch.")
            self.assertEqual(os.path.exists(pci.currentPath), True, "Bzip file did not exist after fetching.")
            self.assertEqual(tarfile.is_tarfile(pci.currentPath), True, "Bzip file was not a tar file after fetching.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchGzip(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarName = mdTestUtilities.createGzipFile(tempDir)
            tarPath = os.path.join(tempDir, tarName)
            pci = createPythonCallInfo(tarPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            self.assertEqual(pci.success, True, "Local Gzip file failed to fetch.")
            self.assertEqual(os.path.exists(pci.currentPath), True, "Gzip file did not exist after fetching.")
            self.assertEqual(tarfile.is_tarfile(pci.currentPath), True, "Gzip file was not a tar file after fetching.")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_fetchURL(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tarDir, tarName = mdTestUtilities.createGzipFile(tempDir)
            urlPath = "http://ftp.gnu.org/gnu/autoconf/autoconf-2.68.tar.gz"
            pci = createPythonCallInfo(urlPath, os.path.join(tempDir, "output"), os.path.join(tempDir, "download"))
            pci = mdSteps.fetch(pci)
            self.assertEqual(pci.success, True, "Gzip file failed to fetch from URL.")
            self.assertEqual(os.path.exists(pci.currentPath), True, "Gzip file did not exist after fetching.")
            self.assertEqual(tarfile.is_tarfile(pci.currentPath), True, "Gzip file was not a tar file after fetching.")
        finally:
            utilityFunctions.removeDir(tempDir)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_mdSteps))
    return suite

if __name__ == "__main__":
    mdLogger.SetLogger("Console")
    unittest.main()