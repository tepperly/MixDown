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

import os, utilityFunctions, mdAutoTools, mdCMake, mdMake, mdStrings, mdTarget, mdOptions

from mdLogger import *

def getBuildStepList():
    return ["fetch", "unpack", "preconfig", "config", "build", "install", "clean"]

def getCommand(stepName, target, options):
    command = ""
    if target.commands.has_key(stepName) and target.commands[stepName] != "":
        command = target.commands[stepName]
    elif stepName == "preconfig":
        command = __getPreconfigureCommand(target)
    elif stepName == "config":
        command = __getConfigureCommand(target)
    elif stepName == "build":
        command = __getBuildCommand(target)
    elif stepName == "install":
        command = __getInstallCommand(target)
    elif stepName == "clean" and (options.cleanTargets or options.importer):
        #Do not return a clean command unless we are importing or specifying we are cleaning targets
        command = __getCleanCommand(target)
    #Do not try to determine fetch and unpack, these are for overwriting default behavior only

    if options.importer:
        return command
    return options.expandDefines(command)

def __getPreconfigureCommand(target):
    command = ""
    path = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if mdCMake.isCMakeProject(path):
        command = mdCMake.getPreconfigureCommand()
    elif os.path.exists(path + "autogen.sh"):
        command = "./autogen.sh"
    elif os.path.exists(path + "buildconf"):
        command = "./buildconf"
    elif mdAutoTools.isAutoToolsProject(path):
        command = mdAutoTools.getPreconfigureCommand()
    return command

def __getConfigureCommand(target):
    command = ""
    path = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if mdCMake.isCMakeProject(path):
        command = mdCMake.getConfigureCommand()
    elif os.path.exists(path + "Configure"):
        command = "./Configure"
    elif mdAutoTools.isAutoToolsProject(path):
        command = mdAutoTools.getConfigureCommand(target)
    return command

def __getBuildCommand(target):
    command = ""
    path = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if mdMake.isMakeProject(path):
        command = mdMake.getBuildCommand()
    return command

def __getInstallCommand(target):
    command = ""
    path = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if mdMake.isMakeProject(path):
        command = mdMake.getInstallCommand()
    return command

def __getCleanCommand(target):
    command = ""
    path = utilityFunctions.includeTrailingPathDelimiter(target.path)
    if mdMake.isMakeProject(path):
        command = mdMake.getCleanCommand()
    return command
