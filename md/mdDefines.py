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

import md.mdOptions

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
mdAutoToolsPrefix = "_AutoToolsPrefix", "--prefix=" + surround(mdPrefix[0])

mdAutoToolsCCompiler = "_AutotoolsCCompiler", "CC=" + surround(mdCCompiler[0])
mdAutoToolsCPreProcessor = "_AutotoolsCPreProcessor", "CPP=" + surround(mdCPreProcessor[0])
mdAutoToolsCXXCompiler = "_AutotoolsCXXCompiler", "CXX=" + surround(mdCXXCompiler[0])
mdAutoToolsFCompiler = "_AutotoolsFCompiler", "FC=" + surround(mdFCompiler[0])
mdAutoToolsF77Compiler = "_AutotoolsF77Compiler", "F77=" + surround(mdF77Compiler[0])
mdAutoToolsOBJCCompiler = "_AutotoolsOBJCCompiler", "OBJC=" + surround(mdOBJCCompiler[0])
mdAutoToolsOBJCPreProcessor = "_AutotoolsOBJCPreProcessor", "OBJCPP=" + surround(mdOBJCPreProcessor[0])
mdAutoToolsOBJCXXCompiler = "_AutotoolsOBJCCompiler", "OBJCXX=" + surround(mdOBJCXXCompiler[0])
mdAutoToolsOBJCXXPreProcessor = "_AutotoolsOBJCPreProcessor", "OBJCXXCPP=" + surround(mdOBJCXXPreProcessor[0])

mdAutoToolsCompilers = "_AutoToolsCompilers", surround(mdAutoToolsCCompiler[0]) + " " + surround(mdAutoToolsCXXCompiler[0]) + " " + surround(mdAutoToolsCPreProcessor[0])

#CMake
mdCMakePrefix = "_CMakePrefix", "-DCMAKE_PREFIX_PATH=" + surround(mdPrefix[0]) + " -DCMAKE_INSTALL_PREFIX=" + surround(mdPrefix[0])

mdCMakeCCompiler = "_CMakeCCompiler", "-DCMAKE_C_COMPILER=" + surround(mdCCompiler[0])
mdCMakeCPreProcessor = "_CMakeCPreProcessor", "" #CMake doesn't have a default way to override this
mdCMakeCXXCompiler = "_CMakeCXXCompiler","-DCMAKE_CXX_COMPILER=" + surround(mdCXXCompiler[0])
mdCMakeFCompiler = "_CMakeFCompiler", "-DCMAKE_Fortran_COMPILER=" + surround(mdFCompiler[0])
mdCMakeF77Compiler = "_CMakeF77Compiler", "" #CMake only has one Fortran compiler override
mdCMakeOBJCCompiler = "_CMakeOBJCCompiler", "OBJC=" + surround(mdOBJCCompiler[0])
mdCMakesOBJCPreProcessor = "_CMakeOBJCPreProcessor", "OBJCPP=" + surround(mdOBJCPreProcessor[0])
mdCMakeOBJCXXCompiler = "_CMakeOBJCCompiler", "OBJCXX=" + surround(mdOBJCXXCompiler[0])
mdCMakeOBJCXXPreProcessor = "_CMakeOBJCPreProcessor", "OBJCXXCPP=" + surround(mdOBJCXXPreProcessor[0])

mdCMakeCompilers = "_CMakeCompilers", surround(mdCMakeCCompiler[0]) + " " + surround(mdCMakeCXXCompiler[0])

#GNUMake
mdMakeJobSlots = "_MakeJobSlots", "-j" + surround(mdJobSlots[0])

def setCompilerDefines(options, CCompiler, CXXCompiler, CPreProcessor):
    options.setDefine(mdCCompiler[0], CCompiler)
    options.setDefine(mdCXXCompiler[0], CXXCompiler)
    options.setDefine(mdCPreProcessor[0], CPreProcessor)
    
    options.setDefine(mdAutoToolsCCompiler[0], mdAutoToolsCCompiler[1])
    options.setDefine(mdAutoToolsCXXCompiler[0], mdAutoToolsCXXCompiler[1])
    options.setDefine(mdAutoToolsCPreProcessor[0], mdAutoToolsCPreProcessor[1])
    options.setDefine(mdAutoToolsCompilers[0], mdAutoToolsCompilers[1])

    options.setDefine(mdCMakeCCompiler[0], mdCMakeCCompiler[1])
    options.setDefine(mdCMakeCXXCompiler[0], mdCMakeCXXCompiler[1])
    options.setDefine(mdCMakeCompilers[0], mdCMakeCompilers[1])

def setJobSlotsDefines(options, jobSlots):
    options.setDefine(mdJobSlots[0], jobSlots)
    options.setDefine(mdMakeJobSlots[0], mdMakeJobSlots[1])

def setPrefixDefines(options, prefix):
    options.setDefine(mdPrefix[0], prefix)
    options.setDefine(mdAutoToolsPrefix[0], mdAutoToolsPrefix[1])
    options.setDefine(mdCMakePrefix[0], mdCMakePrefix[1])

