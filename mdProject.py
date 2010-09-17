import os, Queue

from mdTarget import *
from utilityFunctions import *

class Project:
    def __init__(self, projectFilePath):
        self.name = ""
        self.path = projectFilePath
        self.targets = []
        self.buildOrder = []
        self.__read()
        
    def __addTarget(self, target, lineCount = 0):
        for currTarget in self.targets:
            currName = target.getName()
            if currName == currTarget.getName():
                printErrorAndExit("Cannot have more than one project target by the same name, " + currName, self.path, lineCount)
        self.targets.append(target)
        
    def getTarget(self, targetName):
        for currTarget in self.targets:
            if targetName == currTarget.getName():
                return currTarget
        return None
    
    def getTargets(self):
        return self.targets
        
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
                        if currTarget.getPath() != "":
                            printErrorAndExit("Project targets can only have one 'Path' defined", self.path, lineCount)
                        currTarget.setPath(currPair[1])
                    elif currName == "output":
                        if currTarget.getOutput() != "":
                            printErrorAndExit("Project targets can only have one 'Output' defined", self.path, lineCount)
                        currTarget.setOutput(currPair[1])
                    elif currName == "dependson":
                        if currTarget.getDependsOn() != []:
                            printErrorAndExit("Project targets can only have one 'DependsOn' defined (use a comma delimited list for multiple dependancies)", self.path, lineCount)
                        if currPair[1] != "":
                            dependsOnList = stripItemsInList(currPair[1].split(","))
                            if currTarget.getName() in dependsOnList:
                                printErrorAndExit("Project targets cannot depend on themselves", self.path, lineCount)
                            currTarget.setDependsOn(dependsOnList)
                    elif currName == "steps":
                        if currTarget.getSteps() != []:
                            printErrorAndExit("Project targets can only have one 'Steps' defined (use a comma delimited list for multiple steps)", self.path, lineCount)
                        currTarget.setSteps(stripItemsInList(str.lower(currPair[1]).split(",")))
                    elif currName == "preconfigcmd":
                        if currTarget.getPreConfigCmd() != "":
                            printErrorAndExit("Project targets can only have one 'PreConfigCmd' defined", self.path, lineCount)
                        currTarget.setPreConfigCmd(currPair[1])
                    elif currName == "configcmd":
                        if currTarget.getConfigCmd() != "":
                            printErrorAndExit("Project targets can only have one 'ConfigCmd' defined", self.path, lineCount)
                        currTarget.setConfigCmd(currPair[1])
                    elif currName == "buildcmd":
                        if currTarget.getBuildCmd() != "":
                            printErrorAndExit("Project targets can only have one 'BuildCmd' defined", self.path, lineCount)
                        currTarget.setBuildCmd(currPair[1])
                    elif currName == "installcmd":
                        if currTarget.getInstallCmd() != "":
                            printErrorAndExit("Project targets can only have one 'InstallCmd' defined", self.path, lineCount)
                        currTarget.setInstallCmd(currPair[1])
                            
            if currTarget.isValid():
                self.__addTarget(currTarget, lastPackageLineNumber)
            else:
                printErrorAndExit("Project file ended before project target was finished, all targets require 'Project' and 'Path' to be declared", self.path, lineCount);                        
        finally:
            f.close()
        self.__validateDependsOnLists()
            
    def __validateDependsOnLists(self):
        depQueue = Queue.Queue()
        for currTarget in self.targets:
            currFullDepList = [currTarget.getName()]
            depQueue.put(currTarget.getName())
            
            while not depQueue.empty():
                currDepName = depQueue.get()
                currDepTarget = self.getTarget(currDepName)
                if currDepTarget is None:
                    printErrorAndExit("Project target '%s' has non-existant dependancy '%s'" % (currDepTarget.getName(), currDepName))
                    
                for name in currDepTarget.getDependsOn():
                    if name in currFullDepList:
                        printErrorAndExit("Cyclical dependancy between project targets '%s' and '%s'" % (currTarget.getName(), currDepTarget.getName()))                        
                    currFullDepList += name
                    depQueue.put(name)
                    
    def getBuildOrder(self):
        if self.buildOrder == []:
            depQueue = Queue.Queue()
            depQueue.put(self.name)
            while not depQueue.empty():
                currName = depQueue.get()
                if not currName in self.buildOrder:
                    currTarget = self.getTarget(currName)
                    for currDepName in currTarget.getDependsOn():
                        depQueue.put(currDepName)
                    self.buildOrder.append(currName)
            self.buildOrder.reverse()
        return self.buildOrder
                    
                    
                
                