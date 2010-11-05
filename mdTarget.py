import os

from utilityFunctions import *

class Target:
    def __init__(self, targetName, path = ""):
        self.name = targetName
        self.aliases = []
        self.path = path
        self.output = ""
        self.dependancyDepth = 0
        self.sourceTypes = []
        self.buildSystems = []
        self.dependsOn = []
        self.steps = []
        self.preConfigCmd = ""
        self.configCmd = ""
        self.buildCmd = ""
        self.installCmd = ""
        
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
        retStr  = "Target:\n"
        retStr += "  Name: " + self.name + "\n"
        retStr += "  Path: " + self.path + "\n"
        if len(self.aliases) != 0:
            retStr += "  Alias: " + ",".join(self.aliases) + "\n"        
        if self.output != "":
            retStr += "  Output: " + self.output + "\n"
        if len(self.dependsOn) != 0:
            retStr += "  DependsOn: " + ",".join(self.dependsOn) + "\n"        
        if len(self.sourceTypes) != 0:
            retStr += "  Source Types: " + ",".join(self.sourceTypes) + "\n"
        if len(self.buildSystems) != 0:
            retStr += "  Build Systems: " + ",".join(self.buildSystems) + "\n"
        if len(self.steps) != 0:
            retStr += "  Steps: " + ",".join(self.steps) + "\n"
        if self.preConfigCmd != "":
            retStr += "  PreConfig Command: " + self.preConfigCmd + "\n"
        if self.configCmd != "":
            retStr += "  Config Command: " + self.configCmd + "\n"
        if self.buildCmd != "":
            retStr += "  Build Command: " + self.buildCmd + "\n"
        if self.installCmd != "":
            retStr += "  Install Command: " + self.installCmd + "\n"
        return retStr

    @property
    def steps(self, value):
        steps = []
        for step in value[:]:
            steps.append(str.lower(step))
        self.steps = steps
    
    def hasStep(self, stepName):
        if len(self.steps) == 0: #no steps were specified, do all steps
            return True
        for step in self.steps:
            if step.startswith(stepName):
                return True
        return False

    def addBuildSystem(self, buildSystem):
        if not buildSystem in self.buildSystems:
            self.buildSystems.append(buildSystem)

    def addSourceType(self, sourceType):
        if not sourceType in self.sourceTypes:
            self.sourceTypes.append(sourceType)