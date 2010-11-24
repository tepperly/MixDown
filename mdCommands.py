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

import mdOptions, os, utilityFunctions

from mdLogger import *
from mdTarget import *

def getBuildStepList():
    return ["preconfig", "config", "build", "install"]

def getCommand(stepName, target, options):
    command = ""
    if target.commands.has_key(stepName) and target.commands[stepName] != "":
        command = target.commands[stepName]
    elif stepName == "preconfig":
        command = __getPreConfigureCommand(target)
    elif stepName == "config":
        command = __getConfigureCommand(target, options.getDefine("prefix"))
    elif stepName == "build":
        command = __getBuildCommand(target)
    elif stepName == "install":
        command = __getInstallCommand(target)
    
    if options.importer:
        return command
    return options.expandDefines(command)

def __getPreConfigureCommand(target):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if basename in ['buildconf']:
                command = "./buildconf"
    return command

def __getBuildCommand(target):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if str.lower(basename) in ["GNUmakefile", "makefile", "Makefile", "GNUmakefile.in", "makefile.in", "Makefile.in", "GNUmakefile.am", "makefile.am", "Makefile.am"]:
                command = "make"
    return command

def __getConfigureCommand(target, prefix=""):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if str.lower(basename) in ['configure']:
                command = "./configure"
                if prefix != "":
                    command += " --prefix=" + prefix
                    for dependancy in target.dependsOn:
                        command += " --with-" + dependancy + "=" + prefix
    return command

def __getInstallCommand(target):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if str.lower(basename) in ["GNUmakefile", "makefile", "Makefile", "GNUmakefile.in", "makefile.in", "Makefile.in", "GNUmakefile.am", "makefile.am", "Makefile.am"]:
                command = "make install"
    return command