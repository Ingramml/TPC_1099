import zipfile
import glob
import os
import time
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
all_file = glob.glob('/Volumes/Storage/TPC990/EIN_giving/*/*.csv')
li = []
print
'''
for filename in all_file:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv( '/Users/michaelingram/Downloads/regioncombines.csv', index=False)
'''