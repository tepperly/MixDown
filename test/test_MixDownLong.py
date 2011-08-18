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

import os, socket, sys, unittest, mdTestUtilities
if not ".." in sys.path:
    sys.path.append("..")
from md import logger, utilityFunctions

class Test_MixDownLong(unittest.TestCase):
    def test_subversion(self):
        svnURL = "http://subversion.tigris.org/downloads/subversion-1.6.12.tar.bz2"
        aprURL = "http://mirror.candidhosting.com/pub/apache/apr/apr-1.4.5.tar.bz2"
        aprUtilURL = "http://mirror.candidhosting.com/pub/apache//apr/apr-util-1.3.12.tar.gz"
        neonURL = "http://www.webdav.org/neon/neon-0.29.5.tar.gz"
        sqliteURL = "http://www.sqlite.org/sqlite-autoconf-3070500.tar.gz"

        skipAPRPreconfig = ""
        if socket.gethostname() == "tux316.llnl.gov":
            skipAPRPreconfig = " -sapr:preconfig"
        try:
            mixDownPath = os.path.abspath("..")
            origPath = os.environ["PATH"]
            os.environ["PATH"] = mixDownPath + ":" + origPath

            tempDir = mdTestUtilities.makeTempDir()
            downloadDir = os.path.join(tempDir, "testDownloadFiles")

            svnPath = utilityFunctions.downloadFile(svnURL, downloadDir)
            self.assertNotEquals(svnPath, "", "Svn failed to download")

            aprPath = utilityFunctions.downloadFile(aprURL, downloadDir)
            self.assertNotEquals(aprPath, "", "Apr failed to download")

            aprUtilPath = utilityFunctions.downloadFile(aprUtilURL, downloadDir)
            self.assertNotEquals(aprUtilPath, "", "Apr Util failed to download")

            neonPath = utilityFunctions.downloadFile(neonURL, downloadDir)
            self.assertNotEquals(neonPath, "", "Neon failed to download")

            sqlitePath = utilityFunctions.downloadFile(sqliteURL, downloadDir)
            self.assertNotEquals(sqlitePath, "", "Sqlite failed to download")

            importRC = utilityFunctions.executeSubProcess("MixDown --import " + svnPath + " " + aprPath + " " + aprUtilPath + " " + neonPath + " " + sqlitePath, tempDir)
            self.assertEquals(importRC, 0, "Subversion test case failed import.")

            buildRC = utilityFunctions.executeSubProcess("MixDown subversion-1.6.12.md -ptestPrefix" + skipAPRPreconfig, tempDir)
            self.assertEquals(buildRC, 0, "Subversion test case failed build.")

            cleanRC = utilityFunctions.executeSubProcess("MixDown --clean subversion-1.6.12.md", tempDir)
            self.assertEquals(cleanRC, 0, "Subversion test case failed clean.")

            prefix = os.path.join(tempDir, "testPrefix")
            binDir = os.path.join(prefix, "bin")
            libDir = os.path.join(prefix, "lib")
            self.assertEquals(os.path.exists(os.path.join(binDir, "svn")), True, "Executable does not exist after building CMake Hello test case.")
        finally:
            utilityFunctions.removeDir(tempDir)
            os.environ["PATH"] = origPath

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_MixDownLong))
    return suite

if __name__ == "__main__":
    logger.setLogger("Console")
    unittest.main()
