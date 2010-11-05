from mdLogger import *
from mdOptions import *
from mdProject import *

def build(target, options):
    if target.hasStep("build"):
        if options.verbose:
            Logger().reportStart(target.name, "build")
        returnCode = None
        targetPath = target.path
        outFd = Logger().getOutFd(target.name, "build")
        if target.buildCmd != "":
            returnCode = executeSubProcess(target.buildCmd.split(" "), target.path, outFd, options.verbose, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ["GNUmakefile", "makefile", "Makefile"]:
                        returnCode = executeSubProcess(["make"], targetPath, outFd, options.verbose, False)
        if returnCode == None:
            Logger().reportSkipped(target.name, "build")
        elif returnCode != 0:
            Logger().reportFailure(target.name, "build", returnCode, True)
        else:
            Logger().reportSuccess(target.name, "build")
