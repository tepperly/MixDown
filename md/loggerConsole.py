# Copyright (c) 2010-2013, Lawrence Livermore National Security, LLC
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

import sys
import logger

class LoggerConsole(logger.LoggerBase):
    def close(self):
        pass

    def __formatErrorMessage(self, message, filePath="", lineNumber=0):
        if filePath == "" and lineNumber == 0:
            return "Error: %s\n" % (message)
        elif lineNumber == 0:
            return "Error: %s: %s\n" % (filePath, message)
        else:
            return "Error: %s (line %d): %s\n" % (filePath, lineNumber, message)

    def __formatMessagePrefix(self, targetName="", targetStep=""):
        if targetName == "" and targetStep == "":
            return ""
        if targetName != "" and targetStep != "":
            return "%s: %s: " % (targetName, targetStep.capitalize())
        elif targetStep == "":
            return "%s: " % (targetName)
        return ""

    def writeMessage(self, message, targetName="", targetStep="", forceStdOut=False):
        message = self.__formatMessagePrefix(targetName, targetStep) + message + "\n"
        self._writeStdOut(message)

    def writeError(self, message, targetName="", targetStep="", filePath="", lineNumber=0, exitProgram=False):
        message = self.__formatErrorMessage(self.__formatMessagePrefix(targetName, targetStep) + message , filePath, lineNumber)
        self._writeStdErr(message)
        if exitProgram:
            sys.exit()

    def reportSkipped(self, targetName="", targetStep="", reason=""):
        message = self.__formatMessagePrefix(targetName, targetStep) + reason + "Skipped.\n"
        self._writeStdOut(message)

    def reportStart(self, targetName="", targetStep=""):
        message = self.__formatMessagePrefix(targetName, targetStep) + "Starting...\n"
        self._writeStdOut(message)

    def reportSuccess(self, targetName="", targetStep="", timeInSeconds=0):
        messagePrefix = self.__formatMessagePrefix(targetName, targetStep)
        message = messagePrefix + "success\n"
        if timeInSeconds != 0:
            message += messagePrefix + "Time " + logger.secondsToHMS(timeInSeconds) + "\n"
        self._writeStdOut(message)

    def reportFailure(self, targetName="", targetStep="", timeInSeconds=0, returnCode=0, exitProgram=False):
        messagePrefix = self.__formatMessagePrefix(targetName, targetStep)
        message = self.__formatErrorMessage(messagePrefix + "Failed with error code " + str(returnCode) + ".")
        if timeInSeconds != 0:
            message += messagePrefix + "Time " + logger.secondsToHMS(timeInSeconds) + "\n"
        self._writeStdErr(message)
        if exitProgram:
            sys.exit()

    def getOutFd(self, targetName="", targetStep=""):
        return sys.stdout

    def getErrorFd(self, targetName="", targetStep=""):
        return sys.stderr
