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
import defines

def isMakeProject(path):
    if os.path.exists(os.path.join(path, "GNUmakefile")) or\
       os.path.exists(os.path.join(path, "GNUmakefile.am")) or\
       os.path.exists(os.path.join(path, "GNUmakefile.in")) or\
       os.path.exists(os.path.join(path, "makefile")) or\
       os.path.exists(os.path.join(path, "makefile.am")) or\
       os.path.exists(os.path.join(path, "makefile.in")) or\
       os.path.exists(os.path.join(path, "Makefile")) or\
       os.path.exists(os.path.join(path, "Makefile.am")) or\
       os.path.exists(os.path.join(path, "Makefile.in")):
        return True
    return False

def getPreconfigureCommand():
    #There is no preconfigure command for Make
    return ""

def getConfigureCommand():
    #There is no configure command for Make
    return ""

def getBuildCommand():
    return "make " + defines.surround(defines.makeJobSlots[0])

def getInstallCommand():
    return "make " + defines.surround(defines.makeJobSlots[0]) + " install"

def getCleanCommand():
    return "make " + defines.surround(defines.makeJobSlots[0]) + " clean"
