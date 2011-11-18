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

def setCompilerDefines(options, compilerOverrides):
    autoTools = ""
    cmake = ""

    if compilerOverrides.CCompiler != "":
        options.setDefine(mdCCompiler[0], compilerOverrides.CCompiler)
        options.setDefine(autoToolsCCompiler[0], autoToolsCCompiler[1])
        options.setDefine(cmakeCCompiler[0], cmakeCCompiler[1])
        autoTools = surround(autoToolsCCompiler[0])
        cmake = surround(autoToolsCCompiler[0])
    if compilerOverrides.CPreProcessor != "":
        options.setDefine(mdCPreProcessor[0], compilerOverrides.CPreProcessor)
        options.setDefine(autoToolsCPreProcessor[0], autoToolsCPreProcessor[1])
        options.setDefine(cmakeCPreProcessor[0], cmakeCPreProcessor[1])
        autoTools += " " + surround(autoToolsCPreProcessor[0])
        cmake += " " + surround(cmakeCPreProcessor[0])
    if compilerOverrides.CXXCompiler != "":
        options.setDefine(mdCXXCompiler[0], compilerOverrides.CXXCompiler)
        options.setDefine(autoToolsCXXCompiler[0], autoToolsCXXCompiler[1])
        autoTools += " " + surround(autoToolsCXXCompiler[0])
    if compilerOverrides.FCompiler != "":
        options.setDefine(mdFCompiler[0], compilerOverrides.FCompiler)
        options.setDefine(autoToolsFCompiler[0], autoToolsFCompiler[1])
        options.setDefine(cmakeFCompiler[0], cmakeFCompiler[1])
        autoTools += " " + surround(autoToolsFCompiler[0])
        cmake += " " + surround(cmakeFCompiler[0])
    if compilerOverrides.F77Compiler != "":
        options.setDefine(mdF77Compiler[0], compilerOverrides.F77Compiler)
        options.setDefine(autoToolsF77Compiler[0], autoToolsF77Compiler[1])
        autoTools += " " + surround(autoToolsF77Compiler[0])
    if compilerOverrides.OBJCCompiler != "":
        options.setDefine(mdOBJCCompiler[0], compilerOverrides.OBJCCompiler)
        options.setDefine(autoToolsOBJCCompiler[0], autoToolsOBJCCompiler[1])
        options.setDefine(cmakeOBJCCompiler[0], cmakeOBJCCompiler[1])
        autoTools += " " + surround(autoToolsOBJCCompiler[0])
        cmake += " " + surround(cmakeOBJCCompiler[0])
    if compilerOverrides.OBJCXXCompiler != "":
        options.setDefine(mdOBJCXXCompiler[0], compilerOverrides.OBJCXXCompiler)
        options.setDefine(autoToolsOBJCXXCompiler[0], autoToolsOBJCXXCompiler[1])
        options.setDefine(cmakeOBJCXXCompiler[0], cmakeOBJCXXCompiler[1])
        autoTools += " " + surround(autoToolsOBJCXXCompiler[0])
        cmake += " " + surround(cmakeOBJCXXCompiler[0])
    if compilerOverrides.OBJCXXPreProcessor != "":
        options.setDefine(mdOBJCXXPreProcessor[0], compilerOverrides.OBJCXXPreProcessor)
        options.setDefine(autoToolsOBJCXXPreProcessor[0], autoToolsOBJCXXPreProcessor[1])
        autoTools += " " + surround(autoToolsOBJCXXCompiler[0])

    options.setDefine(autoToolsCompilers[0], autoTools)
    options.setDefine(cmakeCompilers[0], cmake)

