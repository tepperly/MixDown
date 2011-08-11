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

import os, re, shutil, sys, tarfile, tempfile, urllib

from md import autoTools, cmake, commands, make, project,  target, utilityFunctions

from logger import *

def importTargets(options, targetsToImport):
    SetLogger("console")

    finalTargets = []
    ignoredTargets = []
    partialImport = False
    fetchStep = commands.BuildStep("fetch", commands.__getFetchCommand(None))
    unpackStep = commands.BuildStep("unpack", commands.__getUnpackCommand(None))

    tempDir = tempfile.mkdtemp(prefix="mixdown-")
    options.downloadDir = os.path.join(tempDir, "mdDownloads")

    while len(targetsToImport) != 0:
        target = targetsToImport.pop(0)

        Logger().writeMessage("Analyzing target...", target.name)
        Logger().writeMessage("Extracting target...", target.name)

        target.outputPath = os.path.join(tempDir, target.name)
        if not commands.buildStepActor(target, fetchStep, options):
            utilityFunctions.removeDir(tempDir)
            return None, False
        if not commands.buildStepActor(target, unpackStep, options):
            utilityFunctions.removeDir(tempDir)
            return None, False

        #Generate build files and find possible dependancies
        possibleDeps = []
        if cmake.isCMakeProject(target.path):
            Logger().writeMessage("CMake project found...", target.name)
            Logger().writeMessage("Analyzing for dependancies...", target.name)
            possibleDeps = cmake.getDependancies(target.path, target.name)
        elif autoTools.isAutoToolsProject(target.path):
            Logger().writeMessage("Auto Tools project found...", target.name)
            if not os.path.exists(os.path.join(target.path, "configure")):
                if not autoTools.generateConfigureFiles(target.path, target.name):
                    utilityFunctions.removeDir(tempDir)
                    return None, False
            Logger().writeMessage("Analyzing for dependancies...", target.name)
            possibleDeps = autoTools.getDependancies(target.path, target.name)
        elif make.isMakeProject(target.path):
            target.comment = "Make project found. MixDown cannot determine dependancies from Make projects."
            Logger().writeError(target.comment, target.name)
            partialImport = True
        else:
            target.comment = "Unknown build system found.  MixDown cannot determine dependancies or build commands."
            Logger().writeError(target.comment, target.name)
            partialImport = True

        #Find actual dependancies
        for possibleDependancy in possibleDeps:
            if getTarget(possibleDependancy, finalTargets + targetsToImport):
                Logger().writeMessage("Known dependancy found (" + possibleDependancy + ")", target.name)
                target.dependsOn.append(possibleDependancy)
                continue
            elif options.interactive and possibleDependancy in ignoredTargets:
                Logger().writeMessage("Previously ignored dependancy found (" + possibleDependancy + ")", target.name)
                continue

            if searchForPossibleAliasInList(possibleDependancy, finalTargets + targetsToImport, options.interactive):
                target.dependsOn.append(possibleDependancy)
            elif not options.interactive:
                Logger().writeMessage("Ignoring unknown dependancy (" + possibleDependancy + ")", target.name)
            else:
                Logger().writeMessage("Unknown dependancy found (" + possibleDependancy + ")", target.name)
                userInput = raw_input(possibleDependancy + ": Input location, target name, or blank to ignore:").strip()
                if userInput == "":
                    ignoredTargets.append(possibleDependancy)
                elif os.path.isfile(userInput) or os.path.isdir(userInput) or utilityFunctions.isURL(userInput):
                    name = target.targetPathToName(userInput)
                    newTarget = target.Target(name, userInput)
                    targetsToImport.append(newTarget)
                    if target.normalizeName(possibleDependancy) != target.normalizeName(userInput):
                        newTarget.aliases.append(possibleDependancy)
                    target.dependsOn.append(possibleDependancy)
                else:
                    aliasTarget = getTarget(userInput, finalTargets + targetsToImport, possibleDependancy)
                    if aliasTarget != None:
                        Logger().writeMessage("Alias added (" + userInput + ")", aliasTarget.name)
                        target.dependsOn.append(possibleDependancy)
                    else:
                        aliasLocation = raw_input(userInput + ": Target name not found in any known targets.  Location of new target:").strip()
                        if os.path.isfile(aliasLocation) or os.path.isdir(aliasLocation) or utilityFunctions.isURL(aliasLocation):
                            name = target.targetPathToName(aliasLocation)
                            newTarget = target.Target(name, aliasLocation)
                            notReviewedTargets.append(newTarget)
                            if target.normalizeName(possibleDependancy) != target.normalizeName(aliasLocation):
                                newTarget.aliases.append(possibleDependancy)
                            target.dependsOn.append(possibleDependancy)
                        else:
                            Logger().writeError(userInput + ": Alias location not understood.", exitProgram=True)

        finalTargets.append(target)

    #Create project for targets
    projects = project.Project("ProjectNameNotDetermined", finalTargets)

    if not projects.examine(options):
        Logger().writeError("Project failed examination", exitProgram=True)
    if not projects.validate(options):
        Logger().writeError("Project failed validation", exitProgram=True)

    mainTargetPath = projects.targets[0].origPath
    if utilityFunctions.isURL(mainTargetPath):
        mainTargetPath = utilityFunctions.URLToFilename(mainTargetPath)
    mainTargetName, mainTargetVersion = utilityFunctions.splitFileName(mainTargetPath)
    if mainTargetVersion != "":
        projects.name = mainTargetName + "-" + mainTargetVersion
    else:
        projects.name = mainTargetName
    projects.path = projects.name + ".md"

    for target in projects.targets:
        target.outputPath = ""

    if projects.examine(options):
        Logger().writeMessage("\nFinal targets...\n\n" + str(projects))
        projects.write()

    utilityFunctions.removeDir(tempDir)
    return projects, partialImport

def searchForPossibleAliasInList(possibleAlias, targetList, interactive=False):
    for target in targetList:
        if possibleAlias == target.name or possibleAlias in target.aliases:
            return target
        elif target.name.startswith(possibleAlias):
            if interactive:
                userInput = raw_input("Is " + possibleAlias + " an alias for " + target.name + "? ").lower()
                if userInput == "y" or userInput == "yes":
                    target.aliases.append(possibleAlias)
                    return target
            else:
                Logger().writeMessage("Alias added (" + possibleAlias + ")", target.name)
                target.aliases.append(possibleAlias)
                return target
    return None

def getTarget(name, targetList, aliasToAdd = ""):
    normalizedTargetName = target.normalizeName(name)
    foundTarget = None
    for currTarget in targetList:
        if normalizedTargetName == target.normalizeName(currTarget.name):
            foundTarget = currTarget
            break
        for alias in currTarget.aliases:
            if normalizedTargetName == target.normalizeName(alias):
                foundTarget = currTarget
                break

    if foundTarget != None:
        if aliasToAdd != "" and not aliasToAdd in target.aliases:
            target.aliases.append(aliasToAdd)

    return foundTarget

def targetPathInList(path, targetList):
    for target in targetList:
        if path == target.path:
            return True
    return False
