import glob
import pandas as pd
import os
from tqdm import tqdm

files = glob.glob('/Volumes/SSD/TPC990/incomeexpense/2000/*')

dir_name = os.path.dirname(files[1])
dir_name2=os.path.dirname(dir_name)

folder_name=os.path.basename(dir_name2)

li = []
for file in files:
    df = pd.read_csv(file, index_col=None, header=0, low_memory=False)
    print(df.dtypes)
    df['zipcode']=df['zipcode'].astype('object')
    print(df.dtypes)
    if df.empty == True:
        os.remove(file)
    else:
        li.append(df)
if len(li) != 0:
    frame = pd.concat(li, axis=0, ignore_index=True)
    #frame.to_csv(dir_name + '/' + file_suffix[-4:] + '_990_'+folder_name+'_combined.csv', index=False)

print('all files concated')