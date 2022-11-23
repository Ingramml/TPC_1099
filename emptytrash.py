#!/usr/local/bin/python
# delete all files and folders in trash box
import os
import sys

os.chdir('/Volumes/Storage/.Trashes')
if len(sys.argv) >= 2:
    if sys.argv[1] == '-t' or sys.argv[1] == '-T':
        os.system("tree ./")
    elif sys.argv[1] == '-l' or sys.argv[1] == '-L':
        os.system("ls -al")
os.system("rm -rf *")