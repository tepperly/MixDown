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

import os, mdStrings, utilityFunctions

def isMakeProject(path):
    path = utilityFunctions.includeTrailingPathDelimiter(path)
    if os.path.exists(path + "GNUmakefile") or os.path.exists(path + "GNUmakefile.am") or os.path.exists(path + "GNUmakefile.in") or \
       os.path.exists(path + "makefile") or os.path.exists(path + "makefile.am") or os.path.exists(path + "makefile.in") or \
       os.path.exists(path + "Makefile") or os.path.exists(path + "Makefile.am") or os.path.exists(path + "Makefile.in"):
        return True
    return False

def getPreconfigureCommand():
    #There is no preconfigure command for Make
    return ""

def getConfigureCommand():
    #There is no configure command for Make
    return ""

def getBuildCommand():
    return "make $(" + mdStrings.mdMakeJobSlotsDefineName + ")"

def getInstallCommand():
    return "make $(" + mdStrings.mdMakeJobSlotsDefineName + ") install"

def getCleanCommand():
    return "make $(" + mdStrings.mdMakeJobSlotsDefineName + ") clean"
