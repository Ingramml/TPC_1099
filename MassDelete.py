import glob
import os
import regex

keyword =''
files = glob.glob("/Volumes/SSD/production/*/*.csv")
for x in files:
    if os.path.exists(x):
        os.remove(x)
    else:
        #print('No file found')
        pass
