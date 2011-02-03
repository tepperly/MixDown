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

import mdBuild, mdCommands, os

from utilityFunctions import *

class Target:
    def __init__(self, targetName, path = ""):
        self.name = targetName
        self.main = False
        self.aliases = []
        self.origPath = path
        self.path = path
        self.output = ""
        self.dependancyDepth = 0
        self.dependsOn = []
        self.skipSteps = []
        self.commands = dict()
        self.commands["preconfig"] = ""
        self.commands["config"] = ""
        self.commands["build"] = ""
        self.commands["install"] = ""
        
    def isValid(self):
        if self.name == "":
            return False
        if self.path == "":
            return False
        return True
    
    def extract(self, outputPath):
        #try svn with "svn ls <path>" exit code 0 = svn, else not svn repo
        return True
        
    def examine(self, options):
        self.__determineCommands(options)
        
    def __determineCommands(self, options):
        for stepName in mdCommands.getBuildStepList():
            self.commands[stepName] = mdCommands.getCommand(stepName, self, options)
    
    def __str__(self):
        retStr = "Name: " + self.name + "\n"
        retStr += "Path: " + self.origPath + "\n"
        if self.main:
            retStr += "Main: True\n"
        if len(self.aliases) != 0:
            retStr += "Aliases: " + ",".join(self.aliases) + "\n"        
        if self.output != "":
            retStr += "Output: " + self.output + "\n"
        if len(self.dependsOn) != 0:
            retStr += "DependsOn: " + ",".join(self.dependsOn) + "\n"        
        if len(self.skipSteps) != 0:
            retStr += "SkipSteps: " + ",".join(self.skipSteps) + "\n"
        for key in self.commands.keys():
            command = self.commands[key]
            if command != "":
                retStr += key.capitalize() + ": " + command + "\n"
        return retStr

    @property
    def skipSteps(self, value):
        loweredList = []
        for step in value[:]:
            loweredList.append(str.lower(step))
        self.skipSteps = loweredList
    
    def hasStep(self, stepName):
        if len(self.skipSteps) == 0: #no steps were specified, do all steps
            return True
        for step in self.skipSteps:
            if step.startswith(stepName):
                return False
        return True