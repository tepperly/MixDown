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

import os, overrides

class Defines(object):
    def __init__(self):
        self._defines = dict()

    def keys(self):
        return self._defines.keys()

    def set(self, key, value):
        self._defines[normalizeKey(key)] = value.strip()

    def get(self, key):
        normalizedKey = normalizeKey(key)
        strippedKey = normalizeKey(key, False)
        if normalizedKey in self._defines:
            value = self._defines[normalizedKey]
        elif strippedKey in os.environ:
            value = os.environ[strippedKey]
        else:
            value = ""
        return value

    def combine(self, overridingDefines):
        for key in overridingDefines.keys():
            self.set(key, overridingDefines.get(key))

    def expand(self, inString):
        if inString == "":
            return ""
        expandedString = inString
        loopCount = 0
        while expandedString.find("$(") != -1:
            if loopCount > 50:
                logger.writeError("Define depth count (10) exceeded in string '" + inString + "'", exitProgram=True)

            strLength = len(expandedString)
            startIndex = 0
            endIndex = 0
            for i in range(strLength):
                if expandedString[i] == "$":
                    if strLength - i < 4:
                        if inString == expandedString:
                            logger.writeError("Unterminated define found in '" + inString + "' at index " + str(i), exitProgram=True)
                        else:
                            logger.writeError("Unterminated define found in original string '" + inString + "'\n After expanding defines, '" + expandedString + "'", exitProgram=True)
                    startIndex = i
                    break
            if startIndex != 0:
                for j in range(startIndex, strLength):
                    if expandedString[j] == ")":
                        endIndex = j
                        break
                defineName = expandedString[startIndex:endIndex+1]
                defineValue = self.get(defineName)
                expandedString = expandedString.replace(defineName, defineValue)
            loopCount += 1
        expandedString = expandedString.replace("  ", " ").strip()
        return expandedString

def normalizeKey(key, lower=True):
    normalizedKey = key.strip()
    if lower:
        normalizedKey = normalizedKey.lower()
    if normalizedKey.startswith("$("):
        normalizedKey = normalizedKey[2:]
        if normalizedKey.endswith(")"):
            normalizedKey = normalizedKey[:-1]
        normalizedKey = normalizedKey.strip()
    return normalizedKey

#Expands define name to full define
def surround(name):
    return "$(" + name + ")"

#-----------------AutoTools----------------
mdJobSlots = "_JobSlots", ""
mdPrefix = "_Prefix", ""

#Compilers
mdCCompiler = "_CCompiler", ""
mdCPreProcessor = "_CPreProcessor", ""
mdCXXCompiler = "_CXXCompiler", ""
mdFCompiler = "_FCompiler", ""
mdF77Compiler = "_F77Compiler", ""
mdOBJCCompiler = "_OBJCCompiler", ""
mdOBJCXXCompiler = "_OBJCXXCompiler", ""
mdOBJCXXPreProcessor = "_OBJCXXPreProcessor", ""

#Compilers Flags
mdCFlags = "_CFlags", ""
mdCDefines = "_CDefines", ""
mdCPPFlags = "_CPPFlags", ""
mdCXXFlags = "_CXXFlags", ""
mdFFlags = "_FFlags", ""
mdF77Flags = "_F77Flags", ""
mdLinkerFlags = "_LinkerFlags", ""
mdLinkerFlagsEXE = "_mdLinkerFlagsEXE", ""
mdLinkerFlagsModule = "_mdLinkerFlagsModule", ""
mdLinkerFlagsShared = "_mdLinkerFlagsShared", ""
mdOBJCFlags = "OBJCFlags", ""
mdOBJCXXFlags = "OBJCXXFlags", ""

#Libraries
mdLibs = "_Libs", ""
mdFLibs = "_FLibs", ""
mdF77Libs = "_F77Libs", ""

#-----------------AutoTools----------------
autoToolsPrefix = "_AutoToolsPrefix", "--prefix=" + surround(mdPrefix[0])

