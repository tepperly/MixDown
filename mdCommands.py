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

import mdStrings, mdOptions, os, utilityFunctions

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
        command = __getConfigureCommand(target, options.getDefine(mdStrings.mdDefinePrefix))
    elif stepName == "build":
        command = __getBuildCommand(target)
    elif stepName == "install":
        command = __getInstallCommand(target)

    if options.importer:
        return command
    return options.expandDefines(command)

def __getPreConfigureCommand(target):
    command = ""
    basePath = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if os.path.exists(basePath + "autogen.sh"):
        command = "./autogen.sh"
    elif os.path.exists(basePath + "buildconf"):
        command = "./buildconf"
    elif os.path.exists(basePath + "configure.ac") or os.path.exists(basePath + "configure.in"):
        command = "autoreconf -i"
    return command

def __getBuildCommand(target):
    command = ""
    basePath = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if os.path.exists(basePath + "GNUmakefile") or os.path.exists(basePath + "GNUmakefile.am") or os.path.exists(basePath + "GNUmakefile.in") or \
       os.path.exists(basePath + "makefile") or os.path.exists(basePath + "makefile.am") or os.path.exists(basePath + "makefile.in") or \
       os.path.exists(basePath + "Makefile") or os.path.exists(basePath + "Makefile.am") or os.path.exists(basePath + "Makefile.in"):
        command = "make $(" + mdStrings.mdMakeJobSlotsDefineName + ")"
    return command

def __getConfigureCommand(target, prefix=""):
    command = ""
    basePath = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if os.path.exists(basePath + "CMakeFileLists.txt"):
        command = "cmake -DCMAKE_PREFIX_PATH=$(" + mdStrings.mdDefinePrefix + ")"
    elif os.path.exists(basePath + "Configure"):
        command = "./Configure"
    elif os.path.exists(basePath + "configure") or os.path.exists(basePath + "configure.ac") or os.path.exists(basePath + "configure.in"):
        command = "./configure"
        if prefix != "":
            command += " --prefix=$(" + mdStrings.mdDefinePrefix + ")"
            for dependancy in target.dependsOn:
                command += " --with-" + dependancy + "=$(" + mdStrings.mdDefinePrefix + ")"
    return command

def __getInstallCommand(target):
    command = ""
    basePath = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if os.path.exists(basePath + "GNUmakefile") or os.path.exists(basePath + "GNUmakefile.am") or os.path.exists(basePath + "GNUmakefile.in") or \
       os.path.exists(basePath + "makefile") or os.path.exists(basePath + "makefile.am") or os.path.exists(basePath + "makefile.in") or \
       os.path.exists(basePath + "Makefile") or os.path.exists(basePath + "Makefile.am") or os.path.exists(basePath + "Makefile.in"):
        command = "make $(" + mdStrings.mdMakeJobSlotsDefineName + ") install"
    return command