# -*- coding: utf-8 -*-
# about.py
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
from sys import version_info

# The actual Text is in the ui file
class AboutDialog (Qt.QDialog, Ui_Dialog):
    def __init__(self, parent, version):
        Qt.QDialog.__init__(self,parent)
        self.setupUi(self)

        text = self.flactagBrowser.toHtml()
        text = text.replace ("[flactag version]", version)
        self.flactagBrowser.setHtml (text)

        text = self.softwareBrowser.toHtml()
        text = text.replace ("[qt version]", Qt.QT_VERSION_STR)
        text = text.replace ("[pyqt version]", QtCore.PYQT_VERSION_STR)
        text = text.replace ("[python version]", "%d.%d.%d-%s" % (version_info[0], version_info[1], version_info[2], version_info[3]))
        self.softwareBrowser.setHtml (text)
