# Copyright (c) 2010-2012, Lawrence Livermore National Security, LLC
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

import fnmatch, os, Queue
import logger, options, overrides

def findExecutables(dirPairs, exeWildCards):
    executables = []
    q = Queue.Queue()
    for d in dirPairs:
        q.put(d)
    while not q.empty():
        currDirPair = q.get()
        for name in os.listdir(currDirPair[0]):
            fullPath = os.path.join(currDirPair[0], name)
            if os.path.isdir(fullPath) and currDirPair[1]:
                q.put((fullPath, True))
            elif os.access(fullPath, os.X_OK):
                for wildCard in exeWildCards:
                    if fnmatch.fnmatch(name, wildCard):
                        executables.append(fullPath)
    return executables

def profile(mdOptions):
    gnuList = ["gcc", "gobjc", "cpp", "g++", "gfortran", "g77"]
    intelList = ["icc", "icl", "ifort", "ifc"]
    pathscaleList = ["pathCC", "pathcc", "pathf90", "pathf95"]
    portlandGroupList = ["pgcc", "pgCC", "pgf77", "pgf95"]
    fullExeList = gnuList + intelList + pathscaleList + portlandGroupList

    exes = findExecutables(mdOptions.overrideSearchPath, fullExeList)

    groups = {}
    for currPath in exes:
        currDir, currExeName = os.path.split(currPath)
        if not groups.has_key(currDir):
            groups[currDir] = [currExeName]
        elif groups.has_key(currDir) and not currExeName in groups[currDir]:
            groups[currDir].append(currExeName)

    overrideGroups = []
    for key in groups.keys():
        gnuGroup = overrides.OverrideGroup()
        intelGroup = overrides.OverrideGroup()
        pathscaleGroup = overrides.OverrideGroup()
        portlandGroupGroup = overrides.OverrideGroup()
        for exe in groups[key]:
            fullPath = os.path.join(key, exe)
            #GNU
            if exe == "gcc":
                gnuGroup["ccompiler"] = fullPath
            elif exe == "g++":
                gnuGroup["cxxcompiler"] = fullPath
            elif exe == "gobjc":
                gnuGroup["objccompiler"] = fullPath
                gnuGroup["objcxxcompiler"] = fullPath
            elif exe == "cpp":
                gnuGroup["cpreprocessor"] = fullPath
                gnuGroup["objccpreprocessor"] = fullPath
                gnuGroup["objcxxpreprocessor"] = fullPath
            elif exe == "gfortran":
                gnuGroup["fcompiler"] = fullPath
            elif exe == "g77":
                gnuGroup["f77compiler"] = fullPath
            #Intel
            elif exe == "icc":
                intelGroup["ccompiler"] = fullPath
                intelGroup["cxxcompiler"] = fullPath
            elif exe == "icl" and not intelGroup.has_key("ccompiler"):
                intelGroup["ccompiler"] = fullPath
                intelGroup["cxxcompiler"] = fullPath
            elif exe == "ifort":
                intelGroup["fcompiler"] = fullPath
                intelGroup["f77compiler"] = fullPath
            elif exe == "ifc" and not intelGroup.has_key("fcompiler"):
                intelGroup["fcompiler"] = fullPath
                intelGroup["f77compiler"] = fullPath
            #Pathscale
            elif exe == "pathcc":
                pathscaleGroup["ccompiler"] = fullPath
            elif exe == "pathCC":
                pathscaleGroup["cxxcompiler"] = fullPath
            elif exe == "pathf90" and not pathscaleGroup.has_key("fcompiler"):
                pathscaleGroup["f77compiler"] = fullPath
                pathscaleGroup["fcompiler"] = fullPath
            elif exe == "pathf95":
                pathscaleGroup["f77compiler"] = fullPath
                pathscaleGroup["fcompiler"] = fullPath
            #Portland Group
            elif exe == "pgcc":
                portlandGroupGroup["ccompiler"] = fullPath
            elif exe == "pgCC":
                portlandGroupGroup["cxxcompiler"] = fullPath
            elif exe == "pgf77":
                portlandGroupGroup["f77compiler"] = fullPath
            elif exe == "pgf95":
                portlandGroupGroup["fcompiler"] = fullPath

        if len(gnuGroup) > 0:
            gnuGroup.name = [os.path.join(key, "GNU")]
            overrideGroups.append(gnuGroup)
            addGnuOptimizationGroup(overrideGroups, gnuGroup)
        if len(intelGroup) > 0:
            #Do this to stop the creation of intel groups if only cpp is found
            if "cpp" in groups[key]:
                intelGroup["cpreprocessor"] = fullPath

            intelGroup.name = [os.path.join(key, "INTEL")]
            overrideGroups.append(intelGroup)
            addIntelOptimizationGroup(overrideGroups, intelGroup)
        if len(pathscaleGroup) > 0:
            #Do this to stop the creation of pathscale groups if only cpp is found
            if "cpp" in groups[key]:
                pathscaleGroup["cpreprocessor"] = fullPath

            pathscaleGroup.name = [os.path.join(key, "PATHSCALE")]
            overrideGroups.append(pathscaleGroup)
            addPathscaleOptimizationGroup(overrideGroups, pathscaleGroup)
        if len(portlandGroupGroup) > 0:
            #Do this to stop the creation of Portland Group groups if only cpp is found
            if "cpp" in groups[key]:
                portlandGroupGroup["cpreprocessor"] = fullPath

            portlandGroupGroup.name = [os.path.join(key, "PORTLANDGROUP")]
            overrideGroups.append(portlandGroupGroup)
            addPortlandGroupOptimizationGroup(overrideGroups, portlandGroupGroup)

    outFile = open(mdOptions.overrideFile, "w")
    for group in overrideGroups:
        outFile.write(str(group) + "\n")
    outFile.close()

    return True

