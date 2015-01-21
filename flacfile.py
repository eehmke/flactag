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
  
  def __init__(self, name):
    try:
      super(FlacFile,self).__init__(name)
      self.modified = False
    except FLACNoHeaderError:
      raise
    
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
    print ("thisIsPono")

    if 'release_guid' in self.keys():
      release_guid = self['release_guid'][0]
    else:
      release_guid = os.urandom(16).encode('hex')
    if not 'phc' in self.keys ():
      phc = ''
    else:
      phc = self['phc'][0]
    title = self['title'][0]
    artist = self['artist'][0]
    print (release_guid, title, artist)
    
    combined = release_guid + title + artist
    print ("combined: %s; len: %d" % (combined, len(combined)))
    m = hashlib.md5(combined.encode('utf8'))
    key = m.hexdigest()
    print ("key: %s; len: %d" % (key, len(key)))
    dec = decrypt (key, phc)
    print ("decrypted: %s" % dec)
    if dec.startswith ('thisispono'):
      return True, key, release_guid
    else:
      return False, key, release_guid
    
  def encrypt (self, key, release_guid):
    print ("encrypt")
    phc = encrypt (key, 'thisispono_000000000000000000000').encode("hex")
    self.setTag ('phc', phc)
    self.setTag ('release_guid', release_guid)

  def saveFile (self):
    print ("saveFile")
    self.modified = False
    self.save ()
    