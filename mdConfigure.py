from mdOptions import *
from mdProject import *

def configure(target, options):
    if target.hasStep("config"):
        if options.getVerbose():
            print "Configuring target " + target.getName() + "..."
        targetPath = target.getPath()
        if target.getConfigCmd() != "":
            executeCommand(target.getConfigCmd(), "", targetPath, options.getVerbose(), True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ['configure']:
                        executeCommand('./' + basename, "", targetPath, options.getVerbose(), True)
