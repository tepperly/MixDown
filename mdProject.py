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

import os, Queue, mdCommands, mdTarget, utilityFunctions

from mdLogger import *

class Project:
    def __init__(self, projectFilePath, targets=[]):
        self.path = projectFilePath
        self.name = utilityFunctions.getBasename(self.path)
        self.targets = targets[:] #Use copy to prevent list instance to be used between project instances
        self.__validated = False

    def validate(self):
        if self.path == '' or self.name == '':
            return False
        if not self.__validateDependsOnLists():
            return False
        self.__validated = True
        return True

    def examine(self, options):
        if not self.__validated or not self.validate():
            return False
        self.__assignDepthToTargetList()
        self.targets = self.__sortTargetList(self.targets)
        self.name = self.targets[0].name
        for target in reversed(self.targets):
            target.examine(options)
        return True

    def __addTarget(self, target, lineCount=0):
        for currTarget in self.targets:
            currName = target.name
            if currName == currTarget.name:
                Logger().writeError("Cannot have more than one project target by the same name", currName, "", self.path, lineCount, True)
        self.targets.append(target)

    def getTarget(self, targetName):
        for currTarget in self.targets:
            if targetName == currTarget.name or targetName in currTarget.aliases:
                return currTarget
        return None

    def read(self):
        f = open(self.path, "r")
        try:
            currTarget = None
            lineCount = 0
            mainDeclared = False
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
                        if not currTarget is None:
                            if currTarget.isValid():
                                self.__addTarget(currTarget, lastPackageLineNumber)
                            else:
                                Logger().writeError("New target started before previous was finished, all targets require ('Package'|'Project') and 'Path' to be declared", "", "", self.path, lineCount)
                                return False
                        currTarget = mdTarget.Target(currPair[1])
                    elif currName == "main":
                        lastPackageLineNumber = lineCount
                        if mainDeclared:
                            Logger().writeError("Project targets can only have one 'Main' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.main = True
                        mainDeclared = True
                    elif currName == "path":
                        if currTarget.path != "":
                            Logger().writeError("Project targets can only have one 'Path' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.path = currPair[1]
                    elif currName == "output":
                        if currTarget.output != "":
                            Logger().writeError("Project targets can only have one 'Output' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.output = utilityFunctions.includeTrailingPathDelimiter(currPair[1])
                    elif currName == "dependson":
                        if currTarget.dependsOn != []:
                            Logger().writeError("Project targets can only have one 'DependsOn' defined (use a comma delimited list for multiple dependancies)", "", "", self.path, lineCount)
                            return False
                        if currPair[1] != "":
                            dependsOnList = utilityFunctions.stripItemsInList(currPair[1].split(","))
                            if currTarget.name in dependsOnList:
                                Logger().writeError("Project targets cannot depend on themselves", "", "", self.path, lineCount)
                                return False
                            currTarget.dependsOn = dependsOnList
                    elif currName == "aliases":
                        if currTarget.aliases != []:
                            Logger().writeError("Project targets can only have one 'Aliases' defined (use a comma delimited list for multiple aliases)", "", "", self.path, lineCount)
                            return False
                        if currPair[1] != "":
                            aliases = utilityFunctions.stripItemsInList(currPair[1].split(","))
                            if currTarget.name in aliases:
                                Logger().writeError("Project target alias cannot be same as its name", "", "", self.path, lineCount)
                                return False
                            currTarget.aliases = aliases
                    elif currName == "skipsteps" or currName == "skipstep":
                        if currTarget.skipSteps != []:
                            Logger().writeError("Project targets can only have one 'SkipSteps' defined (use a comma delimited list for multiple steps)", "", "", self.path, lineCount)
                            return False
                        currTarget.skipSteps = utilityFunctions.stripItemsInList(str.lower(currPair[1]).split(","))
                    elif currName in mdCommands.getBuildStepList():
                        if currTarget.commands[currName] != "":
                            Logger().writeError("Project targets can only have one '" + currName + "' defined", "", "", self.path, lineCount)
                            return False
                        currTarget.commands[currName] = currPair[1]
                    else:
                        Logger().writeError("Not known project pair name '" + currName + "'", "", "", self.path, lineCount)
                        return False

            if currTarget.isValid():
                self.__addTarget(currTarget, lastPackageLineNumber)
            else:
                Logger().writeError("Project file ended before project target was finished, all targets require 'Project' and 'Path' to be declared", "", "", self.path, lineCount)
                return False
        finally:
            f.close()
        return True

    def write(self, fileName=""):
        if fileName != "":
            outFile = open(fileName, "w")
        else:
            outFile = open(self.path, "w")
        for target in reversed(self.targets):
            outFile.write(str(target) + "\n")
        outFile.close()

    def __str__(self):
        retStr = ""
        for target in reversed(self.targets):
            if len(str) != 0:
                retStr += "\n"
            retStr += str(target)

    def __validateDependsOnLists(self):
        depQueue = Queue.Queue()
        for currTarget in self.targets:
            currFullDepList = [currTarget.name]
            depQueue.put(currTarget.name)

            while not depQueue.empty():
                currDepName = depQueue.get()
                currDepTarget = self.getTarget(currDepName)
                if currDepTarget is None:
                    Logger().writeError("Target has non-existant dependancy '" + currDepName + "'", currTarget.name, "", self.path)
                    return False

                for name in currDepTarget.dependsOn:
                    if name in currFullDepList:
                        Logger().writeError("Target has cyclical dependancy with target '" + currDepName + "'", currTarget.name, "", self.path)
                        return False
                    currFullDepList += name
                    depQueue.put(name)
        return True

    def __assignDepthToTargetList(self):
        q = Queue.Queue()
        q.put(self.name)
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
            lesser = self.__sortTargetList([x for x in targetList[1:] if x.dependancyDepth >= pivot.dependancyDepth])
            greater = self.__sortTargetList([x for x in targetList[1:] if x.dependancyDepth < pivot.dependancyDepth])
            return lesser + [pivot] + greater