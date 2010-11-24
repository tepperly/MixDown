import os, utilityFunctions

from mdLogger import *
from mdTarget import *

def getConfigureCommand(target, prefix=""):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if str.lower(basename) in ['configure']:
                command = "./configure"
                if prefix != "":
                    command += " --prefix=" + outPrefix
                    for dependancy in target.dependsOn:
                        command += " --with-" + dependancy + "=" + outPrefix
    return command