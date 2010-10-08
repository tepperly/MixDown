from mdLogger import *
from mdOptions import *
from mdProject import *

def configure(target, options):
    if target.hasStep("config"):
        if options.verbose:
            Logger().writeMessage("Configuring target " + target.name + "...")
        targetPath = target.path
        outFd = Logger().getOutFd(target.name, "configure")
        if target.configCmd != "":
            executeSubProcess(target.configCmd.split(" "), targetPath, outFd, options.verbose, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ['configure']:
                        executeSubProcess(["./configure"], targetPath, outFd, options.verbose, True)
