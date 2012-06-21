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

import os, collections, errno, re, Queue
import commands, defines, exceptions, logger, target, utilityFunctions

class Project(object):
    def __init__(self, projectFilePath, targets=[]):
        self.path = projectFilePath
        if self.path.endswith(".md"):
            self.name = os.path.split(self.path)[1][:-3]
        else:
            self.name = utilityFunctions.getBasename(self.path)
        self.targets = targets[:] #Use copy to prevent list instance to be used between project instances
        self.__validated = False
        self.__examined = False
        self.defines = defines.Defines()

    def fixTargetSuccessBasedOnDependancies(self):
        for t in self.targets:
            for depName in t.expandedDependsOn:
                d = self.getTarget(depName)
                if not d.success:
                    t.success = False
                    break

    def writeStatusLog(self, options):
        tempDir = os.path.dirname(options.statusLogPath)
        if not os.path.exists(tempDir):
            os.makedirs(tempDir)

        fd = open(options.statusLogPath, 'w')
        try:
            fd.write("path:" + self.path + "\n")
            fd.write("buildDir:" + options.buildDir + "\n")
            fd.write("prefix" + ":" + os.path.abspath(options.defines[defines.mdPrefix[0]]) + ":" + str(options.prefixDefined) + "\n")
            fd.write("\n")

            for target in self.targets:
                fd.write(target.name + ":" + str(target.success) + "\n")
                for step in target.buildSteps:
                    if step.command == "":
                        fd.write(step.name + "::True\n")
                    else:
                        fd.write(step.name + ":" + step.command + ":" + str(step.success) + "\n")
                fd.write("\n")
            fd.flush()
        finally:
            fd.close()

    def __getStatusLogLine(self, fd, lineCount):
        while True:
            l = fd.readline()
            lineCount += 1
            if l == "":
                return [], lineCount, True
            l = l.strip()
            if l == "":
                continue
            else:
                break
        l = l.split(':')
        return l, lineCount, False

    def __assureEqualsInStatusLog(self, l, name, value):
        #Note just get rid of this function.....
        if l[0].lower() != name.lower():
            logger.writeError("Unknown line in status log:\n" + ':'.join(l), filePath="options.statusLogPath")
            return False
        if l[1] != value:
            return False
        return True

    def readStatusLog(self, options):
        lineCount = 0
        if not os.path.exists(options.statusLogPath) or not os.path.isfile(options.statusLogPath):
            return True

        fd = open(options.statusLogPath, 'r')
        try:
            #path:<self.path>
            l, lineCount, EOF = self.__getStatusLogLine(fd, lineCount)
            if EOF:
                return False
            if len(l) != 2:
                logger.writeError("Unknown line in status log:\n" + ':'.join(l), filePath="options.statusLogPath", lineNumber=lineCount)
                return False
            if not self.__assureEqualsInStatusLog(l, "path", self.path):
                return False
            #buildDir:<options.buildDir>
            l, lineCount, EOF = self.__getStatusLogLine(fd, lineCount)
            if EOF:
                return False
            if len(l) != 2:
                logger.writeError("Unknown line in status log:\n" + ':'.join(l), filePath="options.statusLogPath", lineNumber=lineCount)
                return False
            if not self.__assureEqualsInStatusLog(l, "buildDir", options.buildDir):
                return False
            #prefix:<prefix>:<defined>
            l, lineCount, EOF = self.__getStatusLogLine(fd, lineCount)
            if EOF:
                return False
            if len(l) != 3:
                logger.writeError("Unknown line in status log:\n" + ':'.join(l), filePath="options.statusLogPath", lineNumber=lineCount)
                return False
            if not self.__assureEqualsInStatusLog(l, "prefix", os.path.abspath(options.defines[defines.mdPrefix[0]])):
                return False
            if l[2] != str(options.prefixDefined):
                return False

            #Target groups: one target line followed by multiple step lines
            #<target.name>:<success>
            #<step.name>:<step.command>:<step.success>
            while True:
                l, lineCount, EOF = self.__getStatusLogLine(fd, lineCount)
                if EOF:
                    break
                if len(l) == 2:
                    currTarget = self.getTarget(l[0])
                    if currTarget == None:
                        logger.writeError("Unknown line in status log:\n" + ':'.join(l), filePath="options.statusLogPath", lineNumber=lineCount)
                        continue
                    currTarget.success = utilityFunctions.boolToStr(l[1])
                elif len(l) == 3:
                    if currTarget == None:
                        continue
                    currStep = currTarget.findBuildStep(l[0])
                    if currStep == None:
                        continue
                    currStep.success = utilityFunctions.boolToStr(l[2])
                    if currStep.command != l[1]:
                        currStep.success = False
                else:
                    logger.writeError("Unknown line in status log:\n" + ':'.join(l), filePath="options.statusLogPath", lineNumber=lineCount)
        finally:
            fd.close()

    def addSkipStepFromOptions(self, options):
        if options.skipSteps == '' or options.skipSteps == None:
            return True
        skipSteps = options.skipSteps
        for item in skipSteps.split(","):
            pair = item.split(":")
            if len(pair) != 2 or pair[0] == "" or pair[1] == "":
                logger.writeError("Invalid command-line -s pair found: " + item)
                logger.writeMessage("Proper use: -s[Semi-colon delimited list of Skip Step pairs]")
                logger.writeMessage("Skip Step Pair: [targetName]:[Steps to skip, comma delimited]")
                return False
            targets = self.getTarget(pair[0])
            if targets == None:
                logger.writeError("Target not found in -s command-line option: " + pair[0])
                return False
            targets.skipSteps = pair[1].split(",")
        return True

    def validate(self, options):
        if self.__validated:
            return True
        else:
            if self.path == '' or self.name == '':
                return False
            if not self.__validateDependsOnLists():
                return False
            for targets in self.targets:
                if not targets.validate(options):
                    return False
            self.__validated = True
            return True

    def examine(self, options):
        if self.__examined:
            return True
        else:
            if len(self.targets) < 1:
                logger.writeError("Project has no targets")
                return False
            self.__assignDepthToTargetList()
            self.targets = self.__sortTargetList(self.targets)
            self.__expandDependancyLists()
            for targets in self.targets:
                if not targets.examine(options):
                    return False
            self.__examined = True
            return True

    def __addTarget(self, targets, lineCount=0):
        if targets.name == "" or targets.path == "":
            logger.writeError("New target started before previous was finished, all targets require atleast 'Name' and 'Path' to be declared", "", "", self.path, lineCount)
            return False

        for currTarget in self.targets:
            if target.normalizeName(targets.name) == target.normalizeName(currTarget.name):
                logger.writeError("Cannot have more than one project target by the same name", currTarget.name, "", self.path, lineCount)
                return False
        self.targets.append(targets)
        return True

    def getTarget(self, targetName):
        normalizedTargetName = target.normalizeName(targetName)
        for currTarget in self.targets:
            if normalizedTargetName == target.normalizeName(currTarget.name):
                return currTarget
            for alias in currTarget.aliases:
                if normalizedTargetName == target.normalizeName(alias):
                    return currTarget
        return None

    def replaceTarget(self, newTarget):
        normalizedTargetName = target.normalizeName(newTarget.name)
        i = 0
        targetFound = False
        for currTarget in self.targets:
            if normalizedTargetName == target.normalizeName(currTarget.name):
                targetFound = True
                break
            i += 1
        if targetFound:
            self.targets[i] = newTarget

    def read(self):
        if self.path == "":
            logger.writeError("No project file was specified")
            return False
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
                    colonIndex = currLine.find(":")
                    equalsIndex = currLine.find("=")

                    if (colonIndex == -1) and (equalsIndex == -1):
                        logger.writeError("Line could not be understood by project parser.  Lines can be comments, variables, or project definitions.", "", "", self.path, lineCount)
                        return False

                    if ((colonIndex == -1) and (equalsIndex != -1)) or\
                       ((colonIndex != -1) and (equalsIndex != -1) and (equalsIndex < colonIndex)):
                        currPair = currLine.split("=", 1)
                        currPair = currPair[0].strip(), currPair[1].strip()
                        currName = str.lower(currPair[0])
                        self.defines[currPair[0]] = currPair[1]
                    else:
                        currPair = currLine.split(":", 1)
                        currPair = currPair[0].strip(), currPair[1].strip()
                        currName = str.lower(currPair[0])

                        if (currName != "name") and (currTarget is None):
                            logger.writeError("'" + currPair[0] +  "' declared before 'name' in Project file", "", "", self.path, lineCount)
                            return False

                        if currName == "name":
                            lastPackageLineNumber = lineCount
                            if currTarget != None:
                                if not self.__addTarget(currTarget, lastPackageLineNumber):
                                    return False
                            currTarget = target.Target(currPair[1])
                        elif currName == "path":
                            if currTarget.path != "":
                                logger.writeError("Project targets can only have one 'Path' defined", "", "", self.path, lineCount)
                                return False
                            currTarget.path = currPair[1]
                        elif currName == "output":
                            if currTarget.outputPathSpecified:
                                logger.writeError("Project targets can only have one 'Output' defined", "", "", self.path, lineCount)
                                return False
                            currTarget.outputPath = currPair[1]
                            currTarget.outputPathSpecified = True
                        elif currName == "dependson":
                            if currTarget.dependsOn != []:
                                logger.writeError("Project targets can only have one 'DependsOn' defined (use a comma delimited list for multiple dependencies)", "", "", self.path, lineCount)
                                return False
                            if currPair[1] != "":
                                dependsOnList = utilityFunctions.stripItemsInList(currPair[1].split(","))
                                normalizedName = target.normalizeName(currTarget.name)
                                for dependency in dependsOnList:
                                    if not re.match(r'[\w\.+_\-]+$', dependency):
                                        logger.writeError("Dependancy name, '" + dependency + "', found with invalid character. Only alphanumeric is allowed.", currTarget.name, "", self.path, lineCount)
                                        return False
                                    if target.normalizeName(dependency) == normalizedName:
                                        logger.writeError("Project targets cannot depend on themselves", currTarget.name, "", self.path, lineCount)
                                        return False
                                currTarget.dependsOn = dependsOnList
                        elif currName == "aliases":
                            if currTarget.aliases != []:
                                logger.writeError("Project targets can only have one 'Aliases' defined (use a comma delimited list for multiple aliases)", "", "", self.path, lineCount)
                                return False
                            if currPair[1] != "":
                                aliases = utilityFunctions.stripItemsInList(currPair[1].split(","))
                                noralizedName = target.normalizeName(currTarget.name)
                                for alias in aliases:
                                    if target.normalizeName(alias) == normalizedName:
                                        logger.writeError("Project target alias cannot be same as its name", currTarget.name, "", self.path, lineCount)
                                        return False
                                currTarget.aliases = aliases
                        elif currName == "skipsteps" or currName == "skipstep":
                            if currTarget.skipSteps != []:
                                logger.writeError("Project targets can only have one 'SkipSteps' defined (use a comma delimited list for multiple steps)", "", "", self.path, lineCount)
                                return False
                            currTarget.skipSteps = utilityFunctions.stripItemsInList(str.lower(currPair[1]).split(","))
                        elif currName in commands.buildSteps:
                            if currTarget.findBuildStep(currName) != None:
                                logger.writeError("Project targets can only have one '" + currName + "' defined", "", "", self.path, lineCount)
                                return False
                            currTarget.buildSteps.append(commands.BuildStep(currName, currPair[1]))
                        else:
                            logger.writeError("Cannot understand given line: '" + currLine + "'", "", "", self.path, lineCount)
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
        for targets in self.targets:
            if len(retStr) != 0:
                retStr += "\n"
            retStr += str(targets)
        return retStr

    def __validateDependsOnLists(self):
        if len(self.targets) == 0:
            return True

        for currTarget in self.targets:
            normalizedName = target.normalizeName(currTarget.name)
            checkedDependencies = []
            for dependency in currTarget.dependsOn:
                normalizedDepedancy = target.normalizeName(dependency)
                if normalizedDepedancy == normalizedName:
                    logger.writeError("Target cannot depend on itself", currTarget.name, "", self.path)
                    return False
                if normalizedDepedancy in checkedDependencies:
                    logger.writeError("Target has duplicate dependency '" + dependency + "'", currTarget.name, "", self.path)
                    return False
                if self.getTarget(dependency) is None:
                    logger.writeError("Target has non-existant dependency '" + dependency + "'", currTarget.name, "", self.path)
                    return False
                checkedDependencies.append(normalizedDepedancy)

        path = [target.normalizeName(self.targets[0].name)]
        return self.__searchPathsForCycles(path)

    def __searchPathsForCycles(self, path):
        currTarget = self.getTarget(path[len(path)-1])
        for dependency in currTarget.dependsOn:
            normalizedDependency = target.normalizeName(dependency)
            if normalizedDependency in path:
                return False
            path.append(normalizedDependency)
            if not self.__searchPathsForCycles(path):
                return False
            path.pop()
        return True

    def __assignDepthToTargetList(self):
        q = Queue.Queue()
        for targets in self.targets:
            q.put(targets.name)
            while not q.empty():
                currName = q.get()
                currTarget = self.getTarget(currName)
                for currChildName in currTarget.dependsOn:
                    currChildTarget = self.getTarget(currChildName)
                    if currChildTarget.dependencyDepth < (currTarget.dependencyDepth + 1):
                        currChildTarget.dependencyDepth = currTarget.dependencyDepth + 1
                        q.put(currChildName)

    def __sortTargetList(self, targetList):
        if targetList == []:
            return []
        else:
            pivot = targetList[0]
            greater = self.__sortTargetList([x for x in targetList[1:] if x.dependencyDepth >= pivot.dependencyDepth])
            lesser = self.__sortTargetList([x for x in targetList[1:] if x.dependencyDepth < pivot.dependencyDepth])
            return lesser + [pivot] + greater

    def __expandDependancyLists(self):
        for t in reversed(self.targets):
            for depName in t.dependsOn[:]:
                dep = self.getTarget(depName)
                t.expandedDependsOn.append(depName)
                t.expandedDependsOn += dep.dependsOn
            t.expandedDependsOn = utilityFunctions.removeDuplicatesFromList(t.expandedDependsOn)