def addGnuOptimizationGroup(groups, compilerGroup):
    debugGroup = overrides.OverrideGroup()
    debugGroup.name = [compilerGroup.name[0], "debug"]

    releaseGroup = overrides.OverrideGroup()
    releaseGroup.name = [compilerGroup.name[0], "release"]

    gccDebugFlags = "-g -O0 -Wall"
    gccReleaseFlags = "-O2 -Wall"
    if compilerGroup.has_key("ccompiler"):
        debugGroup["cflags"] = gccDebugFlags
        releaseGroup["cflags"] = gccReleaseFlags
    if compilerGroup.has_key("cxxcompiler"):
        debugGroup["cxxflags"] = gccDebugFlags
        releaseGroup["cxxflags"] = gccReleaseFlags
    if compilerGroup.has_key("objccompiler"):
        debugGroup["objcflags"] = gccDebugFlags
        releaseGroup["objcflags"] = gccReleaseFlags
    if compilerGroup.has_key("objcxxcompiler"):
        debugGroup["objcxxflags"] = gccDebugFlags
        releaseGroup["objcxxflags"] = gccReleaseFlags
    if compilerGroup.has_key("cpreprocessor"):
        debugGroup["cppflags"] = "-Wall"
        releaseGroup["cppflags"] = "-Wall"
    if compilerGroup.has_key("fcompiler"):
        debugGroup["fflags"] = "-Wall"
        releaseGroup["fflags"] = "-Wall"
    if compilerGroup.has_key("f77compiler"):
        debugGroup["f77flags"] = "-Wall"
        releaseGroup["f77flags"] = "-Wall"

    if len(debugGroup) > 0:
        groups.append(debugGroup)
    if len(releaseGroup) > 0:
        groups.append(releaseGroup)

