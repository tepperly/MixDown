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

import os, re, tarfile
import autoTools, cmake, commands, git, hg, logger, options, python, svn, utilityFunctions

def normalizeName(name):
    return name.strip().lower()

def targetPathToName(path, exitOnFailure=True):
    name = ""
    path = path.strip()

    if git.isGitRepo(path):
        if os.path.isdir(path):
            name = os.path.basename(path)
        elif utilityFunctions.isURL(path):
            name = utilityFunctions.URLToFilename(path)
            if name.endswith(".git"):
                name = name[:-4]
    elif svn.isSvnRepo(path):
        if path.endswith(os.sep):
            path = path[:-1]
        if path.endswith("/trunk") or path.endswith("\trunk"):
            path = path[:-6]
        if os.path.isdir(path):
            name = os.path.basename(path)
        elif utilityFunctions.isURL(path):
            name = utilityFunctions.URLToFilename(path)
    elif utilityFunctions.isURL(path):
        name = utilityFunctions.URLToFilename(path)
        name = utilityFunctions.splitFileName(name)[0]
    elif os.path.isfile(path) and tarfile.is_tarfile(path):
        name = utilityFunctions.splitFileName(path)[0]
    elif os.path.isdir(path):
        if path.endswith(os.sep):
            name = os.path.basename(path[:-1])
        else:
            name = os.path.basename(path)
    else:
        logger.writeError("Could not convert given target path to name: " + path, exitProgram=exitOnFailure)
    return name

class Target(object):
    def __init__(self, targetName, path=""):
        self.comment = ""
        self.name = targetName
        self.aliases = []
        self.origPath = path
        self.path = path
        self.outputPath = ""
        self.outputPathSpecified = False
        self.dependencyDepth = 0
        self.dependsOn = []
        self._skipSteps = []
        self.pythonCallInfo = python.PythonCallInfo()
        self.buildSteps = []

    def validate(self, option):
        normalizedName = normalizeName(self.name)
        if normalizedName == "":
            return False
        if self.path == "":
            return False
        for alias in self.aliases:
            if normalizeName(alias) == normalizedName:
                logger.writeError(self.name + ": Target's alias cannot be same as it's name")
                return False

        #Check for write access to install directories used in commands.
        if not option.cleanTargets:
            for buildStep in self.buildSteps:
                installDir = autoTools.getInstallDir(buildStep.command)
                if installDir == "":
                    installDir = cmake.getInstallDir(buildStep.command)

                installDir = option.expandDefines(installDir)
                if installDir != "" and not utilityFunctions.haveWriteAccess(installDir):
                    logger.writeError("No write access to used install directory: " + installDir, self.name, step, options.projectFile)
                    if not option.prefixDefined:
                        logger.writeMessage("Use commandline option '-p<install path>' or running MixDown with superuser privileges (sudo)")
                    else:
                        logger.writeMessage("Choose a different install directory for commandline option '-p<install path>'")
                    return False
        return True

    def determineOutputPath(self, option):
        if self.outputPathSpecified and self.outputPath != "":
            return self.outputPath
        else:
            targetsBuildDir = os.path.join(option.buildDir, self.name)
            if option.cleanTargets:
                if os.path.exists(targetsBuildDir) and os.path.isdir(targetsBuildDir):
                    return targetsBuildDir
                elif os.path.isdir(self.path):
                    return self.path
                else:
                    logger.writeError("Output path could not be located, define in project file with \"output=<path>\"", self.name, "clean")
                    return ""
            else:
                option.validateBuildDir()
                return targetsBuildDir

    def examine(self, option):
        if option.importer:
            self.__determineCommands(option)
        self.outputPath = self.determineOutputPath(option)
        return True

    def expandDefines(self, option):
        for buildStep in self.buildSteps:
            buildStep.command = option.expandDefines(buildStep.command)

    def __determineCommands(self, option):
        for stepName in commands.buildSteps:
            buildStep = commands.BuildStep(stepName, commands.getCommand(stepName, self))
            self.buildSteps.append(buildStep)

    def __str__(self):
        retStr = ""
        if self.comment != "":
            if self.comment.endswith("\n"):
                retStr += "#" + self.comment
            else:
                retStr += "#" + self.comment + "\n"
        retStr += "Name: " + self.name + "\n"
        if self.origPath != "":
            retStr += "Path: " + self.origPath + "\n"
        else:
            retStr += "Path: " + self.path + "\n"
        if len(self.aliases) != 0:
            retStr += "Aliases: " + ",".join(self.aliases) + "\n"
        if self.outputPathSpecified:
            retStr += "Output: " + self.outputPath + "\n"
        if len(self.dependsOn) != 0:
            retStr += "DependsOn: " + ",".join(self.dependsOn) + "\n"
        if len(self._skipSteps) != 0:
            retStr += "SkipSteps: " + ",".join(self._skipSteps) + "\n"
        for buildStep in self.buildSteps:
            retStr += buildStep.name.capitalize() + ": " + buildStep.command + "\n"
        return retStr

    def findBuildStep(self, name):
        for buildStep in self.buildSteps:
            if buildStep.name == name:
                return buildStep
        return None

    @property
    def skipSteps(self):
        return self._skipSteps

    @skipSteps.setter
    def skipSteps(self, steps):
        loweredList = []
        for step in steps[:]:
            loweredList.append(str.lower(step))
        self._skipSteps += loweredList

    def isStepToBeSkipped(self, stepName):
        for step in self._skipSteps:
            if step.startswith(stepName):
                return True
        return False
