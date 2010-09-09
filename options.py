import os, MixDown

from MixDown import *

class Options:
    def __init__(self):
        self.projectFile = ""
        self.buildDir = "mdBuild/"
        self.downloadDir = "mdDownload/"
        self.installDir = "mdInstall/"
        self.cleanBefore = False
        self.cleanAfter = False
        self.verbose = False
        
    def __str__(self):
        retStr = "Options:\n"
        retStr += "  Project File: " + self.projectFile + "\n"
        retStr += "  Build Dir:    " + self.buildDir + "\n"
        retStr += "  Download Dir: " + self.downloadDir + "\n"
        retStr += "  Install Dir:  " + self.installDir + "\n"
        retStr += "  Clean Before: " + str(self.cleanBefore) + "\n"
        retStr += "  Clean After:  " + str(self.cleanAfter) + "\n"
        retStr += "  Verbose:      " + str(self.verbose) + "\n"
        return retStr
        
    def getProjectFile(self):
        return self.projectFile 
    def setProjectFile(self, value):
        self.projectFile = value

    def getBuildDir(self):
        return self.buildDir  
    def setBuildDir(self, value):
        self.buildDir = includeTrailingPathDelimiter(value)
        
    def getDownloadDir(self):
        return self.downloadDir
    def setDownloadDir(self, value):
        self.downloadDir = value
        
    def getInstallDir(self):
        return self.installDir
    def setInstallDir(self, value):
        self.installDir = value        
        
    def getCleanBefore(self):
        return self.cleanBefore
    def setCleanBefore(self, value):
        self.cleanBefore = value        
        
    def getCleanAfter(self):
        return self.cleanAfter
    def setCleanAfter(self, value):
        self.cleanAfter = value
        
    def getVerbose(self):
        return self.verbose
    def setVerbose(self, value):
        self.verbose = value

    def processCommandline(self):
        if len(sys.argv) < 2:
            printUsageAndExit()
            
        for currArg in sys.argv[1:]: #skip script name
            currFlag = str.lower(currArg[:2])
            currValue = currArg[2:]
            
            if currFlag == "-b":
                validateOptionPair(currFlag, currValue)
                self.setBuildDir(currValue)
            elif currFlag == "-d":
                validateOptionPair(currFlag, currValue)
                self.setDownloadDir(currValue)
            elif currFlag == "-i":
                validateOptionPair(currFlag, currValue)
                self.setInstallDir(currValue)
            elif currFlag == "-c":
                validateOptionPair(currFlag, currValue)
                lowerCurrValue = str.lower(currValue)
                valueLength = len(currValue)
                if valueLength == 0:
                    printUsageAndExit("Value, 'a' or 'b', expected after -c option")
                elif valueLength > 1:
                    printUsageAndExit("Unexpected value '" + currValue + "' given with -c option")
                    
                if currValue == 'a':
                    self.setCleanAfter(True)
                elif currValue == 'b':
                    self.setCleanBefore(True)
                else:
                    printUsageAndExit("Unexpected value '" + currValue + "' given with -c option")
            elif currFlag == "-v":
                validateOption(currFlag, currValue)
                self.setVerbose(True)
            elif currArg.lower() in ("/help", "/h", "-help", "--help", "-h"):
                printUsageAndExit()
            elif os.path.splitext(currArg)[1] == ".md":
                if not os.path.isfile(currArg):
                    printErrorAndExit("File " + currArg + " does not exist")
                else:
                    self.projectFile = currArg
            else:
                printUsageAndExit("Command line argument '" + currArg + "' not understood")

def validateOptionPair(flag, value):
    if value == "":
        printUsageAndExit(Flag + " option requires a following value")
            
def validateOption(flag, value):
    if value != "":
        printUsageAndExit(Flag + " option does not require a following value")