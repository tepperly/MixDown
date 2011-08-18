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

import os, time
import autoTools, cmake, logger, make, python, defines, target, utilityFunctions

class BuildStep(object):
    def __init__(self, name="", command=""):
        self.name = name
        self.command = command

buildSteps = ["fetch", "unpack", "patch", "preconfig", "config", "build", "install", "clean"]

def buildStepActor(target, buildStep, options):
    logger.reportStart(target.name, buildStep.name)
    returnCode = None

    timeStart = time.time()

    if target.isStepToBeSkipped(buildStep.name):
        logger.reportSkipped(target.name, buildStep.name, "Target specified to skip step")
        return True

    command = options.expandDefines(buildStep.command)
    isPythonCommand, namespace, function = python.parsePythonCommand(command)
    if isPythonCommand:
        success = python.callPythonCommand(namespace, function, target, options)
        if not success:
            returnCode = 1
        else:
            returnCode = 0
    else:
        outFd = logger.getOutFd(target.name, buildStep.name)
        returnCode = utilityFunctions.executeSubProcess(command, target.path, outFd, options.verbose)

    timeFinished = time.time()
    timeElapsed = timeFinished - timeStart

    if returnCode != 0:
        logger.reportFailure(target.name, buildStep.name, timeElapsed, returnCode)
        return False

    logger.reportSuccess(target.name, buildStep.name, timeElapsed)
    return True

def getCommand(stepName, target):
    command = ""
    if stepName == "fetch":
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

    return command

def __getFetchCommand(target):
    return "steps.fetch(pythonCallInfo)"

def __getUnpackCommand(target):
    return "steps.unpack(pythonCallInfo)"

def __getPatchCommand(target):
    return ""

def __getPreconfigureCommand(target):
    command = ""
    if cmake.isCMakeProject(target.path):
        command = cmake.getPreconfigureCommand()
    elif os.path.exists(os.path.join(target.path, "autogen.sh")):
        command = "./autogen.sh"
    elif os.path.exists(os.path.join(target.path, "buildconf")):
        command = "./buildconf"
    elif autoTools.isAutoToolsProject(target.path):
        command = autoTools.getPreconfigureCommand(target.path)
    return command

def __getConfigureCommand(target):
    command = ""
    if cmake.isCMakeProject(target.path):
        command = cmake.getConfigureCommand()
    elif os.path.exists(os.path.join(target.path, "Configure")):
        command = "./Configure"
    elif autoTools.isAutoToolsProject(target.path):
        command = autoTools.getConfigureCommand(target)
    return command

def __getBuildCommand(target):
    command = ""
    if autoTools.isAutoToolsProject(target.path):
        command = autoTools.getBuildCommand()
    elif cmake.isCMakeProject(target.path):
        command = cmake.getBuildCommand()
    elif make.isMakeProject(target.path):
        command = make.getBuildCommand()
    return command

def __getInstallCommand(target):
    command = ""
    if autoTools.isAutoToolsProject(target.path):
        command = autoTools.getInstallCommand()
    elif cmake.isCMakeProject(target.path):
        command = cmake.getInstallCommand()
    elif make.isMakeProject(target.path):
        command = make.getInstallCommand()
    return command

def __getCleanCommand(target):
    command = ""
    if autoTools.isAutoToolsProject(target.path):
        command = autoTools.getCleanCommand()
    elif cmake.isCMakeProject(target.path):
        command = cmake.getCleanCommand()
    elif make.isMakeProject(target.path):
        command = make.getCleanCommand()
    return command
