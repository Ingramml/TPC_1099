import json
import requests
import selenium
import pandas as pd
import os

#Searches for non-profits with name from search term and exports file
searchterm = 'PREGNANCY CENTER'
target_location='/Volumes/SSD/TPC990/'
x = requests.get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm)
x=x.json()
page_num=x["num_pages"]
print(page_num)
z=0
li=[]
while z<page_num:
    temprequest='https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm+'&?cur_page='+str(z)
    newrequest=temprequest.replace(' ','%20')
    x = requests.get(newrequest)
    x=x.json()
    x=x['organizations']
    df = pd.DataFrame.from_dict(x)
    #df = pd.read_csv(df2, index_col=None, header=0, low_memory=False, dtype="object")
    li.append(df)
    #print(li)
    frame = pd.concat(li, axis=0, ignore_index=True)
    z = z + 1
frame.to_csv(os.path.join(target_location,searchterm)+'_combined.csv', index=False)
print(frame['ein'])


