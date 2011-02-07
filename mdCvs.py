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

import mdLogger, os

from utilityFunctions import *

_isCvsInstalled = None

def isCvsInstalled():
    global _isCvsInstalled
    if _isCvsInstalled == None:
        outFile = open(os.devnull, "w")
        returnCode = executeSubProcess("cvs --help", outFileHandle = outFile)
        outFile.close()
        if returnCode == 0:
            _isCvsInstalled = True
        else:
            mdLogger.Logger().writeMessage("Cvs is not installed, cvs repositories will fail to be checked out")
            _isCvsInstalled = False
    return _isCvsInstalled

def isCvsRepo(location):
    location = location.strip()
    if location == "" or not isCvsInstalled():
        return False
    outFile = open(os.devnull, "w")
    #TODO: this does not work...
    returnCode = executeSubProcess("cvs log " + location, outFileHandle = outFile)
    outFile.close()
    if returnCode == 0:
        return True
    return False

def cvsCheckout(repoLocation, outPath):
    repoLocation = repoLocation.strip()
    outPath = outPath.strip()
    if repoLocation == "" or outPath == "" or not isCvsInstalled():
        return False
    outFile = open(os.devnull, "w")
    returnCode = executeSubProcess("cvs co --non-interactive --quiet " + repoLocation + " " + outPath, outFileHandle = outFile)
    outFile.close()
    if returnCode == 0:
        return False
    return True
    
    