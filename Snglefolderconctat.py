import glob
import pandas as pd
import os
from tqdm import tqdm
keyword = 'income_expenses'
files = glob.glob('/Volumes/SSD/production/*'+keyword+'*.csv')
print(files)
dir_name = os.path.dirname(files[1])
dir_name2 = os.path.dirname(dir_name)

folder_name = os.path.basename(dir_name2)

li = []
for file in tqdm(files):
    df = pd.read_csv(file, index_col=None, header=0, low_memory=False, dtype="object")
    df.columns = map(str.lower, df.columns)
    if df.empty:
        os.remove(file)
    else:
        li.append(df)

if len(li) != 0:
    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(dir_name + '/' + keyword + '_all_combined.csv', index=False)

print(keyword+' all files concatenated')

