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

import os, time, utilityFunctions
import mdAutoTools, mdCMake, mdMake, mdOptions, mdPython, mdStrings, mdTarget, utilityFunctions

from mdLogger import *

def getBuildStepList():
    return ["fetch", "unpack", "patch", "preconfig", "config", "build", "install", "clean"]

def buildStepActor(stepName, target, options, verbose=True):
    if verbose:
        Logger().reportStart(target.name, stepName)
    returnCode = None

    timeStart = time.time()

    if target.hasStep(stepName):
        command = getCommand(stepName, target, options)
        if command != "":
            isPythonCommand, namespace, function = mdPython.parsePythonCommand(command)
            if isPythonCommand:
                success = mdPython.callPythonCommand(namespace, function, target, options)
                if not success:
                    returnCode = 1
                else:
                    returnCode = 0
            else:
                outFd = Logger().getOutFd(target.name, stepName)
                returnCode = utilityFunctions.executeSubProcess(command, target.path, outFd, options.verbose)
        else:
            skipReason = "Command could not be determined by MixDown"
    else:
        skipReason = "Target specified to skip step"

    timeFinished = time.time()
    timeElapsed = timeFinished - timeStart

    if returnCode == None:
        if verbose:
            Logger().reportSkipped(target.name, stepName, skipReason)
    elif returnCode != 0:
        if verbose:
            Logger().reportFailure(target.name, stepName, timeElapsed, returnCode)
        return False
    else:
        if verbose:
            Logger().reportSuccess(target.name, stepName, timeElapsed)
    return True

def getCommand(stepName, target, options):
    command = ""
    if target.commands.has_key(stepName) and target.commands[stepName] != "":
        command = target.commands[stepName]
    elif stepName == "fetch":
        command = __getFetchCommand(target)
    elif stepName == "unpack":
        command = __getUnpackCommand(target)
    elif stepName == "patch":
        command = __getPatchCommand(target)
    elif stepName == "preconfig":
        command = __getPreconfigureCommand(target)
    elif stepName == "config":
        command = __getConfigureCommand(target)
    elif stepName == "build":
        command = __getBuildCommand(target)
    elif stepName == "install":
        command = __getInstallCommand(target)
    elif stepName == "clean":
        command = __getCleanCommand(target)

    if options.importer:
        return command
    return options.expandDefines(command)

def __getFetchCommand(target):
    return "mdSteps.fetch(pythonCallInfo)"

def __getUnpackCommand(target):
    return "mdSteps.unpack(pythonCallInfo)"

def __getPatchCommand(target):
    return ""

def __getPreconfigureCommand(target):
    command = ""
    if mdCMake.isCMakeProject(target.path):
        command = mdCMake.getPreconfigureCommand()
    elif os.path.exists(os.path.join(target.path, "autogen.sh")):
        command = "./autogen.sh"
    elif os.path.exists(os.path.join(target.path, "buildconf")):
        command = "./buildconf"
    elif mdAutoTools.isAutoToolsProject(target.path):
        command = mdAutoTools.getPreconfigureCommand(target.path)
    return command

def __getConfigureCommand(target):
    command = ""
    if mdCMake.isCMakeProject(target.path):
        command = mdCMake.getConfigureCommand()
    elif os.path.exists(os.path.join(target.path, "Configure")):
        command = "./Configure"
    elif mdAutoTools.isAutoToolsProject(target.path):
        command = mdAutoTools.getConfigureCommand(target)
    return command

def __getBuildCommand(target):
    command = ""
    if mdMake.isMakeProject(target.path):
        command = mdMake.getBuildCommand()
    return command

def __getInstallCommand(target):
    command = ""
    if mdMake.isMakeProject(target.path):
        command = mdMake.getInstallCommand()
    return command

def __getCleanCommand(target):
    command = ""
    if mdMake.isMakeProject(target.path):
        command = mdMake.getCleanCommand()
    return command