def addIntelOptimizationGroup(groups, compilerGroup):
    debugGroup = overrides.OverrideGroup()
    debugGroup.name = [compilerGroup.name[0], "debug"]

    releaseGroup = overrides.OverrideGroup()
    releaseGroup.name = [compilerGroup.name[0], "release"]

    iccDebugFlags = "-debug full -O0 -Wall"
    iccReleaseFlags = "-debug none -O2 -Wall"
    if compilerGroup.has_key("ccompiler"):
        debugGroup["cflags"] = iccDebugFlags
        releaseGroup["cflags"] = iccReleaseFlags
    if compilerGroup.has_key("cxxcompiler"):
        debugGroup["cxxflags"] = iccDebugFlags
        releaseGroup["cxxflags"] = iccReleaseFlags
    if compilerGroup.has_key("cpreprocessor"):
        debugGroup["cppflags"] = "-Wall"
        releaseGroup["cppflags"] = "-Wall"
    if compilerGroup.has_key("fcompiler"):
        debugGroup["fflags"] = "-O0 -warn all"
        releaseGroup["fflags"] = "-O2 -warn all"
    if compilerGroup.has_key("f77compiler"):
        debugGroup["f77flags"] = "-O0 -warn all"
        releaseGroup["f77flags"] = "-O2 -warn all"

    if len(debugGroup) > 0:
        groups.append(debugGroup)
    if len(releaseGroup) > 0:
        groups.append(releaseGroup)

def addPathscaleOptimizationGroup(groups, compilerGroup):
    debugGroup = overrides.OverrideGroup()
    debugGroup.name = [compilerGroup.name[0], "debug"]

    releaseGroup = overrides.OverrideGroup()
    releaseGroup.name = [compilerGroup.name[0], "release"]

    pathDebugFlags = "-g -O0 -Wall"
    pathReleaseFlags = "-O2 -Wall"
    if compilerGroup.has_key("ccompiler"):
        debugGroup["cflags"] = pathDebugFlags
        releaseGroup["cflags"] = pathReleaseFlags
    if compilerGroup.has_key("cxxcompiler"):
        debugGroup["cxxflags"] = pathDebugFlags
        releaseGroup["cxxflags"] = pathReleaseFlags
    if compilerGroup.has_key("cpreprocessor"):
        debugGroup["cppflags"] = "-Wall"
        releaseGroup["cppflags"] = "-Wall"
    if compilerGroup.has_key("fcompiler"):
        debugGroup["fflags"] = pathDebugFlags
        releaseGroup["fflags"] = pathReleaseFlags
    if compilerGroup.has_key("f77compiler"):
        debugGroup["f77flags"] = pathDebugFlags
        releaseGroup["f77flags"] = pathReleaseFlags

    if len(debugGroup) > 0:
        groups.append(debugGroup)
    if len(releaseGroup) > 0:
        groups.append(releaseGroup)

def addPortlandGroupOptimizationGroup(groups, compilerGroup):
    debugGroup = overrides.OverrideGroup()
    debugGroup.name = [compilerGroup.name[0], "debug"]

    releaseGroup = overrides.OverrideGroup()
    releaseGroup.name = [compilerGroup.name[0], "release"]

    portlandDebugFlags = "-g -O0"
    portlandReleaseFlags = "-O2"
    if compilerGroup.has_key("ccompiler"):
        debugGroup["cflags"] = portlandDebugFlags
        releaseGroup["cflags"] = portlandReleaseFlags
    if compilerGroup.has_key("cxxcompiler"):
        debugGroup["cxxflags"] = portlandDebugFlags
        releaseGroup["cxxflags"] = portlandReleaseFlags
    if compilerGroup.has_key("cpreprocessor"):
        debugGroup["cppflags"] = "-Wall"
        releaseGroup["cppflags"] = "-Wall"
    if compilerGroup.has_key("fcompiler"):
        debugGroup["fflags"] = portlandDebugFlags
        releaseGroup["fflags"] = portlandReleaseFlags
    if compilerGroup.has_key("f77compiler"):
        debugGroup["f77flags"] = portlandDebugFlags
        releaseGroup["f77flags"] = portlandReleaseFlags

    if len(debugGroup) > 0:
        groups.append(debugGroup)
    if len(releaseGroup) > 0:
        groups.append(releaseGroup)
