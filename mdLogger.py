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
    

    