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

'''
Setup file for installing MixDown
'''
from setuptools import setup

setup(
 name = "mixdown",
 version = "0.1",
 author = "Tom Epperly, Chris White, Lorin Hochstein, Prakashkumar Thiagarajan",
 author_email = "epperly2@llnl.gov, white238@llnl.gov, lorinh@gmail.com, tprak@seas.upenn.edu",
 url = "https://github.com/tepperly/MixDown/",
 packages = ['md'],
 scripts = ['MixDown'],
 description = "Meta-build tool for managing collections of third-party libraries",
)
