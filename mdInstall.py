from mdLogger import *
from mdOptions import *
from mdProject import *

def install(target, options):
    if target.hasStep("install"):
        if options.verbose:
            Logger().reportStart(target.name, "install")
        returnCode = None
        outFd = Logger().getOutFd(target.name, "install")
        if target.installCmd != "":
            returnCode = executeSubProcess(target.installCmd.split(" "), target.path, outFd, options.verbose, True)
        else:
            if "make" in target.buildSystems:
                makefile = findShallowestFile(target.path, ["GNUmakefile", "makefile", "Makefile"])
                wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
                returnCode = executeSubProcess(["make", "install"], wd, outFd, options.verbose, False)
            elif "automake" in target.buildSystems:
                makefile = findShallowestFile(target.path, ["GNUmakefile", "makefile", "Makefile"])
                if makefile == "":
                    Logger().writeError(message="Automake did not create a Makefile", targetName=target.name, targetStep="install", exit=False)
                    Logger().reportFailure(target.name, "install", 1, True)
                wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
                returnCode = executeSubProcess(["make", "install"], wd, outFd, options.verbose, False)
        if returnCode == None:
            Logger().reportSkipped(target.name, "install")
        elif returnCode != 0:
            Logger().reportFailure(target.name, "install", returnCode, True)
        else:
            Logger().reportSuccess(target.name, "install")
