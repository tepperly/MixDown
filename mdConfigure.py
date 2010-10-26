from mdLogger import *
from mdOptions import *
from mdProject import *

def configure(target, options):
    if target.hasStep("config"):
        if options.verbose:
            Logger().reportStart(target.name, "configure")
        returnCode = None
        targetPath = target.path
        outFd = Logger().getOutFd(target.name, "configure")
        if target.configCmd != "":
            returnCode = executeSubProcess(target.configCmd.split(" "), targetPath, outFd, options.verbose, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ['configure']:
                        args = ["./configure"]
                        args.append("--prefix=" + options.prefix)
                        for dependancy in target.dependsOn:
                            args.append("--with-" + dependancy + "=" + options.prefix)
                        returnCode = executeSubProcess(args, targetPath, outFd, options.verbose, True)
        if returnCode == None:
            Logger().reportSkipped(target.name, "configure")
        elif returnCode != 0:
            Logger().reportFailure(target.name, "configure", returnCode, True)
        else:
            Logger().reportSuccess(target.name, "configure")
