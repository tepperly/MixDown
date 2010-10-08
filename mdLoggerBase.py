import sys

class LoggerBase():
    __instance = None
    
    #def __new__(classtype, *args, **kwargs):
        ## Check to see if a __instance exists already for this class
        ## Compare class types instead of just looking for None so
        ## that subclasses will create their own __instance objects
        #if classtype != type(classtype.__instance):
            #classtype.__instance = object.__new__(classtype, *args, **kwargs)
        #return classtype.__instance

    #def __new__(cls, *args, **kwargs):
        #if not cls._instance:
            #cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        #return cls._instance

    def __init__(self):
        if not self.__instance:
            self.__instance = LoggerBase()
        
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

    def getOutFd(self, targetName = "", targetStep = ""):
        return sys.stdout

    def getErrorFd(self, targetName = "", targetStep = ""):
        return sys.stderr
    
    def testSingleton(self):
        print "singleton = Base"
        
