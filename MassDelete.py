import glob
import os

files = glob.glob("/Users/michaelingram/PycharmProjects/TPC_1099/*public.xml")
for x in files:
    #print(x)
    os.remove(x)



import os
import sys

os.chdir('/Users/michaelingram/.Trash')
if len(sys.argv) >= 2:
    if sys.argv[1] == '-t' or sys.argv[1] == '-T':
        os.system("tree ./")
    elif sys.argv[1] == '-l' or sys.argv[1] == '-L':
        os.system("ls -al")
else:
    print("Nothing in the bin to delete")
os.system("rm -rf *")
