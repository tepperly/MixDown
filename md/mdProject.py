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

import os, collections, Queue
import md.mdCommands, md.mdOptions, md.mdTarget, md.utilityFunctions

from md.mdLogger import *

class Project(object):
    def __init__(self, projectFilePath, targets=[]):
        self.path = projectFilePath
        if self.path.endswith(".md"):
            self.name = os.path.split(self.path)[1][:-3]
        else:
            self.name = md.utilityFunctions.getBasename(self.path)
        self.targets = targets[:] #Use copy to prevent list instance to be used between project instances
        self.__validated = False
        self.__examined = False

    def addSkipStepFromOptions(self, options):
        if options.skipSteps == '' or options.skipSteps == None:
            return True
        skipSteps = options.skipSteps
        for item in skipSteps.split(";"):
            pair = item.split(":")
            if len(pair) != 2 or pair[0] == "" or pair[1] == "":
                Logger().writeError("Invalid commandline -s pair found: " + item)
                Logger().writeMessage("Proper use: -s[Semi-colon delimited list of Skip Step pairs]")
                Logger().writeMessage("Skip Step Pair: [targetName]:[Steps to skip, comma delimited]")
                return False
            target = self.getTarget(pair[0])
            if target == None:
                Logger().writeError("Target not found in -s commandline option: " + pair[0])
                return False
            target.skipSteps = pair[1].split(",")
        return True

    def validate(self, options):
        if self.__validated:
            return True
        else:
            if self.path == '' or self.name == '':
                return False
            if not self.__validateDependsOnLists():
                return False
            for target in self.targets:
                if not target.validate(options):
                    return False
            self.__validated = True
            return True

    def examine(self, options):
        if self.__examined:
            return True
        else:
            if len(self.targets) < 1:
                Logger().writeError("Project has no targets")
                return False
            self.__assignDepthToTargetList()
            self.targets = self.__sortTargetList(self.targets)
            for target in self.targets:
                if not target.examine(options):
                    return False
            self.__examined = True
            return True

    def __addTarget(self, target, lineCount=0):
        if target.name == "" or target.path == "":
            Logger().writeError("New target started before previous was finished, all targets require atleast 'Name' and 'Path' to be declared", "", "", self.path, lineCount)
            return False

        for currTarget in self.targets:
            if md.mdTarget.normalizeName(target.name) == md.mdTarget.normalizeName(currTarget.name):
                Logger().writeError("Cannot have more than one project target by the same name", currTarget.name, "", self.path, lineCount)
                return False
        self.targets.append(target)
        return True

    def getTarget(self, targetName):
        normalizedTargetName = md.mdTarget.normalizeName(targetName)
        for currTarget in self.targets:
            if normalizedTargetName == md.mdTarget.normalizeName(currTarget.name):
                return currTarget
            for alias in currTarget.aliases:
                if normalizedTargetName == md.mdTarget.normalizeName(alias):
                    return currTarget
        return None

    def read(self):
        f = open(self.path, "r")
        try:
            currTarget = None
            lineCount = 0
            for currLine in f:
                lineCount += 1
                lastPackageLineNumber = 0
                currLine = str.strip(currLine)
                if (currLine == "") or currLine.startswith('#') or currLine.startswith('//'):
                    pass
                else:
                    currPair = currLine.split(":", 1)
                    currPair = currPair[0].strip(), currPair[1].strip()
                    currName = str.lower(currPair[0])

                    if (currName != "name") and (currTarget is None):
                        Logger().writeError("'" + currPair[0] +  "' declared before 'name' in Project file", "", "", self.path, lineCount)
                        return False

                    if currName == "name":
                        lastPackageLineNumber = lineCount
                        if currTarget != None:
                            if not self.__addTarget(currTarget, lastPackageLineNumber):
                                return False
                        currTarget = md.mdTarget.Target(currPair[1])
                    elif currName == "path":
                        if currTarget.path != "":
                            Logger().writeError("Project targets can only have one 'Path' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.path = currPair[1]
                    elif currName == "output":
                        if currTarget.outputPathSpecified:
                            Logger().writeError("Project targets can only have one 'Output' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.outputPath = currPair[1]
                        currTarget.outputPathSpecified = True
                    elif currName == "dependson":
                        if currTarget.dependsOn != []:
                            Logger().writeError("Project targets can only have one 'DependsOn' defined (use a comma delimited list for multiple dependancies)", "", "", self.path, lineCount)
                            return False
                        if currPair[1] != "":
                            dependsOnList = md.utilityFunctions.stripItemsInList(currPair[1].split(","))
                            normalizedName = md.mdTarget.normalizeName(currTarget.name)
                            for dependancy in dependsOnList:
                                if md.mdTarget.normalizeName(dependancy) == normalizedName:
                                    Logger().writeError("Project targets cannot depend on themselves", currTarget.name, "", self.path, lineCount)
                                    return False
                            currTarget.dependsOn = dependsOnList
                    elif currName == "aliases":
                        if currTarget.aliases != []:
                            Logger().writeError("Project targets can only have one 'Aliases' defined (use a comma delimited list for multiple aliases)", "", "", self.path, lineCount)
                            return False
                        if currPair[1] != "":
                            aliases = md.utilityFunctions.stripItemsInList(currPair[1].split(","))
                            noralizedName = md.mdTarget.normalizeName(currTarget.name)
                            for alias in aliases:
                                if md.mdTarget.normalizeName(alias) == normalizedName:
                                    Logger().writeError("Project target alias cannot be same as its name", currTarget.name, "", self.path, lineCount)
                                    return False
                            currTarget.aliases = aliases
                    elif currName == "skipsteps" or currName == "skipstep":
                        if currTarget.skipSteps != []:
                            Logger().writeError("Project targets can only have one 'SkipSteps' defined (use a comma delimited list for multiple steps)", "", "", self.path, lineCount)
                            return False
                        currTarget.skipSteps = md.utilityFunctions.stripItemsInList(str.lower(currPair[1]).split(","))
                    elif currName in md.mdCommands.buildSteps:
                        if currTarget.findBuildStep(currName) != None:
                            Logger().writeError("Project targets can only have one '" + currName + "' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.buildSteps.append(md.mdCommands.BuildStep(currName, currPair[1]))
                    else:
                        Logger().writeError("Cannot understand given line: '" + currLine + "'", "", "", self.path, lineCount)
                        return False

            if not self.__addTarget(currTarget, lastPackageLineNumber):
                return False
        finally:
            f.close()
        return True

    def write(self, fileName=""):
        if fileName != "":
            outFile = open(fileName, "w")
        else:
            outFile = open(self.path, "w")
        outFile.write(str(self) + "\n")
        outFile.close()

    def __str__(self):
        retStr = ""
        for target in self.targets:
            if len(retStr) != 0:
                retStr += "\n"
            retStr += str(target)
        return retStr

    def __validateDependsOnLists(self):
        if len(self.targets) == 0:
            return True

        for currTarget in self.targets:
            normalizedName = md.mdTarget.normalizeName(currTarget.name)
            checkedDependancies = []
            for dependancy in currTarget.dependsOn:
                normalizedDepedancy = md.mdTarget.normalizeName(dependancy)
                if normalizedDepedancy == normalizedName:
                    Logger().writeError("Target cannot depend on itself", currTarget.name, "", self.path)
                    return False
                if normalizedDepedancy in checkedDependancies:
                    Logger().writeError("Target has duplicate dependancy '" + dependancy + "'", currTarget.name, "", self.path)
                    return False
                if self.getTarget(dependancy) is None:
                    Logger().writeError("Target has non-existant dependancy '" + dependancy + "'", currTarget.name, "", self.path)
                    return False
                checkedDependancies.append(normalizedDepedancy)

        path = [md.mdTarget.normalizeName(self.targets[0].name)]
        return self.__searchPathsForCycles(path)

    def __searchPathsForCycles(self, path):
        currTarget = self.getTarget(path[len(path)-1])
        for dependancy in currTarget.dependsOn:
            normalizedDependancy = md.mdTarget.normalizeName(dependancy)
            if normalizedDependancy in path:
                return False
            path.append(normalizedDependancy)
            if not self.__searchPathsForCycles(path):
                return False
            path.pop()
        return True

    def __assignDepthToTargetList(self):
        q = Queue.Queue()
        for target in self.targets:
            q.put(target.name)
            while not q.empty():
                currName = q.get()
                currTarget = self.getTarget(currName)
                for currChildName in currTarget.dependsOn:
                    currChildTarget = self.getTarget(currChildName)
                    if currChildTarget.dependancyDepth < (currTarget.dependancyDepth + 1):
                        currChildTarget.dependancyDepth = currTarget.dependancyDepth + 1
                        q.put(currChildName)

    def __sortTargetList(self, targetList):
        if targetList == []:
            return []
        else:
            pivot = targetList[0]
            greater = self.__sortTargetList([x for x in targetList[1:] if x.dependancyDepth >= pivot.dependancyDepth])
            lesser = self.__sortTargetList([x for x in targetList[1:] if x.dependancyDepth < pivot.dependancyDepth])
            return lesser + [pivot] + greater
