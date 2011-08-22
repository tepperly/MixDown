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

import os

def secondsToHMS(seconds=0):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

__loggerInstance = None

def Logger():
    if __loggerInstance == None:
        setLogger()
    return __loggerInstance

def setLogger(loggerName="", logOutputDir=""):
    global __loggerInstance
    loggerName = loggerName.lower()
    if loggerName == "file" or loggerName == "":
        import loggerFile
        __loggerInstance = loggerFile.LoggerFile(logOutputDir)
    elif loggerName == "html":
        import loggerHtml
        __loggerInstance = loggerHtml.LoggerHtml(logOutputDir)
    elif loggerName == "console":
        import loggerConsole
        __loggerInstance = loggerConsole.LoggerConsole()
    else:
        import loggerFile
        __loggerInstance = loggerFile.LoggerFile()
        __loggerInstance.writeMessage(loggerName + " logger not found, falling back on file logger")

def close():
    Logger().close()

def writeMessage(message):
    Logger().writeMessage(message)

def writeMessage(message, targetName="", targetStep=""):
    Logger().writeMessage(message, targetName, targetStep)

def writeError(message, targetName="", targetStep="", filePath="", lineNumber=0, exitProgram=False):
    Logger().writeError(message, targetName, targetStep, filePath, lineNumber, exitProgram)

def reportSkipped(targetName="", targetStep="", reason=""):
    Logger().reportSkipped(targetName, targetStep, reason)

def reportStart(targetName="", targetStep=""):
    Logger().reportStart(targetName, targetStep)

def reportSuccess(targetName="", targetStep="", timeInSeconds=0):
    Logger().reportSuccess(targetName, targetStep, timeInSeconds)

def reportFailure(targetName="", targetStep="", timeInSeconds=0, returnCode=0, exitProgram=False):
    Logger().reportFailure(targetName, targetStep, timeInSeconds, returnCode, exitProgram)

def getOutFd(targetName="", targetStep=""):
    return Logger().getOutFd(targetName, targetStep)

def getErrorFd(targetName="", targetStep=""):
    return Logger().getErrorFd(targetName, targetStep)

class LoggerBase(object):
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

    def reportSuccess(self, targetName="", targetStep="", timeInSeconds=0):
        pass

    def reportFailure(self, targetName="", targetStep="", timeInSeconds=0, returnCode=0, exitProgram=False):
        pass

    def getOutFd(self, targetName="", targetStep=""):
        return sys.stdout

    def getErrorFd(self, targetName="", targetStep=""):
        return sys.stderr

