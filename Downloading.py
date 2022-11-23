import glob
from tqdm import tqdm
import pandas as pd
import requests
import os
import time
#downloads all files from Amazon Json 990s
count = 0
created = 0
start_time = time.time()
csv_files = glob.glob('/Users/michaelingram/Documents/Filings*dictionary.csv')
print('start at ' + time.ctime(start_time))
for x in csv_files:
    df = pd.read_csv(x)
    # df = pd.read_csv('/Users/michaelingram/Documents/Filings2011dictionary.csv')
    ObjectId = str(df['ObjectId'][0])
    # print(ObjectId)
    foldername = ObjectId[0:4] + '_amazon_XML'
    df2 = df[df['FormType'] == '990']
    urlcolumn = df2['URL']
    print('')
    print(x)
    print(time.ctime())
    print(foldername)
    for z in tqdm(urlcolumn):
        file_location = os.path.join('/Volumes/Storage/TPC990', foldername)
        y = z.strip('https://s3.amazonaws.com/irs-form-990/')
        if os.path.isfile(file_location + '/' + y):
            pass
        else:

            response = requests.get(z)
            os.makedirs(file_location, exist_ok=True)
            with open(str(file_location + '/' + y), 'wb') as file:
                file.write(response.content)
            response.close()
            #time.sleep(.5)
end_time = time.time()
print('total time is ' + str(end_time - start_time) + ' seconds')
