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

import os, mdMake, mdStrings, mdTarget, utilityFunctions

def isAutoToolsProject(path):
    path = utilityFunctions.includeTrailingPathDelimiter(path)
    if os.path.exists(path + "configure") or os.path.exists(path + "configure.ac") or os.path.exists(path + "configure.in"):
        return True
    return False

def getPreconfigureCommand():
    return "autoreconf -i"

def getConfigureCommand(target):
    command = "./configure --prefix=$(" + mdStrings.mdDefinePrefix + ")"
    for dependancy in target.dependsOn:
        command += " --with-" + dependancy + "=$(" + mdStrings.mdDefinePrefix + ")"
    return command

def getBuildCommand():
    return mdMake.getBuildCommand()

def getInstallCommand():
    return mdMake.getInstallCommand()
