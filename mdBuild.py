from mdLogger import *
from mdOptions import *
from mdProject import *

def build(target, options):
    if target.hasStep("build"):
        if options.verbose:
            Logger().writeMessage("Building target " + target.name + "...")
        outFd = Logger().getOutFd(target.name, "build")
        if target.buildCmd != "":
            executeSubProcess(target.buildCmd.split(" "), target.path, outFd, options.verbose, True)
        else:
            if "make" in target.buildSystems:
                makefile = findShallowestFile(target.path, ["GNUmakefile", "makefile", "Makefile"])
                wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
                executeSubProcess(["make"], wd, outFd, options.verbose, True)
