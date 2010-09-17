from mdOptions import *
from mdProject import *

def configure(target):
    if target.hasStep("config"):
        targetPath = target.getPath()
        if target.getConfigCmd() != "":
            executeCommand(target.getConfigCmd(), "", targetPath, True, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if str.lower(basename) in ['configure']:
                        executeCommand('./' + basename, "", targetPath, True, True)
