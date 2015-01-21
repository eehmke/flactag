# -*- coding: utf-8 -*-
# help.py
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

from help_gui import *
from PyQt4 import Qt

# Zeige den Hilfetext. Dies ist eine HTML-Datei, die von OpenOffice exportiert wurde
# Sie kann aktive Links enthalten, darum verwenden wir die QWebView Klasse als Browser
class HelpDialog (Qt.QDialog, Ui_Dialog):
    def __init__(self, parent):
        Qt.QDialog.__init__(self,parent)
        self.setupUi(self)

        #self.webView.loadFinished.connect(self.slotLoadFinished)
        #self.webView.loadStarted.connect(self.slotLoadStarted)
        
        #print "loading file..."
        url = Qt.QUrl.fromLocalFile(Qt.QDir.current().absolutePath() + '/help.html')
        self.webView.load (url)
        self.webView.show()

    #def slotLoadStarted (self):
    #    print ("slotLoadStarted")

    #def slotLoadFinished (self, ok):
    #    print ("slotLoadFinished: %d" % ok)
        