from mdOptions import *
from mdProject import *

def build(project, options):
    for currName in project.getBuildOrder():
        currTarget = project.getTarget(currName)
        if "make" in currTarget.getBuildSystems():
            makefile = findShallowestFile(currTarget.getPath(), ["GNUmakefile", "makefile", "Makefile"])
            wd = includeTrailingPathDelimiter(os.path.dirname(makefile))
            status = executeCommand("make", "", wd, True)
            if status != 0:
                printErrorAndExit("Command 'make': exited with error code " + str(status))
