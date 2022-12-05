import glob
import pandas as pd
import os
from tqdm import tqdm

#Location of folders that contain files
all_folders = glob.glob('/Volumes/SSD/TPC990/Amazon990_2_csv/*')
dir_name = os.path.dirname((all_folders[1]))
print(dir_name)

outPutPath = '/Volumes/SSD/TPC990/Amazon990_2_csv'
fileprefix='profile'
folder_name=os.path.basename(dir_name)
print(folder_name)

li = []
for folders in tqdm(all_folders):
    files = glob.glob(folders + '/'+fileprefix+'*.csv')
    # print(folders)
    file_suffix = os.path.basename(folders)
    df = pd.DataFrame()
    li=[]
    for file in files:
        #print(file)
        df = pd.read_csv(file, index_col=None, header=0, low_memory=False,dtype="object")
        df = df.astype('object')
        if df.empty == True:
            os.remove(file)
        else:
            li.append(df)
    if len(li) != 0:
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.to_csv(dir_name+ '/' + file_suffix[-4:] + '_' +folder_name + '_' + fileprefix+'_combined.csv', index=False)

print('all files concated')
