import os, Queue

from mdLogger import *
from mdTarget import *
from utilityFunctions import *

class Project:
    def __init__(self, projectFilePath):
        self.name = ""
        self.path = projectFilePath
        self.targets = []
        self.__read()
        self.__validateDependsOnLists()
        self.__assignDepthToTargetList()
        self.targets = self.__sortTargetList(self.targets)
        
    def __addTarget(self, target, lineCount = 0):
        for currTarget in self.targets:
            currName = target.name
            if currName == currTarget.name:
                printErrorAndExit("Cannot have more than one project target by the same name, " + currName, self.path, lineCount)
        self.targets.append(target)
        
    def getTarget(self, targetName):
        for currTarget in self.targets:
            if targetName == currTarget.name:
                return currTarget
        return None

    def __read(self):
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
                    currPair = currLine.split("=", 1)
                    currName = str.lower(currPair[0])
                    
                    if (currName != "project") and (currTarget is None):
                            printErrorAndExit("'" + currPair[0] +  "' declared before 'Project' in Project file", self.path, lineCount)
                    
                    if currName == "project":
                        lastPackageLineNumber = lineCount
                        if not currTarget is None:
                            printErrorAndExit("Each project file can only have one 'Project' declared", self.path, lineCount)
                        currTarget = Target(currPair[1])
                        self.name = currPair[1]
                    elif currName == "package":
                        lastPackageLineNumber = lineCount
                        if not currTarget is None:
                            if currTarget.isValid():
                                self.__addTarget(currTarget, lastPackageLineNumber)
                            else:
                                printErrorAndExit("New target started before previous was finished, all targets require ('Package'|'Project') and 'Path' to be declared", self.path, lineCount)
                        currTarget = Target(currPair[1])
                    elif currName == "path":
                        if currTarget.path != "":
                            printErrorAndExit("Project targets can only have one 'Path' defined", self.path, lineCount)
                        currTarget.path = currPair[1]
                    elif currName == "output":
                        if currTarget.output != "":
                            printErrorAndExit("Project targets can only have one 'Output' defined", self.path, lineCount)
                        currTarget.output = includeTrailingPathDelimiter(currPair[1])
                    elif currName == "dependson":
                        if currTarget.dependsOn != []:
                            printErrorAndExit("Project targets can only have one 'DependsOn' defined (use a comma delimited list for multiple dependancies)", self.path, lineCount)
                        if currPair[1] != "":
                            dependsOnList = stripItemsInList(currPair[1].split(","))
                            if currTarget.name in dependsOnList:
                                printErrorAndExit("Project targets cannot depend on themselves", self.path, lineCount)
                            currTarget.dependsOn = dependsOnList
                    elif currName == "steps":
                        if currTarget.steps != []:
                            printErrorAndExit("Project targets can only have one 'Steps' defined (use a comma delimited list for multiple steps)", self.path, lineCount)
                        currTarget.steps = stripItemsInList(str.lower(currPair[1]).split(","))
                    elif currName == "preconfigcmd":
                        if currTarget.preConfigCmd != "":
                            printErrorAndExit("Project targets can only have one 'PreConfigCmd' defined", self.path, lineCount)
                        currTarget.preConfigCmd = currPair[1]
                    elif currName == "configcmd":
                        if currTarget.configCmd != "":
                            printErrorAndExit("Project targets can only have one 'ConfigCmd' defined", self.path, lineCount)
                        currTarget.configCmd = currPair[1]
                    elif currName == "buildcmd":
                        if currTarget.buildCmd != "":
                            printErrorAndExit("Project targets can only have one 'BuildCmd' defined", self.path, lineCount)
                        currTarget.buildCmd = currPair[1]
                    elif currName == "installcmd":
                        if currTarget.installCmd != "":
                            printErrorAndExit("Project targets can only have one 'InstallCmd' defined", self.path, lineCount)
                        currTarget.installCmd = currPair[1]
                            
            if currTarget.isValid():
                self.__addTarget(currTarget, lastPackageLineNumber)
            else:
                printErrorAndExit("Project file ended before project target was finished, all targets require 'Project' and 'Path' to be declared", self.path, lineCount);                        
        finally:
            f.close()
            
    def __validateDependsOnLists(self):
        depQueue = Queue.Queue()
        for currTarget in self.targets:
            currFullDepList = [currTarget.name]
            depQueue.put(currTarget.name)
            
            while not depQueue.empty():
                currDepName = depQueue.get()
                currDepTarget = self.getTarget(currDepName)
                if currDepTarget is None:
                    printErrorAndExit("Project target '%s' has non-existant dependancy '%s'" % (currTarget.name, currDepName))
                    
                for name in currDepTarget.dependsOn:
                    if name in currFullDepList:
                        printErrorAndExit("Cyclical dependancy between project targets '%s' and '%s'" % (currTarget.name, currDepTarget.name))
                    currFullDepList += name
                    depQueue.put(name)
                    
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