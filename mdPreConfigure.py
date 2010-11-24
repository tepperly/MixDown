import os, utilityFunctions

from mdLogger import *
from mdTarget import *

def getPreConfigureCommand(target):
    command = ""
    for item in os.listdir(target.path):
        itemPath = utilityFunctions.includeTrailingPathDelimiter(target.path) + item
        if os.path.isfile(itemPath):
            basename = os.path.basename(item)
            if basename in ['buildconf']:
                command = "./buildconf"
    return command