#Compilers
autoToolsCCompiler = "_AutotoolsCCompiler", "CC=" + surround(mdCCompiler[0])
autoToolsCPreProcessor = "_AutotoolsCPreProcessor", "CPP=" + surround(mdCPreProcessor[0])
autoToolsCXXCompiler = "_AutotoolsCXXCompiler", "CXX=" + surround(mdCXXCompiler[0])
autoToolsFCompiler = "_AutotoolsFCompiler", "FC=" + surround(mdFCompiler[0])
autoToolsF77Compiler = "_AutotoolsF77Compiler", "F77=" + surround(mdF77Compiler[0])
autoToolsOBJCCompiler = "_AutotoolsOBJCCompiler", "OBJC=" + surround(mdOBJCCompiler[0])
autoToolsOBJCXXCompiler = "_AutotoolsOBJCCompiler", "OBJCXX=" + surround(mdOBJCXXCompiler[0])
autoToolsOBJCXXPreProcessor = "_AutotoolsOBJCPreProcessor", "OBJCXXCPP=" + surround(mdOBJCXXPreProcessor[0])

#Compilers Flags
autoToolsCFlags = "_AutotoolsCFlags", "CFLAGS=" + surround(mdCFlags[0])
autoToolsCDefines = "_AutotoolsCDefines", "DEFS=" + surround(mdCDefines[0])
autoToolsCPPFlags = "_AutotoolsCPPFlags", "CPPFLAGS=" + surround(mdCPPFlags[0])
autoToolsCXXFlags = "_AutotoolsCXXFlags", "CXXFLAGS=" + surround(mdCXXFlags[0])
autoToolsFFlags = "_AutotoolsFFlags", "FCFLAGS=" + surround(mdFFlags[0])
autoToolsF77Flags = "_AutotoolsF77Flags", "FFLAGS=" + surround(mdF77Flags[0])
autoToolsLinkerFlags = "_AutotoolsLinkerFlags", "LDFLAGS=" + surround(mdLinkerFlags[0])
autoToolsOBJCFlags = "_AutotoolsOBJCFlags", "OBJCFLAGS=" + surround(mdOBJCFlags[0])
autoToolsOBJCXXFlags = "_AutotoolsOBJCFlags", "OBJCXXFLAGS=" + surround(mdOBJCXXFlags[0])

#Libraries
autoToolsLibs = "_AutotoolsLibs", "LIBS=" + surround(mdLibs[0])
autoToolsFLibs = "_AutotoolsFLibs", "FCLIBS=" + surround(mdFLibs[0])
autoToolsF77Libs = "_AutotoolsF77Libs", "FLIBS=" + surround(mdF77Libs[0])

autoToolsCompilers = "_AutoToolsCompilers", ""
autoToolsFlags = "_AutoToolsFlags", ""

#-----------------CMake----------------
cmakePrefix = "_CMakePrefix", "-DCMAKE_PREFIX_PATH=" + surround(mdPrefix[0]) + " -DCMAKE_INSTALL_PREFIX=" + surround(mdPrefix[0])

#Compilers
cmakeCCompiler = "_CMakeCCompiler", "-DCMAKE_C_COMPILER=" + surround(mdCCompiler[0])
cmakeCXXCompiler = "_CMakeCXXCompiler","-DCMAKE_CXX_COMPILER=" + surround(mdCXXCompiler[0])
cmakeFCompiler = "_CMakeFCompiler", "-DCMAKE_Fortran_COMPILER=" + surround(mdFCompiler[0])
cmakeF77Compiler = "_CMakeF77Compiler", "-DCMAKE_F77_COMPILER=" + surround(mdF77Compiler[0])
cmakeOBJCCompiler = "_CMakeOBJCCompiler", "-DCMAKE_OBJC_COMPILER=" + surround(mdOBJCCompiler[0])
cmakeOBJCXXCompiler = "_CMakeOBJCCompiler", "-DCMAKE_OBJCXX_COMPILER=" + surround(mdOBJCXXCompiler[0])

