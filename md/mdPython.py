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

import os, re, sys

from md import mdSteps

from mdLogger import *

def parsePythonCommand(command):
    remaining = command.strip()
    isPythonCommand = False
    namespace = ""
    function = ""

    if not remaining.endswith("(pythonCallInfo)") or remaining.find(" ") != -1:
        return False, "", ""

    i = 0
    while i < len(remaining):
        if remaining[i] == ".":
            namespace = remaining[:i]
            remaining = remaining[i+1:]
            break
        i += 1
    i = 0
    while i < len(remaining):
        if remaining[i] == "(":
            function = remaining[:i]
            remaining = remaining[i+1:]
            break
        i += 1
    i = 0

    if namespace != "" and function != "":
        isPythonCommand = True

    return isPythonCommand, namespace, function

def callPythonCommand(namespace, function, target, options):
    filename = namespace + ".py"
    if not namespace == "mdSteps" and not os.path.exists(filename):
        Logger().writeError("Expected python file, " + filename + ", not found")
        return False
    else:
        if os.path.isdir(filename):
            Logger().writeError("Expected python file, " + filename + ", found directory")
            return False
        if not "." in sys.path:
            sys.path.append(".")
        sys.path.append("md")
        importedNamespace = __import__(namespace)

    try:
        target.pythonCallInfo.success = False
        target.pythonCallInfo.currentPath = target.path
        target.pythonCallInfo.outputPath = target.outputPath
        target.pythonCallInfo.outputPathSpecified = target.outputPathSpecified
        target.pythonCallInfo.downloadDir = options.downloadDir
        pythonCallInfo = getattr(importedNamespace, function)(target.pythonCallInfo)
    except AttributeError as e:
        Logger().writeError(str(e))
        return False

    if not pythonCallInfo.success:
        return False
    target.path = pythonCallInfo.currentPath
    target.outputPath = pythonCallInfo.outputPath
    target.outputPathSpecified = pythonCallInfo.outputPathSpecified
    options.downloadDir = pythonCallInfo.downloadDir
    target.pythonCallInfo = pythonCallInfo
    return True

class PythonCallInfo(object):
    def __init__(self):
        self.success = False
        self.currentPath = ""
        self.outputPath = ""
        self.outputPathSpecified = False
        self.downloadDir = ""
        self.logger = Logger()
