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

import os, re, tarfile
import mdAutoTools, mdCMake, mdCommands, mdGit, mdHg, mdOptions, mdPython, mdSvn, utilityFunctions

from mdLogger import *

def normalizeName(name):
    return name.strip().lower()

def targetPathToName(path, exitOnFailure=True):
    name = ""
    path = path.strip()

    if mdGit.isGitRepo(path):
        if os.path.isdir(path):
            name = os.path.basename(path)
        elif utilityFunctions.isURL(path):
            name = utilityFunctions.URLToFilename(path)
            if name.endswith(".git"):
                name = name[:-4]
    elif mdSvn.isSvnRepo(path):
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
        Logger().writeError("Could not convert given target path to name: " + path, exitProgram=exitOnFailure)
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
        self.dependancyDepth = 0
        self.dependsOn = []
        self._skipSteps = []
        self.pythonCallInfo = mdPython.PythonCallInfo()
        self.commands = dict()
        for step in mdCommands.getBuildStepList():
            self.commands[step] = ""

    def validate(self, options):
        normalizedName = normalizeName(self.name)
        if normalizedName == "":
            return False
        if self.path == "":
            return False
        for alias in self.aliases:
            if normalizeName(alias) == normalizedName:
                Logger().writeError(self.name + ": Target's alias cannot be same as it's name")
                return False

        #Check for write access to install directories used in commands.
        if not options.cleanTargets:
            for step in mdCommands.getBuildStepList():
                installDir = ""
                command = self.commands[step]
                installDir = mdAutoTools.getInstallDir(command)
                if installDir == "":
                    installDir = mdCMake.getInstallDir(command)

                installDir = options.expandDefines(installDir)
                if installDir != "" and not utilityFunctions.haveWriteAccess(installDir):
                    Logger().writeError("No write access to used install directory: " + installDir, self.name, step, options.projectFile)
                    if not options.prefixDefined:
                        Logger().writeMessage("Use commandline option '-p<install path>' or running MixDown with superuser privileges (sudo)")
                    else:
                        Logger().writeMessage("Choose a different install directory for commandline option '-p<install path>'")
                    return False
        return True

    def determineOutputPath(self, options):
        if self.outputPathSpecified and self.outputPath != "":
            return self.outputPath
        else:
            targetsBuildDir = os.path.join(options.buildDir, self.name)
            if options.cleanTargets:
                if os.path.exists(targetsBuildDir) and os.path.isdir(targetsBuildDir):
                    return targetsBuildDir
                elif os.path.isdir(self.path):
                    return self.path
                else:
                    Logger().writeError("Output path could not be located, define in project file with \"output=<path>\"", self.name, "clean")
                    return ""
            else:
                options.validateBuildDir()
                return targetsBuildDir

    def examine(self, options):
        self.__determineCommands(options)
        self.outputPath = self.determineOutputPath(options)
        return True

    def __determineCommands(self, options):
        for stepName in mdCommands.getBuildStepList():
            self.commands[stepName] = mdCommands.getCommand(stepName, self, options)

    def __str__(self):
        retStr = ""
        if self.comment != "":
            retStr += "#" + self.comment
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
        for stepName in mdCommands.getBuildStepList():
            command = self.commands[stepName]
            if command != "":
                retStr += stepName.capitalize() + ": " + command + "\n"
        return retStr

    @property
    def skipSteps(self):
        return self._skipSteps

    @skipSteps.setter
    def skipSteps(self, value):
        loweredList = []
        for step in value[:]:
            loweredList.append(str.lower(step))
        self._skipSteps += loweredList

    def hasStep(self, stepName):
        if len(self._skipSteps) == 0: #no steps were specified, do all steps
            return True
        for step in self._skipSteps:
            if step.startswith(stepName):
                return False
        return True