#Compilers Flags
cmakeCFlags = "_CMakeCFlags", "-DCMAKE_C_FLAGS=" + surround(mdCFlags[0])
cmakeCXXFlags = "_CMakeCXXFlags", " -DCMAKE_CXX_FLAGS=" + surround(mdCXXFlags[0])
cmakeFFlags = "_CMakeFFlags", "-DCMAKE_Fortran_FLAGS=" + surround(mdFFlags[0])
cmakeF77Flags = "_CMakeF77Flags", "-DCMAKE_F77_FLAGS=" + surround(mdF77Flags[0])
cmakeLinkerFlagsEXE = "_CMakeLinkerFlagsEXE", "-DCMAKE_EXE_LINKER_FLAGS=" + surround(mdLinkerFlagsEXE[0])
cmakeLinkerFlagsModule = "_CMakeLinkerFlagsModule", "-DCMAKE_MODULE_LINKER_FLAGS=" + surround(mdLinkerFlagsModule[0])
cmakeLinkerFlagsShared = "_CMakeLinkerFlagsShared", "-DCMAKE_SHARED_LINKER_FLAGS=" + surround(mdLinkerFlagsShared[0])
cmakeOBJCFlags = "_CMakeOBJCFlags", "-DCMAKE_OBJC_FLAGS=" + surround(mdOBJCFlags[0])
cmakeOBJCXXFlags = "_CMakeOBJCFlags", "-DCMAKE_OBJCXX_FLAGS=" + surround(mdOBJCXXFlags[0])

cmakeCompilers = "_CMakeCompilers", ""
cmakeFlags = "_CMakeFlags", ""

#GNUMake
makeJobSlots = "_MakeJobSlots", "-j" + surround(mdJobSlots[0])

#GCC
gccCFlags = "_GCCCFlags", ""
gccCXXFlags = "_GCCCXXFlags", ""
gccOptimize = "_GCCOptimize", ""

#gfortran
gfortranFFlags = "_GFortranFFlags", ""
gfortranOptimize = "_GFortranOptimize", ""

#-----------------Set Defines----------------
def quoteDefine(define, defineToBeAdded=""):
    if defineToBeAdded == "":
        finalDefine = '"' + define.strip('"') + '"'
    else:
        finalDefine = '"' + define.strip('"') + " " + defineToBeAdded.strip('"') + '"'
    return finalDefine

def setOverrideDefines(defs, overrideGroup):
    __setToolDefines(defs, overrideGroup)
    __setFlagDefines(defs, overrideGroup)

