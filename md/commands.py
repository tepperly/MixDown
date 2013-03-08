# Copyright (c) 2010-2012, Lawrence Livermore National Security, LLC
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

import os, multiprocessing, sys, time
import autoTools, cmake, logger, make, python, defines, target, utilityFunctions

class BuildStep(object):
    def __init__(self, name="", command=""):
        self.name = name
        self.command = command
        self.restartPath = "" #Note: saved for incase build needs to be restarted, not used during building (target.path is)
        self.success = False

buildSteps = ["fetch", "unpack", "patch", "preconfig", "config", "build", "test", "install", "clean"]

def buildStepActor(target, buildStep, options, lock=None):
    if target.isStepToBeSkipped(buildStep.name):
        try:
            if lock:
                lock.acquire()
            logger.reportSkipped(target.name, buildStep.name, "Target specified to skip step")
        finally:
            if lock:
                lock.release()
        return True

    if target.isStepPreviouslyDone(buildStep.name):
        try:
            if lock:
                lock.acquire()
            logger.reportSkipped(target.name, buildStep.name, "Build step successfully built in previous MixDown build")
        finally:
            if lock:
                lock.release()
        return True

    try:
        if lock:
            lock.acquire()
        logger.reportStart(target.name, buildStep.name)
    finally:
        if lock:
            lock.release()
    returnCode = None

    timeStart = time.time()
    command = options.defines.expand(buildStep.command)
    isPythonCommand, namespace, function = python.parsePythonCommand(command)
    if isPythonCommand:
        success = python.callPythonCommand(namespace, function, target, options)
        if not success:
            returnCode = success == 0
        else:
            returnCode = 0
    else:
        try:
            if lock:
                lock.acquire()
            logger.writeMessage("Executing command: " + command, target.name, buildStep.name, True)
        finally:
            if lock:
                lock.release()

        if not os.path.exists(target.path):
            logger.writeError(target.name + "'s path does not exist when about to execute build command in step " + buildStep.name + ".", filePath=target.path)
            returnCode = 1
        else:
            outFd = logger.getOutFd(target.name, buildStep.name)
            returnCode = utilityFunctions.executeSubProcess(command, target.path, outFd)

    timeFinished = time.time()
    timeElapsed = timeFinished - timeStart

    if returnCode != 0:
        buildStep.success = False
        try:
            if lock:
                lock.acquire()
            logger.reportFailure(target.name, buildStep.name, timeElapsed, returnCode)
        finally:
            if lock:
                lock.release()
        return False

    buildStep.success = True
    try:
        if lock:
            lock.acquire()
        logger.reportSuccess(target.name, buildStep.name, timeElapsed)
    finally:
        if lock:
            lock.release()
    return True

def buildTarget(target, options, lock=None):
    if options.cleanMode:
        cleanStep = target.findBuildStep("clean")
        target.success = buildStepActor(target, cleanStep, options, lock)
    else:
        if target.success:
            logger.reportSkipped(target.name, "", "Target successfully built in previous MixDown build")
        elif target.prefix != "" and os.path.exists(options.defines.expand(target.prefix)):
            logger.reportSkipped(target.name, "", "Target's defined prefix detected.")
            target.success = True
        else:
            for buildStep in target.buildSteps:
                buildStep.restartPath = target.path
                if buildStep.name == "clean" or buildStep.command == "":
                    continue
                target.success = buildStepActor(target, buildStep, options, lock)
                if not target.success:
                    break

def buildTargetThreaded(jobQueue, resultQueue, options, lock):
    target = None
    while True:
        target = jobQueue.get(False)
        if target == None:
            sys.exit(0)
        buildTarget(target, options, lock)
        resultQueue.put(target)

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
    elif autoTools.isAutoToolsProject(target.path):
        command = autoTools.getPreconfigureCommand(target.path)
    return command

def __getConfigureCommand(target):
    command = ""
    if cmake.isCMakeProject(target.path):
        command = cmake.getConfigureCommand()
    elif autoTools.isAutoToolsProject(target.path):
        command = autoTools.getConfigureCommand(target)
    elif utilityFunctions.pathExists(os.path.join(target.path, "Configure"), True):
        command = "./Configure"
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
