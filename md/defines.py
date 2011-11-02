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

#General
mdCCompiler = "_CCompiler", ""
mdCPreProcessor = "_CPreProcessor", ""
mdCXXCompiler = "_CXXCompiler", ""
mdFCompiler = "_FCompiler", ""
mdF77Compiler = "_F77Compiler", ""
mdOBJCCompiler = "_OBJCCompiler", ""
mdOBJCPreProcessor = "_OBJCPreProcessor", ""
mdOBJCXXCompiler = "_OBJCCompiler", ""
mdOBJCXXPreProcessor = "_OBJCPreProcessor", ""

mdCFlags = "_CFlags", ""
mdCXXFlags = "_CXXFlags", ""
mdFFlags = "_FFlags", ""

mdJobSlots = "_JobSlots", ""
mdPrefix = "_Prefix", ""

#AutoTools
autoToolsPrefix = "_AutoToolsPrefix", "--prefix=" + surround(mdPrefix[0])

autoToolsCCompiler = "_AutotoolsCCompiler", "CC=" + surround(mdCCompiler[0])
autoToolsCPreProcessor = "_AutotoolsCPreProcessor", "CPP=" + surround(mdCPreProcessor[0])
autoToolsCXXCompiler = "_AutotoolsCXXCompiler", "CXX=" + surround(mdCXXCompiler[0])
autoToolsFCompiler = "_AutotoolsFCompiler", "FC=" + surround(mdFCompiler[0])
autoToolsF77Compiler = "_AutotoolsF77Compiler", "F77=" + surround(mdF77Compiler[0])
autoToolsOBJCCompiler = "_AutotoolsOBJCCompiler", "OBJC=" + surround(mdOBJCCompiler[0])
autoToolsOBJCPreProcessor = "_AutotoolsOBJCPreProcessor", "OBJCPP=" + surround(mdOBJCPreProcessor[0])
autoToolsOBJCXXCompiler = "_AutotoolsOBJCCompiler", "OBJCXX=" + surround(mdOBJCXXCompiler[0])
autoToolsOBJCXXPreProcessor = "_AutotoolsOBJCPreProcessor", "OBJCXXCPP=" + surround(mdOBJCXXPreProcessor[0])

autoToolsCFlags = "_AutotoolsCFlags", "CFLAGS=" + surround(mdCFlags[0])
autoToolsCXXFlags = "_AutotoolsCXXFlags", "CXXFLAGS=" + surround(mdCXXFlags[0])
autoToolsFFlags = "_AutotoolsFFlags", "FFLAGS=" + surround(mdFFlags[0])

autoToolsCompilers = "_AutoToolsCompilers", ""
autoToolsFlags = "_AutoToolsFlags", ""

#CMake
cmakePrefix = "_CMakePrefix", "-DCMAKE_PREFIX_PATH=" + surround(mdPrefix[0]) + " -DCMAKE_INSTALL_PREFIX=" + surround(mdPrefix[0])

cmakeCCompiler = "_CMakeCCompiler", "-DCMAKE_C_COMPILER=" + surround(mdCCompiler[0])
cmakeCPreProcessor = "_CMakeCPreProcessor", "" #CMake doesn't have a default way to override this
cmakeCXXCompiler = "_CMakeCXXCompiler","-DCMAKE_CXX_COMPILER=" + surround(mdCXXCompiler[0])
cmakeFCompiler = "_CMakeFCompiler", "-DCMAKE_Fortran_COMPILER=" + surround(mdFCompiler[0])
cmakeF77Compiler = "_CMakeF77Compiler", "" #CMake only has one Fortran compiler override
cmakeOBJCCompiler = "_CMakeOBJCCompiler", "-DCMAKE_OBJC_COMPILER=" + surround(mdOBJCCompiler[0]) #Guessed
cmakeOBJCPreProcessor = "_CMakeOBJCPreProcessor", "-DCMAKE_OBJCPP_COMPILER=" + surround(mdOBJCPreProcessor[0]) #Guessed
cmakeOBJCXXCompiler = "_CMakeOBJCCompiler", "-DCMAKE_OBJCXX_COMPILER=" + surround(mdOBJCXXCompiler[0]) #Guessed
cmakeOBJCXXPreProcessor = "_CMakeOBJCPreProcessor", "-DCMAKE_OBJCXXCPP_COMPILER=" + surround(mdOBJCXXPreProcessor[0]) #Guessed

