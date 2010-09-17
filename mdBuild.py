from mdOptions import *
from mdProject import *

def build(target):
    if target.hasStep("build"):
        targetPath = target.getPath()
        if target.getBuildCmd() != "":
            executeCommand(target.getBuildCmd(), "", targetPath, True, True)
        else:
            if "make" in target.getBuildSystems():
                makefile = findShallowestFile(target.getPath(), ["GNUmakefile", "makefile", "Makefile"])
                wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
                executeCommand("make", "", wd, True, True)
