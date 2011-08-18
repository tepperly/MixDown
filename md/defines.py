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

mdJobSlots = "_JobSlots", ""
mdPrefix = "_Prefix", ""

#AutoTool
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

autoToolsCompilers = "_AutoToolsCompilers", surround(autoToolsCCompiler[0]) + " " + surround(autoToolsCXXCompiler[0]) + " " + surround(autoToolsCPreProcessor[0])

#CMake
cmakePrefix = "_CMakePrefix", "-DCMAKE_PREFIX_PATH=" + surround(mdPrefix[0]) + " -DCMAKE_INSTALL_PREFIX=" + surround(mdPrefix[0])

cmakeCCompiler = "_CMakeCCompiler", "-DCMAKE_C_COMPILER=" + surround(mdCCompiler[0])
cmakeCPreProcessor = "_CMakeCPreProcessor", "" #CMake doesn't have a default way to override this
cmakeCXXCompiler = "_CMakeCXXCompiler","-DCMAKE_CXX_COMPILER=" + surround(mdCXXCompiler[0])
cmakeFCompiler = "_CMakeFCompiler", "-DCMAKE_Fortran_COMPILER=" + surround(mdFCompiler[0])
cmakeF77Compiler = "_CMakeF77Compiler", "" #CMake only has one Fortran compiler override
cmakeOBJCCompiler = "_CMakeOBJCCompiler", "OBJC=" + surround(mdOBJCCompiler[0])
cmakesOBJCPreProcessor = "_CMakeOBJCPreProcessor", "OBJCPP=" + surround(mdOBJCPreProcessor[0])
cmakeOBJCXXCompiler = "_CMakeOBJCCompiler", "OBJCXX=" + surround(mdOBJCXXCompiler[0])
cmakeOBJCXXPreProcessor = "_CMakeOBJCPreProcessor", "OBJCXXCPP=" + surround(mdOBJCXXPreProcessor[0])

cmakeCompilers = "_CMakeCompilers", surround(cmakeCCompiler[0]) + " " + surround(cmakeCXXCompiler[0])

#GNUMake
makeJobSlots = "_MakeJobSlots", "-j" + surround(mdJobSlots[0])

def setCompilerDefines(options, CCompiler, CXXCompiler, CPreProcessor):
    options.setDefine(mdCCompiler[0], CCompiler)
    options.setDefine(mdCXXCompiler[0], CXXCompiler)
    options.setDefine(mdCPreProcessor[0], CPreProcessor)

    options.setDefine(autoToolsCCompiler[0], autoToolsCCompiler[1])
    options.setDefine(autoToolsCXXCompiler[0], autoToolsCXXCompiler[1])
    options.setDefine(autoToolsCPreProcessor[0], autoToolsCPreProcessor[1])
    options.setDefine(autoToolsCompilers[0], autoToolsCompilers[1])

    options.setDefine(cmakeCCompiler[0], cmakeCCompiler[1])
    options.setDefine(cmakeCXXCompiler[0], cmakeCXXCompiler[1])
    options.setDefine(cmakeCompilers[0], cmakeCompilers[1])

def setJobSlotsDefines(options, jobSlots):
    options.setDefine(mdJobSlots[0], jobSlots)
    options.setDefine(makeJobSlots[0], makeJobSlots[1])

def setPrefixDefines(options, prefix):
    options.setDefine(mdPrefix[0], prefix)
    options.setDefine(autoToolsPrefix[0], autoToolsPrefix[1])
    options.setDefine(cmakePrefix[0], cmakePrefix[1])

