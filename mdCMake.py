# Copyright (c) 2010, Lawrence Livermore National Security, LLC
# Produced at Lawrence Livermore National Laboratory
# LLNL-CODE-462894
# All rights reserved.
#
# This file is part of MixDown. Please read the COPYRIGHT file
# for Our Notice and the LICENSE file for the GNU Lesser General Public
# License.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License (as published by
# the Free Software Foundation) version 3 dated June 2007.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
#  You should have recieved a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os, re, mdMake, mdStrings, utilityFunctions

def isCMakeProject(path):
    path = utilityFunctions.includeTrailingPathDelimiter(path)
    if os.path.exists(path + "CMakeLists.txt"):
        return True
    return False

def getInstallDir(command):
    prefix = ""
    regex = re.compile(r"cmake.*-DCMAKE_INSTALL_PREFIX=([A-Za-z0-9\/\.]+)")
    match = regex.search(command)
    if match != None:
        prefix = match.group(1)
    return prefix

def _findAllCMakeFiles(path, listToBeFilled):
    for name in dirList:
        fullPath = utilityFunctions.includeTrailingPathDelimiter(path) + name
        if os.path.isdir(fullPath):
            _findAllCMakeFiles(path, listToBeFilled)
        elif name == "CMakeLists.txt":
            listToBeFilled.append(fullPath)
        elif name.endswith(".cmake"):
            listToBeFilled.append(fullPath)

def getDependancies(path, name="", verbose=True):
    deps = []
    if not os.path.isdir(path):
        return None
    if not isCMakeProject(path):
        return None

    if verbose:
        Logger().writeMessage("Analyzing CMake files for dependancies...", name)

    fileList = list()
    _findAllCMakeFiles(path, fileList)

    packageRegExp = re.compile(r"find_package\(\s*([^\)]+\s)\)")
    #TODO: look more into this... python regular expressions only return the last match it found
    libraryRegExp = re.compile(r"find_library\(\s*[\w_]+(?:NAMES)?([^\)]+(?:HINTS|PATHS|PATH_SUFFIXES|DOC|NO_DEFAULT_PATH|NO_CMAKE_ENVIRONMENT_PATH|NO_CMAKE_PATH|NO_SYSTEM_ENVIRONMENT_PATH|NO_CMAKE_SYSTEM_PATH|CMAKE_FIND_ROOT_PATH_BOTH|ONLY_CMAKE_FIND_ROOT_PATH|NO_CMAKE_FIND_ROOT_PATH)*\)")
    for name in fileList:
        try:
            cmakeFile = open(name, "r")
            for line in cmakeFile:
                match = packageRegExp.search(line)
                if match != None:
                    foundDep = mdTarget.normalizeName(match.group(1))
                    if not foundDep in deps:
                        deps.append(foundDep)
                    continue
                #TODO: look at todo above
                match = libraryRegExp.search(line)
                if match != None:
                    for item in match.group:
                        print item
                        
                
        finally:
            cmakeFile.close()

    return deps

# Commands
def getPreconfigureCommand():
    #There is no preconfigure command for CMake
    return ""

def getConfigureCommand():
    return "cmake -DCMAKE_PREFIX_PATH=$(" + mdStrings.mdDefinePrefix + ") -DCMAKE_INSTALL_PREFIX=$(" + mdStrings.mdDefinePrefix + ")"

def getBuildCommand():
    return mdMake.getBuildCommand()

def getInstallCommand():
    return mdMake.getInstallCommand()
