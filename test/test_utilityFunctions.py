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
from md import logger, utilityFunctions

class Test_utilityFunctions(unittest.TestCase):
    def test_pathExists1(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = mdTestUtilities.makeTempFile(tempDir)
            self.assertEquals(utilityFunctions.pathExists(tempFile), True, "pathExists should have returned True")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_pathExists2(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = mdTestUtilities.makeTempFile(tempDir)
            self.assertEquals(utilityFunctions.pathExists(tempFile, True), True, "pathExists should have returned True")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_pathExists3(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            tempFile = mdTestUtilities.createBlankFile(os.path.join(tempDir, "test"))
            self.assertEquals(utilityFunctions.pathExists(os.path.join(tempDir, "TeSt"), True), False, "pathExists should have returned False")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_pathExists4(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            self.assertEquals(utilityFunctions.pathExists(os.path.join(tempDir, "test"), True), False, "pathExists should have returned False")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_pathExists5(self):
        try:
            tempDir = mdTestUtilities.makeTempDir()
            directory = os.path.join(tempDir, "testDir")
            os.makedirs(directory)
            mdTestUtilities.createBlankFile(os.path.join(directory, "test"))
            wrongPath = os.path.join(os.path.join(tempDir, "TeStDiR"), "test")
            self.assertEquals(utilityFunctions.pathExists(wrongPath, True), False, "pathExists should have returned False")
        finally:
            utilityFunctions.removeDir(tempDir)

    def test_URLToFileName01(self):
        url = "http://sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar.bz2/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tar.bz2", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName02(self):
        url = "http://sf.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar.bz2/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tar.bz2", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName03(self):
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar.bz2/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tar.bz2", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName04(self):
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tar", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName05(self):
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tb2/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tb2", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName06(self):
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tbz/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tbz", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName07(self):
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar.gz/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tar.gz", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName08(self):
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tgz/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tgz", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName09(self):
        #Check for false positive
        url = "http://www.sourceforge.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "download", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName10(self):
        #Check for false positive
        url = "http://www.oioioi.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar.bz2/download"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "download", "Wrong filename '" + filename + "' returned from function")

    def test_URLToFileName11(self):
        url = "http://www.sf.net/projects/pymol/files/pymol/1.4.1/pymol-v1.4.1.tar.bz2"
        filename = utilityFunctions.URLToFilename(url)
        self.assertEquals(filename, "pymol-v1.4.1.tar.bz2", "Wrong filename '" + filename + "' returned from function")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_utilityFunctions))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
