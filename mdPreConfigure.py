import os

from mdTarget import *
from mdOptions import *
from mdProject import *
from utilityFunctions import *

def preConfigure(target):
    if target.hasStep("preconfig"):
        targetPath = target.getPath()
        if target.getPreConfigCmd() != "":
            executeCommand(target.getPreConfigCmd(), "", targetPath, True, True)
        else:
            for item in os.listdir(targetPath):
                itemPath = includeTrailingPathDelimiter(targetPath) + item
                if os.path.isfile(itemPath):
                    basename = os.path.basename(item)
                    if basename in ['buildconf']:
                        executeCommand('./' + basename, "", targetPath, True, True)
            
    