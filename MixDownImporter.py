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

    options, notReviewedTargets = processCommandlineOptions(tempDir)

    while len(notReviewedTargets) != 0:
        target = notReviewedTargets.pop(0)
        if not mainTargetFlagged:
            target.main = True
            mainTargetFlagged = True

        Logger().writeMessage("Analyzing target", target.name)
        Logger().writeMessage("Extracting target", target.name)
       
        target.output = tempDir + target.name
        target.extract(options)

        if os.path.exists(target.path + "/configure.ac") and not os.path.exists(target.path + "/configure"):
            Logger().writeMessage("Running 'autoreconf'", target.name)
            utilityFunctions.executeSubProcess("autoreconf -i", target.path, exitOnError=True)

        if os.path.exists(target.path + "/configure"):
            Logger().writeMessage("Analyzing 'configure --help' output", target.name)
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
                        Logger().writeMessage("Known dependancy found (" + possibleDependancy + ")", target.name)
                        target.dependsOn.append(possibleDependancy)
                        continue
                    elif possibleDependancy in ignoredTargets:
                        Logger().writeMessage("Previously ignored dependancy found (" + possibleDependancy + ")", target.name)
                        continue

                    aliasTarget = searchForPossibleAliasInList(possibleDependancy, finalTargets + notReviewedTargets, options.interactive)
                    if aliasTarget != None:
                        target.dependsOn.append(possibleDependancy)
                    elif options.interactive:
                        Logger().writeMessage("Unknown dependancy found (" + possibleDependancy + ")", target.name)
                        userInput = raw_input(possibleDependancy + ": Input location, target name, or blank to ignore:").strip()
                        if userInput == "":
                            ignoredTargets.append(possibleDependancy)
                        elif os.path.isfile(userInput) or os.path.isdir(userInput) or utilityFunctions.isURL(userInput):
                            name = mdTarget.targetPathToName(userInput)
                            newTarget = mdTarget.Target(name, userInput)
                            notReviewedTargets.append(newTarget)
                            if mdTarget.normalizeName(possibleDependancy) != mdTarget.normalizeName(userInput):
                                newTarget.aliases.append(possibleDependancy)
                            target.dependsOn.append(possibleDependancy)
                        else:
                            aliasTarget = targetNameInList(userInput, finalTargets + notReviewedTargets, possibleDependancy)
                            if aliasTarget != None:
                                Logger().writeMessage("Alias added (" + userInput + ")", aliasTarget.name)
                                target.dependsOn.append(possibleDependancy)
                            else:
                                aliasLocation = raw_input(userInput + ": Target name not found in any known targets.  Location of new target:").strip()
                                if os.path.isfile(aliasLocation) or os.path.isdir(aliasLocation) or utilityFunctions.isURL(aliasLocation):
                                    name = mdTarget.targetPathToName(aliasLocation)
                                    newTarget = mdTarget.Target(name, aliasLocation)
                                    notReviewedTargets.append(newTarget)
                                    if mdTarget.normalizeName(possibleDependancy) != mdTarget.normalizeName(aliasLocation):
                                        newTarget.aliases.append(possibleDependancy)
                                    target.dependsOn.append(possibleDependancy)
                                else:
                                    printErrorAndExit(userInput + ": Alias location not understood.")
                    else:
                        Logger().writeMessage("Ignoring unknown dependancy (" + possibleDependancy + ")", target.name)
            helpFile.close()
        finalTargets.append(target)

    #Create project for targets
    mainTargetName, mainTargetVersion = utilityFunctions.splitFileName(finalTargets[0].origPath)
    if mainTargetVersion != "":
        outFileName = mainTargetName + "-" + mainTargetVersion + ".md"
    else:
        outFileName = mainTargetName + ".md"
    project = mdProject.Project(outFileName, finalTargets)
    
    for target in project.targets:
        target.output = ""

    if project.examine(options):
        Logger().writeMessage("\nFinal targets...\n" + str(project))
        project.write(outFileName)

    utilityFunctions.removeDir(tempDir)

def searchForPossibleAliasInList(possibleAlias, targetList, interactive=False):
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
                Logger().writeMessage("Alias added (" + possibleAlias + ")", target.name)
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

def processCommandlineOptions(tempDir):
    if len(sys.argv) < 2:
        printUsageAndExit()

    targetList = []
    options = mdOptions.Options()
    options.verbose = True
    options.importer = True
    options.downloadDir = utilityFunctions.includeTrailingPathDelimiter(tempDir + "mdDownloads")
    options.setDefine(mdStrings.mdDefinePrefix, "$(" + mdStrings.mdDefinePrefix + ")")
    for currArg in sys.argv[1:]:
        if currArg.lower() == "-i":
            options.interactive = True
        if currArg.lower() == "-q":
            options.verbose = False
        elif utilityFunctions.isURL(currArg) or os.path.isfile(currArg) or os.path.isdir(currArg):
            name = mdTarget.targetPathToName(currArg)
            currTarget = mdTarget.Target(name, currArg)
            targetList.append(currTarget)
        else:
            Logger().writeError("Could not understand given commandline option: " + currArg, exitProgram=True)

    if len(targetList) == 0:
        printUsageAndExit()
    else:
        Logger().writeMessage("Root Project: " + targetList[0].name)

    return options, targetList

if __name__ == "__main__":
    main()
