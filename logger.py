# -*- coding: utf-8 -*-
# logger.py
# This program aims to support tagging of FLAC files
# Copyright (C) 2015  Eggert Ehmke <eggert@eehmke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

from about_gui import *
from PyQt4 import Qt
from PyQt4 import QtCore

# The actual Text is in the ui file
class Logger ():
    def __init__(self, verbose):
      self.verbose = verbose
      
    # the __call__ method can be called directly by the instance
    def __call__ (self, message, verbose = False):
      if verbose or self.verbose:
        print (message)
        