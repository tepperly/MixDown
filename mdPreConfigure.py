import os

from mdTarget import *
from mdOptions import *
from mdProject import *
from utilityFunctions import *
from mdLogger import *

def preConfigure(target, options):
    if target.hasStep("preconfig"):
        if options.verbose:
            Logger().writeMessage("Preconfiguring target " + target.name + "...")
        returnCode = None
        targetPath = target.path
        outFd = Logger().getOutFd(target.name, "preConfigure")
        if target.preConfigCmd != "":
            returnCode = executeSubProcess(target.preConfigCmd.split(" "), targetPath, outFd, options.verbose, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if basename in ['buildconf']:
                        returnCode = executeSubProcess(["./" + basename], targetPath, outFd, options.verbose, True)
        if returnCode != None:
            if returnCode != 0:
                Logger().reportFailure(target.name, "preConfigure", returnCode, True)
            else:
                Logger().reportSuccess(target.name, "preConfigure")
