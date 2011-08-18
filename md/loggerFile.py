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

import os, sys
import logger

class LoggerFile(logger.LoggerBase):
    def __init__(self, logOutputDir=""):
        self.logOutputDir = logOutputDir
        if self.logOutputDir != "" and not os.path.isdir(self.logOutputDir):
            os.makedirs(self.logOutputDir)
        self.errorFds = dict()
        self.outFds = dict()

    def __formatErrorMessage(self, message, filePath="", lineNumber=0):
        if filePath == "" and lineNumber == 0:
            return "\nError: %s\n" % (message)
        elif lineNumber == 0:
            return "\nError: %s: %s\n" % (filePath, message)
        else:
            return "\nError: %s (line %d): %s\n" % (filePath, lineNumber, message)

    def __formatMessagePrefix(self, targetName="", targetStep=""):
        if targetName == "" and targetStep == "":
            return ""
        if targetName != "" and targetStep != "":
            return "%s: %s: " % (targetName, targetStep.capitalize())
        elif targetStep == "":
            return "%s: " % (targetName)
        return ""

    def close(self):
        for key in self.errorFds.keys():
            self.errorFds[key].close()
        for key in self.outFds.keys():
            self.outFds[key].close()

    def __lookupOutFileName(self, targetName, targetStep):
        return os.path.join(self.logOutputDir, targetName + "_" + targetStep + ".log")

    def __lookupOutFile(self, targetName, targetStep):
        key = str.lower(targetName + targetStep)
        value = self.outFds.get(key)
        if value == None and targetName != "":
            outFileName = self.__lookupOutFileName(targetName, targetStep)
            value = open(outFileName, "w")
            self.outFds[key] = value
        return value

    def writeMessage(self, message, targetName="", targetStep=""):
        sys.stderr.flush()
        if targetName == "":
            sys.stdout.write(message + "\n")
        else:
            self.__lookupOutFile(targetName, targetStep).write(message + "\n")

    def writeError(self, message, targetName="", targetStep="", filePath="", lineNumber=0, exitProgram=False):
        sys.stdout.flush()
        errorMessage = self.__formatErrorMessage(message, filePath, lineNumber)
        if targetName == "":
            sys.stderr.write(errorMessage + "\n")
        else:
            self.__lookupOutFile(targetName, targetStep).write(errorMessage)
            sys.stderr.write(errorMessage)
        sys.stderr.flush()
        if exitProgram:
            sys.exit()

    def reportSkipped(self, targetName="", targetStep="", reason=""):
        messagePrefix = self.__formatMessagePrefix(targetName, targetStep)
        if reason != "":
            message = messagePrefix + reason + ": Skipped.\n"
        else:
            message = messagePrefix + "Skipped.\n"
        sys.stderr.flush()
        sys.stdout.write(message)
        self.__lookupOutFile(targetName, targetStep).write(message)

    def reportStart(self, targetName="", targetStep=""):
        message = self.__formatMessagePrefix(targetName, targetStep) + "Starting...\n"
        sys.stderr.flush()
        sys.stdout.write(message)
        self.__lookupOutFile(targetName, targetStep).write(message)

    def reportSuccess(self, targetName="", targetStep="", timeInSeconds=0):
        messagePrefix = self.__formatMessagePrefix(targetName, targetStep)
        message = messagePrefix + "Succeeded.\n"
        if timeInSeconds != 0:
            message += messagePrefix + "Time " + logger.secondsToHMS(timeInSeconds) + "\n"
        sys.stderr.flush()
        sys.stdout.write(message)
        self.__lookupOutFile(targetName, targetStep).write(message)

    def reportFailure(self, targetName="", targetStep="", timeInSeconds=0, returnCode=0, exitProgram=False):
        messagePrefix = self.__formatMessagePrefix(targetName, targetStep)
        message = ""
        if timeInSeconds != 0:
            message += messagePrefix + "Time " + logger.secondsToHMS(timeInSeconds) + "\n"
        message += self.__formatErrorMessage(messagePrefix + "Failed with error code " + str(returnCode) + ".")
        message += "Look at following log file for failure reason:\n  " + self.__lookupOutFileName(targetName, targetStep)
        message += "\n"
        sys.stdout.flush()
        sys.stderr.write(message)
        self.__lookupOutFile(targetName, targetStep).write(message)
        sys.stderr.flush()
        if exitProgram:
            sys.exit()

    def getOutFd(self, targetName="", targetStep=""):
        if targetName != "" and targetStep != "":
            return self.__lookupOutFile(targetName, targetStep).fileno()
        return sys.stdout

    def getErrorFd(self, targetName="", targetStep=""):
        if targetName != "" and targetStep != "":
            return self.__lookupOutFile(targetName, targetStep).fileno()
        return sys.stderr

