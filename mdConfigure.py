from mdLoggerBase import *
from mdOptions import *
from mdProject import *

def configure(target, options, logger):
    if target.hasStep("config"):
        if options.verbose:
            logger.writeMessage("Configuring target " + target.getName() + "...")
        targetPath = target.path
        outFd = logger.getOutFd(target.name, "configure")
        if target.configCmd != "":
            executeSubProcess(target.configCmd.split(" "), targetPath, outFd, options.verbose, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ['configure']:
                        executeSubProcess(["./configure"], targetPath, outFd, options.verbose, True)
