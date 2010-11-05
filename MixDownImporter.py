#! /usr/bin/env python

import os, re, shutil, sys, tarfile, tempfile, utilityFunctions

from mdTarget import *

def main():
    tempDir = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    finalTargets = []
    ignoredTargets = []
    
    printProgramHeader()
    interactive, notReviewedTargets = processCommandlineOptions()
    
    while len(notReviewedTargets) != 0:
        target = notReviewedTargets.pop(0)
        tempPath = target.path
    
        print target.name + ": Analyzing target"
        if utilityFunctions.isURL(tempPath):
            print target.name + ": Downloading target to temporary directory"
            newPath = os.path.join(tempDir, URLToFilename(tempPath))
            urllib.urlretrieve(tempPath, newPath)
            tempPath = newPath
            
        if os.path.isfile(tempPath) and tarfile.is_tarfile(tempPath):
            print target.name + ": Untaring target to temporary directory"
            newPath = tempDir + utilityFunctions.splitFileName(tempPath)[0]
            utilityFunctions.untar(tempPath, newPath, True)
        elif os.path.isdir(tempPath):
            print target.name + ": Copying target directory to temporary directory"
            newPath = tempDir + os.path.basename(tempPath)
            shutil.copytree(tempPath, newPath)
        else:
            printUsageAndExit(target.name + ": Cannot understand given target")
        tempPath = newPath

        if os.path.exists(tempPath + "/configure"):
            print target.name + ": Analyzing 'configure --help' output"
            helpFileName = tempPath + "/configure_help.log"
            helpFile = open(helpFileName, "w")
            utilityFunctions.executeSubProcess(["./configure", "--help"], tempPath, helpFile.fileno(), False, True)
            helpFile.close()
            
            helpFile = open(helpFileName, "r")
            targetRe = re.compile(r"--with-([a-zA-Z\-_]+)=(?:PREFIX|PATH)")
            for line in helpFile:
                match = targetRe.search(line)
                if match != None:
                    possibleDependancy = match.group(1)
                    if targetNameInList(possibleDependancy, finalTargets + notReviewedTargets):
                        print target.name + ": Known dependancy found (" + possibleDependancy + ")"
                        target.dependsOn.append(possibleDependancy)
                        continue
                    elif possibleDependancy in ignoredTargets:
                        print target.name + ": Previously ignored dependancy found (" + possibleDependancy + ")"
                        continue
                        
                    aliasTarget = searchForPossibleAliasInList(possibleDependancy, finalTargets + notReviewedTargets, interactive)
                    if aliasTarget != None:
                        target.dependsOn.append(possibleDependancy)
                    elif interactive:
                        print target.name + ": Unknown dependancy found (" + possibleDependancy + ")"
                        userInput = raw_input(possibleDependancy + ": Input location, alias, or blank to ignore:").strip()
                        if userInput == "":
                            ignoredTargets.append(possibleDependancy)
                        elif os.path.isfile(userInput) or os.path.isdir(userInput) or utilityFunctions.isURL(userInput):
                            notReviewedTargets.append(Target(possibleDependancy, userInput))
                            target.dependsOn.append(possibleDependancy)
                        else:
                            aliasTarget = targetNameInList(userInput, finalTargets + notReviewedTargets, possibleDependancy)
                            if aliasTarget != None:
                                print aliasTarget.name + ": Alias added (" + userInput + ")"
                                target.dependsOn.append(possibleDependancy)
                            else:
                                aliasLocation = raw_input(userInput + ": Alias not found in any known targets.  Location of new target:").strip()
                                if os.path.isfile(aliasLocation) or os.path.isdir(aliasLocation) or utilityFunctions.isURL(aliasLocation):
                                    notReviewedTargets.append(Target(userInput, aliasLocation))
                                    target.dependsOn.append(userInput)
                                else:
                                    printErrorAndExit(userInput + ": Alias location not understood.")
                    else:
                        print target.name + ": Ignoring unknown dependancy (" + possibleDependancy + ")"

            helpFile.close()

        finalTargets.append(target)
    
    print "Final targets..."
    for target in finalTargets:
        print str(target)           
        
    utilityFunctions.removeDir(tempDir)

def searchForPossibleAliasInList(possibleAlias, targetList, interactive = False):
    for target in targetList:
        if possibleAlias == target.name or possibleAlias in target.aliases:
            return target
        elif target.name.startswith(possibleAlias):
            if interactive:
                userInput = raw_input("Is " + possibleAlias + " an alias for " + target.name + "? ").lower()
                if userInput == "y" or userInput == "yes":
                    target.aliases.append(possibleAlias)
                    return target
            else:
                print target.name + ": Alias, " + possibleAlias + ", added"
                target.aliases.append(possibleAlias)
                return target
    return None

def targetNameInList(name, targetList, aliasToAdd = ""):
    for target in targetList:
        if name == target.name or name in target.aliases:
            if aliasToAdd != "" and not aliasToAdd in target.aliases:
                target.aliases.append(aliasToAdd)
            return target
    return None

def targetPathInList(path, targetList):
    for target in targetList:
        if path == target.path:
            return True
    return False
        
def printUsageAndExit(errorStr = ""):
    print "MixDownImporter.py <location of root project (required)> <list of dependancy locations separated by spaces (optional)>"
    if errorStr != "":
        print "Error: " + errorStr + "\n"
    sys.exit()

def printProgramHeader():
    print "MixDown Importer\n"
    
def processCommandlineOptions():
    interactive = False
    targetList = []
    if len(sys.argv) < 2:
        printUsageAndExit()
    
    for currArg in sys.argv[1:]:
        if currArg.lower() == "-i":
            interactive = True
        elif utilityFunctions.isURL(currArg) or os.path.isfile(currArg):
            name = utilityFunctions.splitFileName(currArg)[0]
            currTarget = Target(name, currArg)
            targetList.append(currTarget)

    if len(targetList) == 0:
        printUsageAndExit()
    else:
        print "Root Project: " + targetList[0].name
        
    return interactive, targetList
    
if __name__ == "__main__":
    main()