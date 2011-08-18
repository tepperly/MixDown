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

import sys
import logger

class LoggerHtml(logger.LoggerBase):
    def __init__(self, logOutputDir=""):
        self.logOutputDir = logOutputDir
        if self.logOutputDir != "" and not os.path.isdir(self.logOutputDir):
            os.makedirs(self.logOutputDir)

    def close(self):
        pass

    def __FormatErrorMessage(self, message, filePath="", lineNumber=0):
        if filePath == "" and lineNumber == 0:
            return "Error: %s\n" % (message)
        elif lineNumber == 0:
            return "Error: %s: %s\n" % (filePath, message)
        else:
            return "Error: %s (line %d): %s\n" % (filePath, lineNumber, message)

    def writeMessage(self, message):
        self.writeMessage(message, "", "")

    def writeMessage(self, message, targetName="", targetStep=""):
        sys.stderr.flush()
        sys.stdout.write(message)

    def writeError(self, message, targetName="", targetStep="", filePath="", lineNumber=0, exitProgram=False):
        sys.stdout.flush()
        sys.stderr.write(self.__FormatErrorMessage(message, filePath, lineNumber))
        sys.stderr.flush()

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
