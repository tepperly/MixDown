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

    exes = findExecutables(mdOptions.overrideSearchPath, gnuList + intelList)

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
                gnuGroup["cxxpreprocessor"] = fullPath
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

        if len(gnuGroup) > 0:
            gnuGroup.compiler = os.path.join(key, "GNU")
            gnuGroup.optimization = "*"
            gnuGroup.parallel = "*"
            overrideGroups.append(gnuGroup)
        if len(intelGroup) > 0:
            intelGroup.compiler = os.path.join(key, "INTEL")
            intelGroup.optimization = "*"
            intelGroup.parallel = "*"
            overrideGroups.append(intelGroup)

    outFile = open(mdOptions.overrideFile, "w")
    for group in overrideGroups:
        outFile.write(str(group) + "\n")
    outFile.close()

    return True