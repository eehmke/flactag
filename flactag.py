#!/usr/bin/python
# -*- coding: utf-8 -*-
# flactag.py
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

import sys
import argparse
from flactag_gui import *
from PyQt4 import Qt
# QtNetwork, sip is not needed directly, but satifies py2exe
from PyQt4 import QtNetwork
import sip
from PyQt4.QtGui import *
from mutagen.flac import FLAC, FLACNoHeaderError
import base64
import help, about, flacfile
from flacfile import FlacFile

# Change history
# 0.0.1 15.01.2015 initial creation
# 0.0.2 16.01.2015 blue light funktion implemented
# 0.0.3 16.01.2015 persistent gui, more info fields (samplerate, length, channel number)
# 0.0.4 17.01.1015 blue/green/yellow/red label to show the hires state of the file
# 0.0.5 18.01.2015 improved coding of special characters in title and artist
# 0.0.6 18.01.2015 improved coding of special characters in filenames, new icons
# 0.0.7 19.01.2015 check for empty title and artist tags
# 0.1.0 20.01.2015 add directory traverse, add and delete pono tags
# 0.1.1 21.01.2015 added check for sample rate for mass apply of pono tags
# 0.1.2

class FlacTagWindow (QtGui.QMainWindow, Ui_MainWindow):
  def __init__(self, parent):
    global args
    super(FlacTagWindow, self).__init__()
    self.setupUi(self)
    
    self.version = "V0.1.2"
    
    homePath = Qt.QDir.homePath()
    rootPath = Qt.QDir.rootPath()
    self.dirModel = Qt.QFileSystemModel (self)
    self.dirModel.setRootPath (rootPath)
    self.dirModel.setFilter (Qt.QDir.NoDotAndDotDot | Qt.QDir.AllDirs)
    self.dirTreeView.setModel (self.dirModel)
    # self.dirTreeView.setRootIndex(self.dirModel.index(rootPath))
    header = self.dirTreeView.header()
    header.hideSection(1)
    header.hideSection(2)
    header.hideSection(3)

    self.dirTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.dirTreeView.customContextMenuRequested.connect(self.dirTreeContextMenuSelected)
    
    self.fileModel = Qt.QFileSystemModel (self)
    self.fileModel.setRootPath (homePath)
    self.fileModel.setFilter (Qt.QDir.NoDotAndDotDot | Qt.QDir.Files)
    self.fileListView.setModel (self.fileModel)
    
    selmodel = self.dirTreeView.selectionModel()
    selmodel.selectionChanged.connect(self.handleDirSelectionChanged)
    
    selmodel = self.fileListView.selectionModel()
    selmodel.selectionChanged.connect(self.handleFileSelectionChanged)

    self.fileListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.fileListView.customContextMenuRequested.connect(self.fileListContextMenuSelected)
    
    self.tableModel = QtGui.QStandardItemModel(0,2,self)
    self.tableModel.setHorizontalHeaderItem(0, QtGui.QStandardItem("Tag"))
    self.tableModel.setHorizontalHeaderItem(1, QtGui.QStandardItem("Value"))
    self.tagListView.setModel (self.tableModel)
    
    self.tableModel.itemChanged.connect (self.handleItemChanged)
    
    self.tagListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tagListView.customContextMenuRequested.connect(self.tagListContextMenuSelected)
    self.tagListView.setSelectionBehavior( QtGui.QAbstractItemView.SelectRows );
    
    self.buttonAdd.clicked.connect (self.buttonAddClicked)
    self.buttonDelete.clicked.connect (self.buttonDeleteClicked)
    self.buttonAddHires.clicked.connect (self.buttonAddHiresClicked)
    
    self.setupActions ()
    
    self.bluePixmap = QtGui.QPixmap(20,20)
    self.bluePixmap.fill(QtGui.QColor("blue"))
    self.greenPixmap = QtGui.QPixmap(20,20)
    self.greenPixmap.fill(QtGui.QColor("green"))
    self.yellowPixmap = QtGui.QPixmap(20,20)
    self.yellowPixmap.fill(QtGui.QColor("yellow"))
    self.redPixmap = QtGui.QPixmap(20,20)
    self.redPixmap.fill(QtGui.QColor("red"))

    setting = Qt.QSettings ("flactag", "flactag")
    setting.beginGroup ('main_window')
    self.restoreGeometry (setting.value("geometry").toByteArray())
    self.centralwidget.restoreGeometry (setting.value("centralwidget").toByteArray())
    self.splitter.restoreState (setting.value("splitter").toByteArray())
    self.splitter_2.restoreState (setting.value("splitter_2").toByteArray())
    self.restoreState(setting.value("windowState").toByteArray());
    self.tagListView.horizontalHeader ().restoreState (setting.value("tagListView").toByteArray())
    setting.endGroup ()

    self.audio = None
    if args.file:
      self.fileInfo = Qt.QFileInfo (args.file)
      fullName = self.fileInfo.filePath ()
      self.audio = FlacFile (fullName)
      self.displayFlacInfo ()
    else:
      self.fileInfo = None
      
  def setupActions (self):
    self.actionOpen_File.triggered.connect(self.openFile)
    self.action_Save.triggered.connect(self.saveFile)
    self.action_Quit.triggered.connect(self.quit)
    self.action_Help.triggered.connect(self.showHelp)
    self.action_About.triggered.connect(self.showAbout)
    
    self.actionOpen_File.setIcon (QtGui.QIcon.fromTheme ("document-open"))
    self.toolBar.addAction (self.actionOpen_File)
    
    self.action_Save.setIcon (QtGui.QIcon.fromTheme ("document-save"))
    self.toolBar.addAction (self.action_Save)
    
    self.action_Quit.setIcon (QtGui.QIcon.fromTheme ("application-exit"))
    self.toolBar.addAction (self.action_Quit)
    
    self.action_Help.setIcon (QtGui.QIcon.fromTheme ("help-contents"))
    self.action_About.setIcon (QtGui.QIcon.fromTheme ("help-about"))
    
  def checkModified (self):
    if self.audio and self.audio.modified and self.fileInfo:
      ret = QtGui.QMessageBox.warning(self, "FLAC Tagger",
                                "The tags of this file have been modified.\n"
                                "%s\n"
                                "Do you want to save your changes?" % self.fileInfo.fileName (),
                                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard
                                | QtGui.QMessageBox.Cancel,
                                QtGui.QMessageBox.Save)
      if ret == QtGui.QMessageBox.Save:
        self.saveFile ()
        return True
      elif ret == QtGui.QMessageBox.Discard:
        return True
      else:
        return False
    return True

  def openFile (self):
    print ("openFile")
    if self.checkModified ():
      fileName = QtGui.QFileDialog.getOpenFileName (self, Qt.QString.fromUtf8("Open FLAC file"))
      if fileName:
        fileName = unicode (fileName)
        self.fileInfo = Qt.QFileInfo (fileName)
        self.audio = FlacFile(fileName)
        self.displayFlacInfo ()
 
  def saveFile (self):
    print ("saveFile")
    self.audio.saveFile()
    
  def quit (self):
    print ("quit")
    setting = Qt.QSettings ("flactag", "flactag")
    setting.beginGroup ('main_window')
    setting.setValue("geometry", self.saveGeometry())
    setting.setValue("centralwidget", self.centralwidget.saveGeometry())
    setting.setValue("splitter", self.splitter.saveState())
    setting.setValue("splitter_2", self.splitter_2.saveState())
    setting.setValue("windowState", self.saveState())
    setting.setValue("tagListView", self.tagListView.horizontalHeader ().saveState())
    setting.endGroup ()
    if self.checkModified ():
      Qt.QApplication.quit()

  @QtCore.pyqtSlot("QItemSelection& QItemSelection&")
  def handleDirSelectionChanged (self, selected, unselected):
    # print ("handleDirSelectionChanged")
    indexes = selected.indexes()
    if indexes:
      index = indexes[0]
      sPath = self.dirModel.fileInfo (index).absoluteFilePath ()
      self.fileListView.setRootIndex (self.fileModel.setRootPath(sPath))

  @QtCore.pyqtSlot("QItemSelection& QItemSelection&")
  def handleFileSelectionChanged (self, selected, unselected):
    # print ("handleFileSelectionChanged")
    indexes = selected.indexes()
    if indexes:
      if self.checkModified ():
        index = indexes[0]
        self.fileInfo = self.fileModel.fileInfo (index)
        fullName = self.fileInfo.filePath ()
        try:
          self.audio = FlacFile (unicode (fullName))
          self.displayFlacInfo ()
        except FLACNoHeaderError:
          pass
      
  def handleItemChanged (self, item):
    print ("handleItemChanged")
    row = item.row ()
    if (row >= 0):
      print (row)
      tag = unicode (self.tableModel.item (row, 0).text())
      value = unicode(self.tableModel.item (row, 1).text())
      # print ("tag: %s:" % tag)
      # print ("value: %s:" % value)
      if tag and value:
        self.audio.setTag (tag, value)
      if self.audio.modified:
        self.displayFlacInfo ()

  @QtCore.pyqtSlot("QPoint")
  def tagListContextMenuSelected (self, point):
    print ("tagListContextMenuSelected")
    index = self.tagListView.indexAt (point).row()
    print (index)
    if index >= 0:
      key = self.tableModel.item (index, 0).text().toUtf8()
      val = self.tableModel.item (index, 1).text().toUtf8()
      print (key)
      print (val)

  @QtCore.pyqtSlot("QPoint")
  def dirTreeContextMenuSelected (self, point):
    print ("dirTreeContextMenuSelected")
    index = self.dirTreeView.indexAt (point)
    if self.dirModel.isDir (index):
      info = self.dirModel.fileInfo (index)
      path = info.absoluteFilePath ()
      print (unicode (path))
       
      menu = QMenu(self)
      ##to show the menu title; works but the menu is not closed at exit
      #menu.setWindowFlags(QtCore.Qt.Tool)
      #menu.setWindowTitle (path)
      actionTraverseDirSetPono = QAction("&Set Pono tags in this directory", self)
      actionTraverseDirResetPono = QAction("&Reset Pono tags in this directory", self)
      menu.addAction(actionTraverseDirSetPono)
      menu.addAction(actionTraverseDirResetPono)
      menu.popup(self.dirTreeView.viewport().mapToGlobal(point))
      actionTraverseDirSetPono.triggered.connect (lambda: self.traverseDirSetPono(path))
      actionTraverseDirResetPono.triggered.connect (lambda: self.traverseDirResetPono(path))

  @QtCore.pyqtSlot("QPoint")
  def fileListContextMenuSelected (self, point):
    print ("fileListContextMenuSelected")
    index = self.fileListView.indexAt (point).row()
    print (index)

  def buttonAddClicked (self):
    print ("buttonAddClicked")
    self.tableModel.appendRow ([QtGui.QStandardItem (""), QtGui.QStandardItem ("")])
    # tag names must be lowercase
    newName = 'newentry'
    counter = 0      
    while newName in self.audio.keys():
      newName = "newentry%d" % counter
      print ("newName: %s" % newName)
      counter += 1
    self.audio.setTag (newName, '???')
    self.displayFlacInfo ()
    
  def buttonDeleteClicked (self):
    print ("buttonDeleteClicked")
    select = self.tagListView.selectionModel()
    if select.hasSelection():
      row = select.selectedRows()[0].row()
      print (row)
      tag = unicode (self.tableModel.item (row, 0).text())
      self.audio.deleteTag (tag)
      self.displayFlacInfo ()

  def traverseDirSetPono (self, path):
    result = QtGui.QMessageBox.warning(self, "FLAC Tagger",
                                "phc and release_guid tags will be added to all hires flac files "
                                "in this directory and its subdirectories.\n"
                                "Are yoo sure?",
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                QtGui.QMessageBox.No)
    if result == QtGui.QMessageBox.Yes:
      self.counter = 0
      self.doTraverseDirSetPono (path)
      QtGui.QMessageBox.information(self, "FLAC Tagger",
                                "%d files have been modified.\n"
                                "phc and release_guid tags have been added." % self.counter,
                                QtGui.QMessageBox.Ok)
    
  def doTraverseDirSetPono (self, path):
    print ("traverseDirSetPono: %s" % path)
    dir = Qt.QDir (path)
    list = dir.entryInfoList()
    for iList in range (len(list)):
      info = list[iList]
      sFilePath = info.filePath()
      if info.isDir():
        # recursive
        if info.fileName() != ".." and info.fileName() != ".":
          self.doTraverseDirSetPono (sFilePath)
      else:
        print ("file: %s" % sFilePath)
        try:
          audio = FlacFile (unicode (sFilePath))
          isPono, key, release_guid = audio.thisIsPono ()
          if isPono:
            print ('is pono')
          else:
            print ('is not pono')
            if audio.info.sample_rate > 44100:
              audio.encrypt (key, release_guid)
              audio.saveFile ()
              self.counter += 1
        except FLACNoHeaderError:
          print ('is no flac file')
          
  def traverseDirResetPono (self, path):
    result = QtGui.QMessageBox.warning(self, "FLAC Tagger",
                                "phc and release_guid tags will be deleted from all flac files "
                                "in this directory and its subdirectories.\n"
                                "Are yoo sure?",
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                QtGui.QMessageBox.No)
    if result == QtGui.QMessageBox.Yes:
      self.counter = 0
      self.doTraverseDirResetPono (path)
      QtGui.QMessageBox.information(self, "FLAC Tagger",
                                "%d files have been modified.\n"
                                "phc and release_guid tags have been deleted." % self.counter,
                                QtGui.QMessageBox.Ok)

  def doTraverseDirResetPono (self, path):
    print ("traverseDirSetPono: %s" % path)
    dir = Qt.QDir (path)
    list = dir.entryInfoList()
    for iList in range (len(list)):
      info = list[iList]
      sFilePath = info.filePath()
      if info.isDir():
        # recursive
        if info.fileName() != ".." and info.fileName() != ".":
          self.doTraverseDirResetPono (sFilePath)
      else:
        print ("file: %s" % sFilePath)
        try:
          audio = FlacFile (unicode (sFilePath))
          isPono, key, release_guid = audio.thisIsPono ()
          if isPono:
            print ('is pono')
            audio.deleteTag ('phc')
            audio.deleteTag ('release_guid')
            audio.saveFile ()
            self.counter += 1
          else:
            print ('is not pono')
        except FLACNoHeaderError:
          print ('is no flac file')
      
  def checkTitleArtist (self):
    print ("checkTitleArtist")
    
    if not 'artist' in self.audio.keys() or not self.audio ['artist']:  
      self.audio.setTag ('artist', 'unkown artist')
      QtGui.QMessageBox.warning(self, "FLAC Tagger",
                                "This file does not contain valid artist information.\n"
                                "A tag \"unknown artist\" has been added.",
                                QtGui.QMessageBox.Ok)
    
    if not 'title' in self.audio.keys() or not self.audio ['title']:  
      self.audio.setTag ('title', 'unkown title')
      QtGui.QMessageBox.warning(self, "FLAC Tagger",
                                "This file does not contain valid title information.\n"
                                "A tag \"unknown title\" has been added.",
                                QtGui.QMessageBox.Ok)

  def buttonAddHiresClicked (self):
    print ("buttonAddHiresClicked")

    self.checkTitleArtist ()
    doit = False
    isPono, key, release_guid = self.audio.thisIsPono ()
    if isPono:
      ret = QtGui.QMessageBox.warning(self, "FLAC Tagger",
                                "This file already contains valid HiRes tags.\n"
                                "Do you want to replace it?",
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                QtGui.QMessageBox.No)
      if ret == QtGui.QMessageBox.Yes:
        doit = True
    else:
      doit = True
      
    if doit:
      self.audio.encrypt (key, release_guid)
    if self.audio.modified:
      self.displayFlacInfo ()

  def setColorLabel (self):
    isPono, key, release_guid = self.audio.thisIsPono ()
    print ("isPono: %d" % isPono)
    if self.audio.info.sample_rate > 44100:
      if isPono:
        self.colorLabel.setPixmap (self.bluePixmap)
      else:
        self.colorLabel.setPixmap (self.greenPixmap)
    else:
      if isPono:
        self.colorLabel.setPixmap (self.redPixmap)
      else:
        self.colorLabel.setPixmap (self.yellowPixmap)

  def displayFlacInfo (self):
    name = self.fileInfo.fileName ()
    #print ("name: %s" % name)
    self.fileNameEdit.setText (name)
      
    # save the state to be restored after resetting the header
    state = self.tagListView.horizontalHeader ().saveState ()
    self.tableModel.clear ()
    self.tableModel.setHorizontalHeaderItem(0, QtGui.QStandardItem("Tag"))
    self.tableModel.setHorizontalHeaderItem(1, QtGui.QStandardItem("Value"))
    self.tagListView.horizontalHeader ().restoreState (state)
      
    self.sampleRateLabel.setText ("Sample rate: %d Hz" % self.audio.info.sample_rate)
    self.lengthLabel.setText ("Length: %d:%02d" % (self.audio.info.length/60,  self.audio.info.length%60))
    self.channelsLabel.setText ("Channels: %d" % self.audio.info.channels)
    for key in self.audio:
      # print ("tag: %s; value: %s" % (key, audio[key]))
      tag = QtGui.QStandardItem (Qt.QString (key.encode()))
      value = QtGui.QStandardItem (Qt.QString (self.audio[key][0]))
      self.tableModel.appendRow ([tag, value])
    self.setColorLabel ()

  def showHelp (self):
    dialog = help.HelpDialog (self)
    dialog.show()

  def showAbout (self):
    dialog = about.AboutDialog (self, self.version)
    dialog.show()
  
# Hauptprogramm
# Starte die Applikation und zeige das Hauptfenster
def main():
  global args
  
  #print ("Version: %s" % Qt.QT_VERSION_STR)
  #print ("File: %s" % args.file)
    
  app = QtGui.QApplication(sys.argv)

  w = FlacTagWindow(None)
  # app.setStyle (QtGui.QStyleFactory.create("plastique"))
  
  w.show()

  sys.exit(app.exec_())


if __name__ == '__main__':
  global args
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', dest='verbose', action='store_true')
  parser.add_argument('-p', dest='profile', action='store_true')
  parser.add_argument('-f', dest='file', action='store')
  args = parser.parse_args()
  # print (args)
  
  main()
