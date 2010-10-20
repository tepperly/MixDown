__loggerInstance = None

def Logger():
    if __loggerInstance == None:
        SetLogger()
    return __loggerInstance

def SetLogger(loggerName = "", logOutputDir = ""):
    global __loggerInstance
    if __loggerInstance == None:
        if loggerName == "html":
            import mdLoggerHtml
            __loggerInstance = mdLoggerHtml.LoggerHtml(logOutputDir)
        elif loggerName == "file":
            import mdLoggerFile
            __loggerInstance = mdLoggerFile.LoggerFile(logOutputDir)
        elif loggerName == "console":
            import mdLoggerConsole
            __loggerInstance = mdLoggerConsole.LoggerConsole()
        else:
            import mdLoggerConsole
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
    
    def reportSkipped(self, targetName = "", targetStep = ""):
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


    