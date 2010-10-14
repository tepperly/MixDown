import mdLoggerConsole, mdLoggerFile, mdLoggerHtml

__loggerInstance = None

def Logger():
    if __loggerInstance == None:
        SetLogger()
    return __loggerInstance

def SetLogger(loggerName = ""):
    global __loggerInstance
    if __loggerInstance == None:
        if loggerName == "html":
            __loggerInstance = mdLoggerHtml.LoggerHtml()
        elif loggerName == "file":
            __loggerInstance = mdLoggerFile.LoggerFile()
        elif loggerName == "console":
            __loggerInstance = mdLoggerConsole.LoggerConsole()
        else:
            __loggerInstance = mdLoggerConsole.LoggerConsole()
            __loggerInstance.writeError(loggerName + " logger not found, falling back on console logger")
    else:
        raise IOError("Error: logger cannot be set after it has already been set")

class LoggerBase:
    def close(self):
        pass
    
    def writeMessage(self, message):
        pass

    def writeMessage(self, message, targetName = "", targetStep = ""):
        pass

    def writeError(self, message, targetName = "", targetStep = "", filePath = "", lineNumber = 0, exit = False):
        pass
    
    def reportStart(self, targetName = "", targetStep = ""):
        pass
    
    def reportSuccess(self, targetName = "", targetStep = ""):
        pass

    def reportFailure(self, targetName = "", targetStep = "", returnCode = 0, exit = False):
        pass

    def getOutFd(self, targetName = "", targetStep = ""):
        return sys.stdout

    def getErrorFd(self, targetName = "", targetStep = ""):
        return sys.stderr

    def testSingleton(self):
        print "singleton = Base"


    