#!/usr/bin/python
# -*- encoding: utf-8 -*-

#To install acoustid lib execute: pip install pyacoustid
import acoustid as fp
import os
import sys
import shutil
import argparse

parser = argparse.ArgumentParser(prog="duplicatemp3", description="DuplicateMP3 verification script")

#Format: filename: finger_print
DB = {}
move_dup_files = False

diff_name_id = 1

parser.add_argument("dir", metavar="dir", type=str,
    help="The directory of musics")
parser.add_argument("move_to", metavar="move_to", type=str,
    help="The directory destination of duplicated music")
parser.add_argument("-v","--verbose", action="store_true",
    help="Show messages")

args = parser.parse_args()

INI_PATH = args.dir
MOVE_TO = args.move_to

if not INI_PATH or not MOVE_TO:
    print "You must specify the directories"
    exit(-1)

if not os.path.isdir(INI_PATH):
    print "The directory of musics does not existis"
    exit(-2)

if not os.path.isdir(MOVE_TO):
    print "Creating destination directory"
    try:
        os.makedirs(MOVE_TO)
    except Exception, e:
        print "An error ocoured when creating %s directory" % MOVE_TO
        print e.msgerror
        exit(-2)


print "Verifying the music files, it may take a long time..."
try:
    for root, dirs, files in os.walk(INI_PATH):
        for name in files:
            if name[-3:] in ("mp3","wav","aac"):
                mp3 = os.path.join(root,name)
                finger = fp.fingerprint_file(mp3)[1]
                if finger in DB.keys():
                    #Duplicated file
                    if parser.verbose:
                        print "# %s \n--> %s\n" % (
                            DB[finger],
                            mp3
                        )
                    if move_dup_files:
                        try:
                            shutil.move(mp3, MOVE_TO)
                        except shutil.Error as e:
                            on = os.path.join(MOVE_TO, name)
                            nn = os.path.join(MOVE_TO, name + "_%d" % diff_name_id)
                            shutil.move(on, nn)
                            diff_name_id+=1
                            shutil.move(mp3, MOVE_TO)

                else:
                    DB[finger] = mp3
except KeyboardInterrupt:
    print "Operation canceled"
else:    
    print "Done!"
