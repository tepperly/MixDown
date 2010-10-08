import os, MixDown

from MixDown import *

class Options:
    def __init__(self):
        self.projectFile = ""
        self.buildDir = "mdBuild/"
        self.downloadDir = "mdDownload/"
        self.installDir = "mdInstall/"
        self.logDir = "mdLogFiles/"
        self.cleanBefore = False
        self.cleanAfter = False
        self.verbose = False
        self.logger = ""

    def __str__(self):
        retStr = "Options:\n"
        retStr += "  Project File: " + self.projectFile + "\n"
        retStr += "  Build Dir:    " + self.buildDir + "\n"
        retStr += "  Download Dir: " + self.downloadDir + "\n"
        retStr += "  Install Dir:  " + self.installDir + "\n"
        retStr += "  Clean Before: " + str(self.cleanBefore) + "\n"
        retStr += "  Clean After:  " + str(self.cleanAfter) + "\n"
        retStr += "  Verbose:      " + str(self.verbose) + "\n"
        retStr += "  Logger:       " + self.logger.capitalize() + "\n"
        return retStr
        
    @property
    def buildDir(self, value):
        self.buildDir = includeTrailingPathDelimiter(value)

    @property
    def downloadDir(self, value):
        self.downloadDir = includeTrailingPathDelimiter(value)

    @property
    def installDir(self, value):
        self.installDir = includeTrailingPathDelimiter(value)
        
    def processCommandline(self):
        if len(sys.argv) < 2:
            printUsageAndExit()
            
        for currArg in sys.argv[1:]: #skip script name
            currFlag = str.lower(currArg[:2])
            currValue = currArg[2:]
            
            if currFlag == "-l":
                validateOptionPair(currFlag, currValue)
                self.logger = str.lower(currValue)
            elif currFlag == "-b":
                validateOptionPair(currFlag, currValue)
                self.buildDir = currValue
            elif currFlag == "-d":
                validateOptionPair(currFlag, currValue)
                self.downloadDir = currValue
            elif currFlag == "-i":
                validateOptionPair(currFlag, currValue)
                self.installDir = currValue
            elif currFlag == "-c":
                validateOptionPair(currFlag, currValue)
                lowerCurrValue = str.lower(currValue)
                valueLength = len(currValue)
                if valueLength == 0:
                    printUsageAndExit("Value, 'a' or 'b', expected after -c option")
                elif valueLength > 1:
                    printUsageAndExit("Unexpected value '" + currValue + "' given with -c option")
                    
                if currValue == 'a':
                    self.cleanAfter = True
                elif currValue == 'b':
                    self.cleanBefore = True
                else:
                    printUsageAndExit("Unexpected value '" + currValue + "' given with -c option")
            elif currFlag == "-v":
                validateOption(currFlag, currValue)
                self.verbose = True
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