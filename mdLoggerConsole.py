import sys

class LoggerConsole:
    def close(self):
        pass
    
    def __FormatErrorMessage(self, message, filePath = "", lineNumber = 0):
        if filePath == "" and lineNumber == 0:
            return "Error: %s\n" % (message)
        elif lineNumber == 0:
            return "Error: %s: %s\n" % (filePath, message)
        else:
            return "Error: %s (line %d): %s\n" % (filePath, lineNumber, message)

    def writeMessage(self, message, targetName = "", targetStep = ""):
        sys.stderr.flush()
        sys.stdout.write(message + "\n")

    def writeError(self, message, targetName = "", targetStep = "", filePath = "", lineNumber = 0, exit = False):
        sys.stdout.flush()
        sys.stderr.write(self.__FormatErrorMessage(message, filePath, lineNumber))
        sys.stderr.flush()
        if exit:
            sys.exit()

    def reportSkipped(self, targetName = "", targetStep = ""):
        sys.stderr.flush()
        sys.stdout.write(targetName + ": " + str.capitalize(targetStep) + ": Skipped...\n")
    
    def reportStart(self, targetName = "", targetStep = ""):
        sys.stderr.flush()
        sys.stdout.write(targetName + ": " + str.capitalize(targetStep) + ": Starting...\n")

    def reportSuccess(self, targetName = "", targetStep = ""):
        sys.stderr.flush()
        sys.stdout.write(targetName + ": " + str.capitalize(targetStep) + ": Succeeded\n")

    def reportFailure(self, targetName = "", targetStep = "", returnCode = 0, exit = False):
        sys.stdout.flush()
        sys.stderr.write("Error: " + targetName + ": " + str.capitalize(targetStep) + ": Failed with error code " + returnCode + ".\n")
        sys.stderr.flush()
        if exit:
            sys.exit()

    def getOutFd(self, targetName = "", targetStep = ""):
        return sys.stdout

    def getErrorFd(self, targetName = "", targetStep = ""):
        return sys.stderr
    
    def testSingleton(self):
        print "singleton = Console"
