from mdLogger import *
from mdOptions import *
from mdProject import *

def build(target, options):
    if target.hasStep("build"):
        if options.verbose:
            Logger().writeMessage("Building target " + target.name + "...")
        returnCode = None
        outFd = Logger().getOutFd(target.name, "build")
        if target.buildCmd != "":
            returnCode = executeSubProcess(target.buildCmd.split(" "), target.path, outFd, options.verbose, True)
        else:
            if "make" in target.buildSystems:
                makefile = findShallowestFile(target.path, ["GNUmakefile", "makefile", "Makefile"])
                wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
                returnCode = executeSubProcess(["make"], wd, outFd, options.verbose, False)
        if returnCode != None:
            if returnCode != 0:
                Logger().reportFailure(target.name, "build", returnCode, True)
            else:
                Logger().reportSuccess(target.name, "build")
