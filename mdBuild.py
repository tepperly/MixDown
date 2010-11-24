import os, utilityFunctions

from mdLogger import *
from mdTarget import *

def getBuildCommand(target):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if str.lower(basename) in ["GNUmakefile", "makefile", "Makefile", "GNUmakefile.in", "makefile.in", "Makefile.in", "GNUmakefile.am", "makefile.am", "Makefile.am"]:
                command = "make"
    return command