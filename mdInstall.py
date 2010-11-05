from mdLogger import *
from mdOptions import *
from mdProject import *

def install(target, options):
    if target.hasStep("install"):
        if options.verbose:
            Logger().reportStart(target.name, "install")
        returnCode = None
        targetPath = target.path
        outFd = Logger().getOutFd(target.name, "install")
        if target.installCmd != "":
            returnCode = executeSubProcess(target.installCmd.split(" "), target.path, outFd, options.verbose, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ["GNUmakefile", "makefile", "Makefile"]:
                        returnCode = executeSubProcess(["make", "install"], targetPath, outFd, options.verbose, False)
        if returnCode == None:
            Logger().reportSkipped(target.name, "install")
        elif returnCode != 0:
            Logger().reportFailure(target.name, "install", returnCode, True)
        else:
            Logger().reportSuccess(target.name, "install")
