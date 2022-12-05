import glob
import pandas as pd
import os
from tqdm import tqdm

#def folderconcat (folder_location,keyword)

all_folders = glob.glob('/Volumes/SSD/production/*')
keyword = 'profile'

dir_name = os.path.dirname((all_folders[1]))
folder_name = os.path.basename(dir_name)

li = []
for folders in tqdm(all_folders):
    files = glob.glob(folders + '/' + keyword + '*.csv')
    # print(folders)
    file_suffix = os.path.basename(folders)
    df = pd.DataFrame()
    li=[]
    for file in files:

        df = pd.read_csv(file, index_col=None, header=0, low_memory=False, dtype="object")
        if df.empty == True:
            os.remove(file)
        else:
            li.append(df)
    if len(li) != 0:
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.to_csv(dir_name + '/' + file_suffix[-4:] + keyword+'_combined.csv', index=False)

print('all files concated')