def setOptimizationDefines(options, optimizationOverrides):
    gccCFlags = ""
    gccCPPFlags = ""
    gxxFlags = ""
    gfortranFlags = ""
    g77Flags = ""
    gobjcFlags = ""
    gobjcxxFlags = ""

    #Verbose flags (for example: Optimize = True/False)"
    if optimizationOverrides.optimize != "":
        if optimizationOverrides.optimize == "true":
            options.setDefine(gccOptimize[0], "-O2")
            options.setDefine(gfortranOptimize[0], "-O2")
        else:
            options.setDefine(gccOptimize[0], "-O0")
            options.setDefine(gfortranOptimize[0], "-O0")
        gccCFlags = surround(gccOptimize[0])
        gccCXXFlags = surround(gccOptimize[0])
        gfortranFlags = surround(gfortranOptimize[0])
        g77Flags = surround(gfortranOptimize[0])

    #Account for CMake's undocumented 3 different linker flags.  If not none of the three are
    #  specified by user, just use Linker Flags for all three.
    ldFlags = optimizationOverrides.LinkerFlags
    ldFlagsEXE = optimizationOverrides.LinkerFlagsEXE
    ldFlagsModule = optimizationOverrides.LinkerFlagsModule
    ldFlagsShared = optimizationOverrides.LinkerFlagsShared
    if ldFlags != "" and ldFlagsEXE == "" and ldFlagsModule == "" and ldFlagsShared == "":
        ldFlagsEXE = ldFlags
        ldFlagsModule = ldFlags
        ldFlagsShared = ldFlags

    #Add specified flags last
    if optimizationOverrides.CFlags != "":
        gccCFlags = quoteDefine(gccCFlags, optimizationOverrides.CFlags)
    if optimizationOverrides.CPPFlags != "":
        gccCPPFlags = quoteDefine(gccCPPFlags, optimizationOverrides.CPPFlags)
    if optimizationOverrides.CXXFlags != "":
        gccCXXFlags = quoteDefine(gccCXXFlags, optimizationOverrides.CXXFlags)
    if optimizationOverrides.FFlags != "":
        gfortranFlags = quoteDefine(gfortranFlags, optimizationOverrides.FFlags)
    if optimizationOverrides.F77Flags != "":
        g77Flags = quoteDefine(g77Flags, optimizationOverrides.F77Flags)
    if optimizationOverrides.OBJCFlags != "":
        gobjcFlags = quoteDefine(gobjcFlags, optimizationOverrides.OBJCFlags)
    if optimizationOverrides.OBJCXXFlags != "":
        gobjcxxFlags = quoteDefine(gobjcxxFlags, optimizationOverrides.OBJCXXFlags)

    #TODO: Test which compiler is actually being used and set flags accordingly
    #  For example: gcc gets gccCFlags, icc gets iccCflags

    autoTools = " "
    cmake = " "
    if gccCFlags != "":
        options.setDefine(mdCFlags[0], gccCFlags)
        options.setDefine(autoToolsCFlags[0], autoToolsCFlags[1])
        options.setDefine(cmakeCFlags[0], cmakeCFlags[1])
        autoTools += surround(autoToolsCFlags[0]) + " "
        cmake += surround(cmakeCFlags[0]) + " "
    if gccCPPFlags != "":
        options.setDefine(mdCPPFlags[0], gccCPPFlags)
        options.setDefine(autoToolsCPPFlags[0], autoToolsCPPFlags[1])
        options.setDefine(cmakeCPPFlags[0], cmakeCPPFlags[1])
        autoTools += surround(autoToolsCPPFlags[0]) + " "
        cmake += surround(cmakeCPPFlags[0]) + " "
    if gccCXXFlags != "":
        options.setDefine(mdCXXFlags[0], gccCXXFlags)
        options.setDefine(autoToolsCXXFlags[0], autoToolsCXXFlags[1])
        options.setDefine(cmakeCXXFlags[0], cmakeCXXFlags[1])
        autoTools += surround(autoToolsCXXFlags[0]) + " "
        cmake += surround(cmakeCXXFlags[0]) + " "
    if gfortranFlags != "":
        options.setDefine(mdFFlags[0], gfortranFlags)
        options.setDefine(autoToolsFFlags[0], autoToolsFFlags[1])
        options.setDefine(cmakeFFlags[0], cmakeFFlags[1])
        autoTools += surround(autoToolsFFlags[0]) + " "
        cmake += surround(cmakeFFlags[0]) + " "
    if g77Flags != "":
        options.setDefine(mdF77Flags[0], g77Flags)
        options.setDefine(autoToolsF77Flags[0], autoToolsF77Flags[1])
        options.setDefine(cmakeF77Flags[0], cmakeF77Flags[1])
        autoTools += surround(autoToolsF77Flags[0]) + " "
        cmake += surround(cmakeF77Flags[0]) + " "
    if ldFlags != "":
        options.setDefine(mdLinkerFlags[0], ldFlags)
        options.setDefine(autoToolsLinkerFlags[0], autoToolsLinkerFlags[1])
        autoTools += surround(autoToolsLinkerFlags[0]) + " "
    if ldFlagsEXE != "":
        options.setDefine(mdLinkerFlagsEXE[0], ldFlagsEXE)
        options.setDefine(cmakeLinkerFlagsEXE[0], cmakeLinkerFlagsEXE[1])
        cmake += surround(cmakeLinkerFlagsEXE[0]) + " "
    if ldFlagsModule != "":
        options.setDefine(mdLinkerFlagsModule[0], ldFlagsModule)
        options.setDefine(cmakeLinkerFlagsModule[0], cmakeLinkerFlagsModule[1])
        cmake += surround(cmakeLinkerFlagsModule[0]) + " "
    if ldFlagsShared != "":
        options.setDefine(mdLinkerFlagsShared[0], ldFlagsShared)
        options.setDefine(cmakeLinkerFlagsShared[0], cmakeLinkerFlagsShared[1])
        cmake += surround(cmakeLinkerFlagsShared[0]) + " "
    if gobjcFlags != "":
        options.setDefine(mdOBJCFlags[0], gobjcFlags)
        options.setDefine(autoToolsOBJCFlags[0], autoToolsOBJCFlags[1])
        options.setDefine(cmakeOBJCFlags[0], cmakeOBJCFlags[1])
        autoTools += surround(autoToolsOBJCFlags[0]) + " "
        cmake += surround(cmakeOBJCFlags[0]) + " "
    if gobjcxxFlags != "":
        options.setDefine(mdOBJCXXFlags[0], gobjcxxFlags)
        options.setDefine(autoToolsOBJCXXFlags[0], autoToolsOBJCXXFlags[1])
        options.setDefine(cmakeOBJCXXFlags[0], cmakeOBJCXXFlags[1])
        autoTools += surround(autoToolsOBJCXXFlags[0]) + " "
        cmake += surround(cmakeOBJCXXFlags[0]) + " "

    options.setDefine(autoToolsFlags[0], autoTools)
    options.setDefine(cmakeFlags[0], cmake)

def setParallelDefines(options, parallelDefines):
    pass

def setJobSlotsDefines(options, jobSlots):
    options.setDefine(mdJobSlots[0], jobSlots)
    options.setDefine(makeJobSlots[0], makeJobSlots[1])

def setPrefixDefines(options, prefix):
    options.setDefine(mdPrefix[0], prefix)
    options.setDefine(autoToolsPrefix[0], autoToolsPrefix[1])
    options.setDefine(cmakePrefix[0], cmakePrefix[1])
