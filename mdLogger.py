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

import os

__loggerInstance = None

def Logger():
    if __loggerInstance == None:
        SetLogger()
    return __loggerInstance

def SetLogger(loggerName="", logOutputDir=""):
    global __loggerInstance
    loggerName = loggerName.lower()
    if loggerName == "file" or loggerName == "":
        import mdLoggerFile
        if logOutputDir != "":
            os.makedirs(logOutputDir)
        __loggerInstance = mdLoggerFile.LoggerFile(logOutputDir)
    elif loggerName == "html":
        import mdLoggerHtml
        if logOutputDir != "":
            os.makedirs(logOutputDir)
        __loggerInstance = mdLoggerHtml.LoggerHtml(logOutputDir)
    elif loggerName == "console":
        import mdLoggerConsole
        __loggerInstance = mdLoggerConsole.LoggerConsole()
    else:
        import mdLoggerFile
        __loggerInstance = mdLoggerFile.LoggerFile()
        __loggerInstance.writeWarning(loggerName + " logger not found, falling back on file logger")

class LoggerBase:
    def close(self):
        pass

    def writeMessage(self, message):
        pass

    def writeMessage(self, message, targetName="", targetStep=""):
        pass

    def writeError(self, message, targetName="", targetStep="", filePath="", lineNumber=0, exitProgram=False):
        pass

    def reportSkipped(self, targetName="", targetStep="", reason=""):
        pass

    def reportStart(self, targetName="", targetStep=""):
        pass

    def reportSuccess(self, targetName="", targetStep=""):
        pass

    def reportFailure(self, targetName="", targetStep="", returnCode=0, exitProgram=False):
        pass

    def getOutFd(self, targetName="", targetStep=""):
        return sys.stdout

    def getErrorFd(self, targetName="", targetStep=""):
        return sys.stderr

