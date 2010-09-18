from mdOptions import *
from mdProject import *

def build(target, options):
    if target.hasStep("build"):
        if options.getVerbose():
            print "Building target " + target.getName() + "..."
        targetPath = target.getPath()
        if target.getBuildCmd() != "":
            executeCommand(target.getBuildCmd(), "", targetPath, options.getVerbose(), True)
        else:
            if "make" in target.getBuildSystems():
                makefile = findShallowestFile(target.getPath(), ["GNUmakefile", "makefile", "Makefile"])
                wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
                executeCommand("make", "", wd, options.getVerbose(), True)
