import sys

from mdLoggerBase import LoggerBase

class LoggerHtml(LoggerBase):
    def close(self):
        pass
    
    def writeMessage(self, message):
        self.writeMessage(message, "", "")

    def writeMessage(self, message, targetName = "", targetStep = ""):
        sys.stderr.flush()
        sys.stdin.write(message)        

    def writeError(self, message, targetName = "", targetStep = "", filePath = "", lineNumber = 0, exit = False):
        sys.stdin.flush()
        sys.stderr.write(self.__FormatErrorMessage(message, filePath, lineNumber))
        sys.stderr.flush()

    def getOutFd(self, targetName = "", targetStep = ""):
        return sys.stdout

    def getErrorFd(self, targetName = "", targetStep = ""):
        return sys.stderr

    def testSingleton(self):
        print "singleton = Html"
    