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

import os
import logger, utilityFunctions

_isGitInstalled = None

def isGitInstalled():
    global _isGitInstalled
    if _isGitInstalled == None:
        outFile = open(os.devnull, "w")
        try:
            returnCode = utilityFunctions.executeSubProcess("git --help", outFileHandle = outFile)
        except:
            #Assume any exceptions means Git is not installed
            returnCode = 1
        outFile.close()
        if returnCode == 0:
            _isGitInstalled = True
        else:
            logger.writeMessage("Git is not installed, git repositories will fail to be checked out")
            _isGitInstalled = False
    return _isGitInstalled

def isGitRepo(location):
    location = location.strip()
    if location == "" or not isGitInstalled():
        return False
    #This corrects various false positives
    filename = utilityFunctions.URLToFilename(location)
    if filename.endswith(".bz2") or filename.endswith(".gz"):
        return False
    outFile = open(os.devnull, "w")
    returnCode = utilityFunctions.executeSubProcess("git ls-remote " + location, outFileHandle = outFile)
    outFile.close()
    if returnCode == 0:
        return True
    return False

def gitCheckout(repoLocation, outPath):
    repoLocation = repoLocation.strip()
    outPath = outPath.strip()
    if repoLocation == "" or outPath == "" or not isGitInstalled():
        return False
    outFile = open(os.devnull, "w")
    returnCode = utilityFunctions.executeSubProcess("git clone " + repoLocation + " " + outPath, outFileHandle = outFile)
    outFile.close()
    if returnCode == 0:
        return True
    return False

