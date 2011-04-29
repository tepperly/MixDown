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

import distutils, os, re, tarfile, urllib
import mdAutoTools, mdCMake, mdCommands, mdGit, mdHg, mdOptions, mdSvn, utilityFunctions

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
        if path.endswith("/"):
            path = path[:-1]
        if path.endswith("/trunk"):
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
        name = os.path.basename(path)
    else:
        Logger().writeError("Could not convert given target path to name: " + path, exitProgram=exitOnFailure)
    return name

class Target:
    def __init__(self, targetName, path=""):
        self.name = targetName
        self.aliases = []
        self.origPath = path
        self.path = path
        self.output = ""
        self.dependancyDepth = 0
        self.dependsOn = []
        self.skipSteps = []
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
                    return False
        return True

    def determineOutputDirectory(self, options):
        if self.output != "":
            return self.output
        else:
            targetsBuildDir = utilityFunctions.includeTrailingPathDelimiter(options.buildDir + self.name)
            if options.cleanTargets:
                if os.path.exists(targetsBuildDir) and os.path.isdir(targetsBuildDir):
                    return targetsBuildDir
                elif os.path.isdir(self.path):
                    return self.path
                else:
                    Logger().writeError("Output path could not be located, define in project file with \"output=<path>\"", self.name, "clean", exitProgram=True)
            else:
                options.validateBuildDir()
                return targetsBuildDir

    def extract(self, options, exitOnFailure=True):
        extracted = False
        outputDir = self.determineOutputDirectory(options)

        #Check if it is a repository (CVS, SVN, Git, Hg)
        if mdGit.isGitRepo(self.path):
            if not mdGit.gitCheckout(self.path, outputDir):
                Logger().writeError("Given Git repo '" + self.path +"' was unable to be checked out", exitProgram=exitOnFailure)
            else:
                self.path = outputDir
                extracted = True
        elif mdHg.isHgRepo(self.path):
            if not mdHg.hgCheckout(self.path, outputDir):
                Logger().writeError("Given Hg repo '" + self.path +"' was unable to be checked out", exitProgram=exitOnFailure)
            else:
                self.path = outputDir
                extracted = True
        elif mdSvn.isSvnRepo(self.path):
            if not mdSvn.svnCheckout(self.path, outputDir):
                Logger().writeError("Given Svn repo '" + self.path +"' was unable to be checked out", exitProgram=exitOnFailure)
            else:
                self.path = outputDir
                extracted = True
        elif os.path.isdir(self.path):
            if self.output != "":
                distutils.dir_util.copy_tree(self.path, self.output)
                self.path = self.output
            extracted = True
        elif not os.path.isfile(self.path) and utilityFunctions.isURL(self.path):
            options.validateDownloadDir()
            filenamePath = options.downloadDir + utilityFunctions.URLToFilename(self.path)
            urllib.urlretrieve(self.path, filenamePath)
            self.path = filenamePath

        if os.path.isfile(self.path):
            if tarfile.is_tarfile(self.path):
                utilityFunctions.untar(self.path, outputDir, True)
                self.path = outputDir
                extracted = True
            else:
                if self.path.endswith(".tar.gz") or self.path.endswith(".tar.bz2")\
                   or self.path.endswith(".tar") or self.path.endswith(".tgz")\
                   or self.path.endswith(".tbz") or self.path.endswith(".tb2"):
                    Logger().writeError("Given tar file '" + self.path +"' not understood by python's tarfile package", exitProgram=exitOnFailure)
                else:
                    Logger().writeError("Given target '" + self.path + "' not understood (Folders, URLs, Repositories, and Tar files are acceptable)", exitProgram=exitOnFailure)

        return extracted

    def examine(self, options):
        self.__determineCommands(options)
        return True

    def __determineCommands(self, options):
        for stepName in mdCommands.getBuildStepList():
            self.commands[stepName] = mdCommands.getCommand(stepName, self, options)

    def __str__(self):
        retStr = "Name: " + self.name + "\n"
        if self.origPath != "":
            retStr += "Path: " + self.origPath + "\n"
        else:
            retStr += "Path: " + self.path + "\n"
        if len(self.aliases) != 0:
            retStr += "Aliases: " + ",".join(self.aliases) + "\n"
        if self.output != "":
            retStr += "Output: " + self.output + "\n"
        if len(self.dependsOn) != 0:
            retStr += "DependsOn: " + ",".join(self.dependsOn) + "\n"
        if len(self.skipSteps) != 0:
            retStr += "SkipSteps: " + ",".join(self.skipSteps) + "\n"
        for stepName in mdCommands.getBuildStepList():
            command = self.commands[stepName]
            if command != "":
                retStr += stepName.capitalize() + ": " + command + "\n"
        return retStr

    @property
    def skipSteps(self, value):
        loweredList = []
        for step in value[:]:
            loweredList.append(str.lower(step))
        self.skipSteps = loweredList

    def hasStep(self, stepName):
        if len(self.skipSteps) == 0: #no steps were specified, do all steps
            return True
        for step in self.skipSteps:
            if step.startswith(stepName):
                return False
        return True