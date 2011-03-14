#! /usr/bin/env python

import os, re, shutil, sys, tarfile, tempfile, urllib
import mdCommands, mdOptions, mdProject, mdStrings, mdTarget, utilityFunctions

from mdLogger import *

def main():
    SetLogger("console")

    tempDir = utilityFunctions.includeTrailingPathDelimiter(tempfile.mkdtemp(prefix="mixdown-"))
    finalTargets = []
    ignoredTargets = []
    mainTargetFlagged = False

    printProgramHeader()
    interactive, notReviewedTargets = processCommandlineOptions()

    while len(notReviewedTargets) != 0:
        target = notReviewedTargets.pop(0)
        if not mainTargetFlagged:
            target.main = True
            mainTargetFlagged = True

        print target.name + ": Analyzing target"
        if utilityFunctions.isURL(target.path):
            print target.name + ": Downloading target to temporary directory"
            newPath = os.path.join(tempDir, utilityFunctions.URLToFilename(target.path))
            urllib.urlretrieve(target.path, newPath)
            target.path = newPath

        if os.path.isfile(target.path) and tarfile.is_tarfile(target.path):
            print target.name + ": Untaring target to temporary directory"
            newPath = tempDir + utilityFunctions.splitFileName(target.path)[0]
            utilityFunctions.untar(target.path, newPath, True)
        elif os.path.isdir(target.path):
            print target.name + ": Copying target directory to temporary directory"
            newPath = tempDir + os.path.basename(target.path)
            shutil.copytree(target.path, newPath)
        else:
            printUsageAndExit(target.name + ": Cannot understand given target")
        target.path = newPath

        if os.path.exists(target.path + "/configure.ac") and not os.path.exists(target.path + "/configure"):
            print target.name + ": Running 'autoreconf'"
            utilityFunctions.executeSubProcess("autoreconf -i", target.path, exitOnError=True)

        if os.path.exists(target.path + "/configure"):
            print target.name + ": Analyzing 'configure --help' output"
            helpFileName = target.path + "/configure_help.log"
            helpFile = open(helpFileName, "w")
            utilityFunctions.executeSubProcess("./configure --help", target.path, helpFile.fileno(), False, True)
            helpFile.close()

            helpFile = open(helpFileName, "r")
            targetRe = re.compile(r"--with-([a-zA-Z\-_]+)=(?:PREFIX|PATH|DIR)")
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
                            notReviewedTargets.append(mdTarget.Target(possibleDependancy, userInput))
                            target.dependsOn.append(possibleDependancy)
                        else:
                            aliasTarget = targetNameInList(userInput, finalTargets + notReviewedTargets, possibleDependancy)
                            if aliasTarget != None:
                                print aliasTarget.name + ": Alias added (" + userInput + ")"
                                target.dependsOn.append(possibleDependancy)
                            else:
                                aliasLocation = raw_input(userInput + ": Alias not found in any known targets.  Location of new target:").strip()
                                if os.path.isfile(aliasLocation) or os.path.isdir(aliasLocation) or utilityFunctions.isURL(aliasLocation):
                                    notReviewedTargets.append(mdTarget.Target(userInput, aliasLocation))
                                    target.dependsOn.append(userInput)
                                else:
                                    printErrorAndExit(userInput + ": Alias location not understood.")
                    else:
                        print target.name + ": Ignoring unknown dependancy (" + possibleDependancy + ")"
            helpFile.close()
        finalTargets.append(target)

    #Create project for targets
    mainTargetName, mainTargetVersion = utilityFunctions.splitFileName(finalTargets[0].origPath)
    if mainTargetVersion != "":
        outFileName = mainTargetName + "-" + mainTargetVersion + ".md"
    else:
        outFileName = mainTargetName + ".md"
    project = mdProject.Project(outFileName, finalTargets)

    options = mdOptions.Options()
    options.importer = True
    options.setDefine(mdStrings.mdDefinePrefix, "$(" + mdStrings.mdDefinePrefix + ")")

    if project.examine(options):
        print "\nFinal targets...\n"
        print str(project)
        project.write(outFileName)

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
                print target.name + ": Alias added (" + possibleAlias + ")"
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
        elif utilityFunctions.isURL(currArg) or os.path.isfile(currArg) or os.path.isdir(currArg):
            name = utilityFunctions.splitFileName(currArg)[0]
            currTarget = mdTarget.Target(name, currArg)
            targetList.append(currTarget)

    if len(targetList) == 0:
        printUsageAndExit()
    else:
        print "Root Project: " + targetList[0].name

    return interactive, targetList

if __name__ == "__main__":
    main()
