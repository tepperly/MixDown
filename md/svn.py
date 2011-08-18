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

_isSvnInstalled = None

def isSvnInstalled():
    global _isSvnInstalled
    if _isSvnInstalled == None:
        outFile = open(os.devnull, "w")
        try:
            returnCode = utilityFunctions.executeSubProcess("svn --help", outFileHandle = outFile)
        except:
            #Assume any exceptions means Svn is not installed
            returnCode = 1
        outFile.close()
        if returnCode == 0:
            _isSvnInstalled = True
        else:
            logger.writeMessage("Svn is not installed, svn repositories will fail to be checked out")
            _isSvnInstalled = False
    return _isSvnInstalled

def isSvnRepo(location):
    location = location.strip()
    if location == "" or not isSvnInstalled():
        return False
    outFile = open(os.devnull, "w")
    returnCode = utilityFunctions.executeSubProcess("svn ls " + location, outFileHandle = outFile)
    outFile.close()
    if returnCode == 0:
        return True
    return False

def svnCheckout(repoLocation, outPath):
    repoLocation = repoLocation.strip()
    outPath = outPath.strip()
    if repoLocation == "" or outPath == "" or not isSvnInstalled():
        return False
    outFile = open(os.devnull, "w")
    returnCode = utilityFunctions.executeSubProcess("svn co --non-interactive " + repoLocation + " " + outPath, outFileHandle = outFile)
    outFile.close()
    if returnCode == 0:
        return True
    return False

