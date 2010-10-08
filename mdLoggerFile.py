import os, sys

from mdLoggerBase import LoggerBase

class LoggerFile(LoggerBase):
    def __init__(self):
        self.errorFds = dict()
        self.outFds = dict()
        
    def close(self):
        for fd in self.errorFds:
            fd.close()
        for fd in self.outFds:
            fd.close()

    def __LookupOutFd(self, targetName, targetStep):
        key = str.lower(targetName + targetStep)
        value = self.outFds.get(key)
        if value == None and targetName != "":
            value = os.open("mdLogFiles/" + targetName + "_" + targetStep + ".log", os.O_CREAT|os.O_WRONLY|os.O_TRUNC)
            self.outFds[key] = value
        return value

    def __LookupErrorFd(self, targetName, targetStep):
        key = str.lower(targetName + targetStep)
        value = self.errorFds.get(key)
        if value == None and targetName != "":
            value = os.open("mdLogFiles/" + targetName + "_" + targetStep + ".log", os.O_CREAT|os.O_WRONLY|os.O_TRUNC)
            self.errFds[key] = value
        return value

    def writeMessage(self, message, targetName = "", targetStep = ""):
        sys.stderr.flush()
        self.getOutFd(targetName, targetStep).write(message + "\n")

    def writeError(self, message, targetName = "", targetStep = "", filePath = "", lineNumber = 0, exit = False):
        sys.stdin.flush()
        self.getErrorFd(targetName, targetStep).write(self.__FormatErrorMessage(message, filePath, lineNumber))
        sys.stderr.flush()

    def getOutFd(self, targetName = "", targetStep = ""):
        if targetName != "" and targetStep != "":
            return self.__LookupOutFd(targetName, targetStep)
        return sys.stdout

    def getErrorFd(self, targetName = "", targetStep = ""):
        if targetName != "" and targetStep != "":
            return self.__LookupErrorFd(targetName, targetStep)
        return sys.stderr

    def testSingleton(self):
        print "singleton = File"
    