def __setToolDefines(defs, overrideGroup):
    autoTools = ""
    cmake = ""

    if overrideGroup.hasOverride("CCompiler"):
        defs.set(mdCCompiler[0], overrideGroup.getOverride("CCompiler"))
        defs.set(autoToolsCCompiler[0], autoToolsCCompiler[1])
        defs.set(cmakeCCompiler[0], cmakeCCompiler[1])
        autoTools = surround(autoToolsCCompiler[0])
        cmake = surround(autoToolsCCompiler[0])
    if overrideGroup.hasOverride("CPreProcessor"):
        defs.set(mdCPreProcessor[0], overrideGroup.getOverride("CPreProcessor"))
        defs.set(autoToolsCPreProcessor[0], autoToolsCPreProcessor[1])
        defs.set(cmakeCPreProcessor[0], cmakeCPreProcessor[1])
        autoTools += " " + surround(autoToolsCPreProcessor[0])
        cmake += " " + surround(cmakeCPreProcessor[0])
    if overrideGroup.hasOverride("CXXCompiler"):
        defs.set(mdCXXCompiler[0], overrideGroup.getOverride("CXXCompiler"))
        defs.set(autoToolsCXXCompiler[0], autoToolsCXXCompiler[1])
        autoTools += " " + surround(autoToolsCXXCompiler[0])
    if overrideGroup.hasOverride("FCompiler"):
        defs.set(mdFCompiler[0], overrideGroup.getOverride("FCompiler"))
        defs.set(autoToolsFCompiler[0], autoToolsFCompiler[1])
        defs.set(cmakeFCompiler[0], cmakeFCompiler[1])
        autoTools += " " + surround(autoToolsFCompiler[0])
        cmake += " " + surround(cmakeFCompiler[0])
    if overrideGroup.hasOverride("F77Compiler"):
        defs.set(mdF77Compiler[0], overrideGroup.getOverride("F77Compiler"))
        defs.set(autoToolsF77Compiler[0], autoToolsF77Compiler[1])
        autoTools += " " + surround(autoToolsF77Compiler[0])
    if overrideGroup.hasOverride("OBJCCompiler"):
        defs.set(mdOBJCCompiler[0], overrideGroup.getOverride("OBJCCompiler"))
        defs.set(autoToolsOBJCCompiler[0], autoToolsOBJCCompiler[1])
        defs.set(cmakeOBJCCompiler[0], cmakeOBJCCompiler[1])
        autoTools += " " + surround(autoToolsOBJCCompiler[0])
        cmake += " " + surround(cmakeOBJCCompiler[0])
    if overrideGroup.hasOverride("OBJCXXCompiler"):
        defs.set(mdOBJCXXCompiler[0], overrideGroup.getOverride("OBJCXXCompiler"))
        defs.set(autoToolsOBJCXXCompiler[0], autoToolsOBJCXXCompiler[1])
        defs.set(cmakeOBJCXXCompiler[0], cmakeOBJCXXCompiler[1])
        autoTools += " " + surround(autoToolsOBJCXXCompiler[0])
        cmake += " " + surround(cmakeOBJCXXCompiler[0])
    if overrideGroup.hasOverride("OBJCXXPreProcessor"):
        defs.set(mdOBJCXXPreProcessor[0], overrideGroup.getOverride("OBJCXXPreProcessor"))
        defs.set(autoToolsOBJCXXPreProcessor[0], autoToolsOBJCXXPreProcessor[1])
        autoTools += " " + surround(autoToolsOBJCXXCompiler[0])

    defs.set(autoToolsCompilers[0], autoTools)
    defs.set(cmakeCompilers[0], cmake)

