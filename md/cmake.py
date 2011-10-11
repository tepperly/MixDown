# Copyright (c) 2010-2011, Lawrence Livermore National Security, LLC
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

import os, re
import defines, exceptions, logger, make, target, utilityFunctions


def isCMakeProject(path):
    if os.path.exists(os.path.join(path, "CMakeLists.txt")):
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
    dirList = os.listdir(path)
    for name in dirList:
        fullPath = os.path.join(path, name)
        if os.path.isdir(fullPath):
            _findAllCMakeFiles(fullPath, listToBeFilled)
        elif name == "CMakeLists.txt":
            listToBeFilled.append(fullPath)
        elif name.endswith(".cmake"):
            listToBeFilled.append(fullPath)

def getDependencies(path, name="", verbose=True):
    deps = []
    if not os.path.isdir(path):
        return None
    if not isCMakeProject(path):
        return None

    if verbose:
        logger.writeMessage("Analyzing CMake files for dependencies...", name)

    fileList = list()
    _findAllCMakeFiles(path, fileList)

    packageRegExp = re.compile(r"find_package\s*\((\s*[\w\.]+)\s*.*\)")
    #find_library(...) starts with a output variable then has two options
    # 1) the name of the library to search for
    # 2) "NAMES" followed by a list of possible library names
    #It can then be followed by possible paths and various tokens listed below
    #By using the first name in the list I should be to avoid any extra paths that may or may not exist and get
    #  the majority of library names right (since most examples I found were close to "OpenGL, OpenGL3.1, OpenGL, 3.2, etc"
    libraryRegExp = re.compile(r"find_library\s*\(\s*([^\)]+)\s*\)")
    libraryTokens = ['names', 'hints', 'paths', 'path_suffixes', 'doc', 'no_default_path', 'no_cmake_environment_path', 'no_cmake_path', 'no_system_environment_path', 'no_cmake_system_path', 'cmake_find_root_path_both', 'only_cmake_find_root_path',  'no_cmake_find_root_path']

    for name in fileList:
        try:
            cmakeFile = open(name, "r")
            for line in cmakeFile:
                match = packageRegExp.search(line)
                if match != None:
                    foundDep = target.normalizeName(match.group(1))
                    if not foundDep in deps:
                        deps.append(foundDep)

                ignoredFirstParam = False
                match = libraryRegExp.search(line)
                if match != None:
                    paramStr = match.group(1).strip()
                    paramList = paramStr.split(" ")
                    for param in paramList:
                        param = target.normalizeName(param)
                        if param != "":
                            if not ignoredFirstParam:
                                ignoredFirstParam = True
                                continue
                            if param in libraryTokens:
                                continue
                            foundDep = param
                            break
                    if not foundDep.startswith("${") and not foundDep in deps:
                        deps.append(foundDep)
                ignoredFirstParam = False
        finally:
            cmakeFile.close()
    return deps

def isCmakeInstalled():
    return utilityFunctions.isInstalled("cmake")

# Commands
def getPreconfigureCommand():
    #There is no preconfigure command for CMake
    return ""

def getConfigureCommand():
    if not isCmakeInstalled():
        raise exceptions.ToolNotInstalledException("CMake")
    return "cmake " + defines.surround(defines.cmakePrefix[0]) + " " + defines.surround(defines.cmakeCompilers[0])

def getBuildCommand():
    return make.getBuildCommand()

def getInstallCommand():
    return make.getInstallCommand()

def getCleanCommand():
    return make.getCleanCommand()
