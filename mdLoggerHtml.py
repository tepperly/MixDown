import sys

class LoggerHtml:
    def close(self):
        pass
    
    def __FormatErrorMessage(self, message, filePath = "", lineNumber = 0):
        if filePath == "" and lineNumber == 0:
            return "Error: %s\n" % (message)
        elif lineNumber == 0:
            return "Error: %s: %s\n" % (filePath, message)
        else:
            return "Error: %s (line %d): %s\n" % (filePath, lineNumber, message)

    def writeMessage(self, message):
        self.writeMessage(message, "", "")

    def writeMessage(self, message, targetName = "", targetStep = ""):
        sys.stderr.flush()
        sys.stdin.write(message)        

    def writeError(self, message, targetName = "", targetStep = "", filePath = "", lineNumber = 0, exit = False):
        sys.stdin.flush()
        sys.stderr.write(self.__FormatErrorMessage(message, filePath, lineNumber))
        sys.stderr.flush()

    def reportSuccess(self, targetName = "", targetStep = ""):
        pass

    def reportFailure(self, targetName = "", targetStep = "", returnCode = 0, exit = False):
        pass

    def getOutFd(self, targetName = "", targetStep = ""):
        return sys.stdout

    def getErrorFd(self, targetName = "", targetStep = ""):
        return sys.stderr

    def testSingleton(self):
        print "singleton = Html"
    