cmakeCFlags = "_CMakeCFlags", "-DCMAKE_C_FLAGS=" + surround(mdCFlags[0])
cmakeCXXFlags = "_CMakeCXXFlags", " -DCMAKE_CXX_FLAGS=" + surround(mdCXXFlags[0])
cmakeFFlags = "_CMakeFFlags", "-DCMAKE_Fortran_FLAGS=" + surround(mdFFlags[0])  #Guessed

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
    if compilerOverrides.OBJCPreProcessor != "":
        options.setDefine(mdOBJCPreProcessor[0], compilerOverrides.OBJCPreProcessor)
        options.setDefine(autoToolsOBJCPreProcessor[0], autoToolsOBJCPreProcessor[1])
        options.setDefine(cmakeOBJCPreProcessor[0], cmakeOBJCPreProcessor[1])
        autoTools += " " + surround(autoToolsOBJCPreProcessor[0])
        cmake += " " + surround(cmakeOBJCPreProcessor[0])
    if compilerOverrides.OBJCXXCompiler != "":
        options.setDefine(mdOBJCXXCompiler[0], compilerOverrides.OBJCXXCompiler)
        options.setDefine(autoToolsOBJCXXCompiler[0], autoToolsOBJCXXCompiler[1])
        options.setDefine(cmakeOBJCXXCompiler[0], cmakeOBJCXXCompiler[1])
        autoTools += " " + surround(autoToolsOBJCXXCompiler[0])
        cmake += " " + surround(cmakeOBJCXXCompiler[0])
    if compilerOverrides.OBJCXXPreProcessor != "":
        options.setDefine(mdOBJCXXPreProcessor[0], compilerOverrides.OBJCXXPreProcessor)
        options.setDefine(autoToolsOBJCXXPreProcessor[0], autoToolsOBJCXXPreProcessor[1])
        options.setDefine(cmakeOBJCXXPreProcessor[0], cmakeOBJCXXPreProcessor[1])
        autoTools += " " + surround(autoToolsOBJCXXPreProcessor[0])
        cmake += " " + surround(cmakeOBJCXXPreProcessor[0])

    options.setDefine(autoToolsCompilers[0], autoTools)
    options.setDefine(cmakeCompilers[0], cmake)

def setOptimizationDefines(options, optimizationOverrides):
    gccCFlags = ""
    gccCXXFlags = ""
    gfortranFFlags = ""

    if optimizationOverrides.optimize != "":
        if optimizationOverrides.optimize == "true":
            options.setDefine(gccOptimize[0], "-O2")
            options.setDefine(gfortranOptimize[0], "-O2")
        else:
            options.setDefine(gccOptimize[0], "-O0")
            options.setDefine(gfortranOptimize[0], "-O0")
        gccCFlags = surround(gccOptimize[0])
        gccCXXFlags = surround(gccOptimize[0])
        gfortranFFlags = surround(gfortranOptimize[0])

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
    if gccCXXFlags != "":
        options.setDefine(mdCXXFlags[0], gccCXXFlags)
        options.setDefine(autoToolsCXXFlags[0], autoToolsCXXFlags[1])
        options.setDefine(cmakeCXXFlags[0], cmakeCXXFlags[1])
        autoTools += surround(autoToolsCXXFlags[0]) + " "
        cmake += surround(cmakeCXXFlags[0]) + " "
    if gfortranFFlags != "":
        options.setDefine(mdFFlags[0], gfortranFFlags)
        options.setDefine(autoToolsFFlags[0], autoToolsFFlags[1])
        options.setDefine(cmakeFFlags[0], cmakeFFlags[1])
        autoTools += surround(autoToolsFFlags[0]) + " "
        cmake += surround(cmakeFFlags[0]) + " "

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

