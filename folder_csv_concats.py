import glob
import pandas as pd
import os
from tqdm import tqdm



#all_folders = glob.glob('/Volumes/SSD/production/*')
#keyword = 'boardmember'
def folder_csv_concat (folder_location,keyword):
    all_folders = glob.glob(folder_location+'/*')
    dir_name = os.path.dirname((all_folders[1]))

    li = []
    for folders in tqdm(all_folders):
        files = glob.glob(folders + '/' + keyword + '*.csv')
        # print(folders)
        file_suffix = os.path.basename(folders)
        df = pd.DataFrame()
        li = []
        for file in files:

            df = pd.read_csv(file, index_col=None, header=0, low_memory=False, dtype="object")
            if df.empty:
                os.remove(file)
            else:
                li.append(df)
        if len(li) != 0:
            frame = pd.concat(li, axis=0, ignore_index=True)
            frame.to_csv(dir_name + '/' + file_suffix[-4:] + keyword+'_combined.csv', index=False)

    print('all files concated')

folder_csv_concat('/Users/michaelingram/Downloads/Tpc','boardmember')
folder_csv_concat('/Users/michaelingram/Downloads/Tpc','profile')
folder_csv_concat('/Users/michaelingram/Downloads/Tpc','income')
folder_csv_concat('/Users/michaelingram/Downloads/Tpc','grants')