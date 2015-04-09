#!/usr/bin/python
# -*- coding: utf-8 -*-
# flacfile.py
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


import os
from PyQt4 import Qt
from mutagen.flac import FLAC, FLACNoHeaderError
from Crypto.Cipher import AES
import hashlib
from logger import Logger

def decrypt (key, data):
  """
  input in hex encoded string like dd02f9ac30e04649bc10515da9606b91
  """
  if len(key) not in (16, 24, 32):
    raise ValueError("Key must be 16, 24, or 32 bytes")
  if (len(data) % 16) != 0:
    raise ValueError("Message must be a multiple of 16 bytes")
  key = key.decode("hex")
  cipher = AES.new(key, AES.MODE_ECB)
  return cipher.decrypt(data.decode("hex"))

def encrypt (key, data):
  key = key.decode("hex")
  cipher = AES.new(key, AES.MODE_ECB)
  return cipher.encrypt (data)

class FlacFile (FLAC):
  
  def __init__(self, name, logger):
    try:
      super(FlacFile,self).__init__(name)
      self.modified = False
      self.logger = logger
    except FLACNoHeaderError:
      logger ("FLACNoHeaderError %s" % name)
      raise
    except:
      logger ("Unknown FLAC Error % s" % name)
      raise BaseException ("Unknown FLAC Error % s" % name)
    
  def setTag (self ,tag, value):
    self[tag] = value
    self.modified = True
    
  def deleteTag (self, tag):
    try:
      del self[tag]
    except KeyError:
      pass
    self.modified = True
    
  def thisIsPono (self):
    self.logger ("thisIsPono")

    if 'release_guid' in self.keys():
      self.release_guid = self['release_guid'][0]
    else:
      self.release_guid = os.urandom(16).encode('hex')
    if not 'phc' in self.keys ():
      phc = ''
    else:
      phc = self['phc'][0]
    title = self['title'][0]
    artist = self['artist'][0]
    
    combined = self.release_guid + title + artist
    self.logger ("combined: %s; len: %d" % (combined, len(combined)))
    m = hashlib.md5(combined.encode('utf8'))
    self.key = m.hexdigest()
    self.logger ("key: %s; len: %d" % (self.key, len(self.key)))
    dec = decrypt (self.key, phc)
    self.logger ("decrypted: %s" % dec)
    if dec.startswith ('thisispono'):
      return True
    else:
      return False
    
  def addPicture (self,pic):
    self.logger ("addPicture")
    self.add_picture (pic)
    self.modified = True
    
  def encrypt (self):
    self.logger ("encrypt")
    phc = encrypt (self.key, 'thisispono_000000000000000000000').encode("hex")
    self.setTag ('phc', phc)
    self.setTag ('release_guid', self.release_guid)

  def saveFile (self):
    self.logger ("saveFile")
    self.modified = False
    self.save ()
    