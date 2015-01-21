# flactag
The FLAC Tagger flactag aims to work as a tag editor for FLAC audio files and supports the Pono specific tags

Use at your own risk!
Be sure to have backup copies of your files. Only work on the copy.
You have been warned. If you loose any files or damage your Pono, the author will not be responsible for the loss.
 
This being said, the program seems to do it's job and has caused no harm on my system. 
Please test it and report your experiences to me. 
Error reports or feature suggestions are welcome.
 
Flactag can be used to check, modify or delete the tags in a FLAC file. 
It has been written with the Pono specific enhancements in mind, but is not restricted to them. 
In this sense it is aimed to grow into a full featured tag editor. However, it does not check 
the validity of entered tags. It allows to delete or modify of existing tags that may be important. 
It allows to add tags that may have no meaning.
 
The Pono specific tags are phc and release_guid. It is not checked if the file is actually 
a high resolution file. If you apply these tags to FLAC files that you ripped from CD, it
will nevertheless switch the blue light on. If you don't want to light the blue led, 
flactag can be used to delete these tags.
 
A color icon will appear to indicate the hires state. For lowres files (44100 Hz) the color 
is yellow, if it contains valid phc tag then red. Hires files with no valid phc tag are 
marked green, a valid phc tag is marked blue.
 
To add these tags to a FLAC file, press the Button „Add Hires Tags“. 
If there is no release_guid tag, it will be created as a random string. 
If there is already one release_guid tag, it will be used. 
If the calculation of the key results is a valid Pono signature, a warning will be displayed. 
If all checks are done, the phc tag will be calculated and added to the list of tags.
 
The actual file will not be written until the user selects „Save File“ from the File menu. 
If the file has been modified and a new file is opened, or if the program is about to close, 
a warning will be displayed.
 
To add or remove hires tags to a complete directory tree, select that directory and select 
the context menu by pressing the right mouse button. Select „Set Pono tags in this directory“ 
or „Reset Pono tags in this directory“. The action will be applied for all files in that directory 
and its subdirectory. Only files that have a sample rate above 44100 Hz are modified.
 
Have fun and enjoy the blue light
