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
#  You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import distutils, os, tarfile, urllib, zipfile
import git, hg, logger, svn, utilityFunctions

def fetch(pythonCallInfo):
    outfd = logger.getOutFd(pythonCallInfo.target.name, "fetch")
    if git.isGitRepo(pythonCallInfo.target.path):
        if not git.gitCheckout(pythonCallInfo.target.path, pythonCallInfo.target.outputPath):
            pythonCallInfo.logger.writeError("Given Git repo '" + pythonCallInfo.target.path +"' was unable to be checked out")
            pythonCallInfo.success = False
        else:
            pythonCallInfo.target.path = pythonCallInfo.target.outputPath
            pythonCallInfo.success = True
    elif hg.isHgRepo(pythonCallInfo.target.path):
        if not hg.hgCheckout(pythonCallInfo.target.path, pythonCallInfo.target.outputPath):
            pythonCallInfo.logger.writeError("Given Hg repo '" + pythonCallInfo.target.path +"' was unable to be checked out")
            pythonCallInfo.success = False
        else:
            pythonCallInfo.target.path = pythonCallInfo.target.outputPath
            pythonCallInfo.success = True
    elif svn.isSvnRepo(pythonCallInfo.target.path):
        if not svn.svnCheckout(pythonCallInfo.target.path, pythonCallInfo.target.outputPath, outfd):
            pythonCallInfo.logger.writeError("Given Svn repo '" + pythonCallInfo.target.path +"' was unable to be checked out")
            pythonCallInfo.success = False
        else:
            pythonCallInfo.target.path = pythonCallInfo.target.outputPath
            pythonCallInfo.success = True
    elif utilityFunctions.isURL(pythonCallInfo.target.path):
        filenamePath = os.path.join(pythonCallInfo.options.downloadDir, utilityFunctions.URLToFilename(pythonCallInfo.target.path))
        if not os.path.exists(pythonCallInfo.options.downloadDir):
            os.mkdir(pythonCallInfo.options.downloadDir)
        urllib.urlretrieve(pythonCallInfo.target.path, filenamePath)
        pythonCallInfo.target.path = filenamePath
        pythonCallInfo.success = True
    elif os.path.isdir(pythonCallInfo.target.path):
        if pythonCallInfo.target.outputPathSpecified and \
           os.path.abspath(pythonCallInfo.target.path) != os.path.abspath(pythonCallInfo.target.outputPath):
            distutils.dir_util.copy_tree(pythonCallInfo.target.path, pythonCallInfo.target.outputPath)
            pythonCallInfo.target.path = pythonCallInfo.target.outputPath
        pythonCallInfo.success = True
    elif os.path.isfile(pythonCallInfo.target.path):
        pythonCallInfo.success = True

    return pythonCallInfo

def unpack(pythonCallInfo):
    if os.path.isfile(pythonCallInfo.target.path):
        if not utilityFunctions.validateCompressedFile(pythonCallInfo.target.path):
            pythonCallInfo.success = False
        else:
            if tarfile.is_tarfile(pythonCallInfo.target.path):
                utilityFunctions.untar(pythonCallInfo.target.path, pythonCallInfo.target.outputPath, True)
                pythonCallInfo.target.path = pythonCallInfo.target.outputPath
                pythonCallInfo.success = True
            elif zipfile.is_zipfile(pythonCallInfo.target.path):
                utilityFunctions.unzip(pythonCallInfo.target.path, pythonCallInfo.target.outputPath, True)
                pythonCallInfo.target.path = pythonCallInfo.target.outputPath
                pythonCallInfo.success = True
    elif os.path.isdir(pythonCallInfo.target.path):
        pythonCallInfo.success = True
    else:
        pythonCallInfo.logger.writeError("Given path '" + pythonCallInfo.target.path + "' not understood by MixDown's unpack (path should be a file or a directory at this point)")
        pythonCallInfo.success = False

    return pythonCallInfo