def __setFlagDefines(defs, overrideGroup):
    autoTools = " "
    cmake = " "

    #Account for CMake's undocumented 3 different linker flags.  If not none of the three are
    #  specified by user, just use Linker Flags for all three.
    ldFlags = ""
    ldFlagsEXE = ""
    ldFlagsModule = ""
    ldFlagsShared = ""
    if overrideGroup.hasOverride("LinkerFlags"):
        ldFlags = overrideGroup.getOverride("LinkerFlags")
    if overrideGroup.hasOverride("LinkerFlagsEXE"):
        ldFlagsEXE = overrideGroup.getOverride("LinkerFlagsEXE")
    if overrideGroup.hasOverride("LinkerFlagsModule"):
        ldFlagsModule = overrideGroup.getOverride("LinkerFlagsModule")
    if overrideGroup.hasOverride("LinkerFlagsShared"):
        ldFlagsShared = overrideGroup.getOverride("LinkerFlagsShared")
    if ldFlags != "" and ldFlagsEXE == "" and ldFlagsModule == "" and ldFlagsShared == "":
        ldFlagsEXE = ldFlags
        ldFlagsModule = ldFlags
        ldFlagsShared = ldFlags

    if ldFlags != "":
        defs.set(mdLinkerFlags[0], quoteDefine(ldFlags))
        defs.set(autoToolsLinkerFlags[0], autoToolsLinkerFlags[1])
        autoTools += surround(autoToolsLinkerFlags[0]) + " "
    if ldFlagsEXE != "":
        defs.set(mdLinkerFlagsEXE[0], quoteDefine(ldFlagsEXE))
        defs.set(cmakeLinkerFlagsEXE[0], cmakeLinkerFlagsEXE[1])
        cmake += surround(cmakeLinkerFlagsEXE[0]) + " "
    if ldFlagsModule != "":
        defs.set(mdLinkerFlagsModule[0], quoteDefine(ldFlagsModule))
        defs.set(cmakeLinkerFlagsModule[0], cmakeLinkerFlagsModule[1])
        cmake += surround(cmakeLinkerFlagsModule[0]) + " "
    if ldFlagsShared != "":
        defs.set(mdLinkerFlagsShared[0], quoteDefine(ldFlagsShared))
        defs.set(cmakeLinkerFlagsShared[0], cmakeLinkerFlagsShared[1])
        cmake += surround(cmakeLinkerFlagsShared[0]) + " "

    if overrideGroup.hasOverride("CFlags"):
        defs.set(mdCFlags[0], quoteDefine(overrideGroup.getOverride("CFlags")))
        defs.set(autoToolsCFlags[0], autoToolsCFlags[1])
        defs.set(cmakeCFlags[0], cmakeCFlags[1])
        autoTools += surround(autoToolsCFlags[0]) + " "
        cmake += surround(cmakeCFlags[0]) + " "
    if overrideGroup.hasOverride("CPPFlags"):
        defs.set(mdCPPFlags[0], quoteDefine(overrideGroup.getOverride("CPPFlags")))
        defs.set(autoToolsCPPFlags[0], autoToolsCPPFlags[1])
        defs.set(cmakeCPPFlags[0], cmakeCPPFlags[1])
        autoTools += surround(autoToolsCPPFlags[0]) + " "
        cmake += surround(cmakeCPPFlags[0]) + " "
    if overrideGroup.hasOverride("CXXFlags"):
        defs.set(mdCXXFlags[0], quoteDefine(overrideGroup.getOverride("CXXFlags")))
        defs.set(autoToolsCXXFlags[0], autoToolsCXXFlags[1])
        defs.set(cmakeCXXFlags[0], cmakeCXXFlags[1])
        autoTools += surround(autoToolsCXXFlags[0]) + " "
        cmake += surround(cmakeCXXFlags[0]) + " "
    if overrideGroup.hasOverride("FFlags"):
        defs.set(mdFFlags[0], quoteDefine(overrideGroup.getOverride("FFlags")))
        defs.set(autoToolsFFlags[0], autoToolsFFlags[1])
        defs.set(cmakeFFlags[0], cmakeFFlags[1])
        autoTools += surround(autoToolsFFlags[0]) + " "
        cmake += surround(cmakeFFlags[0]) + " "
    if overrideGroup.hasOverride("F77Flags"):
        defs.set(mdF77Flags[0], quoteDefine(overrideGroup.getOverride("F77Flags")))
        defs.set(autoToolsF77Flags[0], autoToolsF77Flags[1])
        defs.set(cmakeF77Flags[0], cmakeF77Flags[1])
        autoTools += surround(autoToolsF77Flags[0]) + " "
        cmake += surround(cmakeF77Flags[0]) + " "
    if overrideGroup.hasOverride("OBJCFlags"):
        defs.set(mdOBJCFlags[0], quoteDefine(overrideGroup.getOverride("OBJCFlags")))
        defs.set(autoToolsOBJCFlags[0], autoToolsOBJCFlags[1])
        defs.set(cmakeOBJCFlags[0], cmakeOBJCFlags[1])
        autoTools += surround(autoToolsOBJCFlags[0]) + " "
        cmake += surround(cmakeOBJCFlags[0]) + " "
    if overrideGroup.hasOverride("OBJCXXFlags"):
        defs.set(mdOBJCXXFlags[0], quoteDefine(overrideGroup.getOverride("OBJCXXFlags")))
        defs.set(autoToolsOBJCXXFlags[0], autoToolsOBJCXXFlags[1])
        defs.set(cmakeOBJCXXFlags[0], cmakeOBJCXXFlags[1])
        autoTools += surround(autoToolsOBJCXXFlags[0]) + " "
        cmake += surround(cmakeOBJCXXFlags[0]) + " "

    defs.set(autoToolsFlags[0], autoTools)
    defs.set(cmakeFlags[0], cmake)

def setJobSlotsDefines(defs, jobSlots):
    defs.set(mdJobSlots[0], jobSlots)
    defs.set(makeJobSlots[0], makeJobSlots[1])

def setPrefixDefines(defs, prefix):
    defs.set(mdPrefix[0], prefix)
    defs.set(autoToolsPrefix[0], autoToolsPrefix[1])
    defs.set(cmakePrefix[0], cmakePrefix[1])
