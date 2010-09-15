import os

from utilityFunctions import *

class Target:
    def __init__(self, targetName):
        self.name = targetName
        self.path = ""
        self.output = ""
        self.sourceTypes = []
        self.buildSystems = []
        self.dependsOn = []
        self.steps = []
        
    def isValid(self):
        if self.name == "":
            return False
        if self.path == "":
            return False
        return True
        
    def examine(self):
        self.__examine(self.path)
        
    def __examine(self, path):
        for item in os.listdir(path):
            #TODO: follow directories
            itemPath = includeTrailingPathDelimiter(path) + item
            if os.path.isdir(itemPath):
                self.__examine(itemPath)
            elif os.path.isfile(itemPath):
                #Look for build systems
                currBaseName = os.path.basename(item)
                if currBaseName in ["GNUmakefile", "makefile", "Makefile"]:
                    self.addBuildSystem("make")
                elif currBaseName == "build.xml":
                    self.addBuildSystem("ant")
                elif currBaseName == "configure.ac":
                    self.addBuildSystem("autoconf")
                elif currBaseName == "Makefile.am":
                    self.addBuildSystem("automake")
                elif currBaseName == "CMakeLists.txt":
                    self.addBuildSystem("cmake")
                else:
                    #Look for source types
                    currFileExt = str.lower(os.path.splitext(item)[1])
                    if not currFileExt == "":
                        if currFileExt in [".c", ".h"]:
                            self.addSourceType("C")
                        elif currFileExt in [".cpp", ".hpp"]:
                            self.addSourceType("C++")
                        elif currFileExt in [".java"]:
                            self.addSourceType("Java")
                        elif currFileExt in [".py"]:
                            self.addSourceType("Python")
                        elif currFileExt in [".f", ".for"]:
                            self.addSourceType("Fortran")
                        elif currFileExt in [".f77"]:
                            self.addSourceType("Fortran 77")
                        elif currFileExt in [".f90"]:
                            self.addSourceType("Fortran 90")            
                        elif currFileExt in [".lisp"]:
                            self.addSourceType("Lisp")        
                        elif currFileExt in [".pas"]:
                            self.addSourceType("Pascal")
    def __str__(self):
        retStr = "Target: " + self.path + "\n"
        retStr += prettyPrintList(self.sourceTypes, "Source Types: ", "  ", "    ") + "\n"
        retStr += prettyPrintList(self.buildSystems, "Build Systems: ", "  ", "    ") + "\n"
        return retStr
    
    def getName(self):
        return self.name
    def setName(self, value):
        self.name = value

    def getPath(self):
        return self.path
    def setPath(self, value):
        self.path = value
    
    def getOutput(self):
        return self.output
    def setOutput(self, value):
        self.output = value
    
    def getDependsOn(self):
        return self.dependsOn
    def setDependsOn(self, value):
        self.dependsOn = value

    def getSteps(self):
        return self.steps
    def setSteps(self, value):
        self.steps = value

    def getBuildSystems(self):
        return self.buildSystems
    
    def addBuildSystem(self, buildSystem):
        if not buildSystem in self.buildSystems:
            self.buildSystems.append(buildSystem)

    def getSourceTypes(self):
        return self.sourceTypes
    
    def addSourceType(self, sourceType):
        if not sourceType in self.sourceTypes:
            self.sourceTypes.append(sourceType)
