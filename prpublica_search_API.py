import json
import requests
import selenium
import pandas as pd
import os

#Searches for non-profits with name from search term and exports file
searchterm = "center"
target_location='/Volumes/SSD/TPC990/'

response = requests.get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm)

x=response.json()
page_num=x["num_pages"]
print(x)
print(page_num)
z=0
li=[]
df3=pd.DataFrame()
os.makedirs(os.path.join(target_location,searchterm.upper()),exist_ok = True)
new_target_location = target_location+'/'+searchterm.upper()+'/'

while z<page_num:
    temprequest = 'https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm+'&?cur_page='+str(z)
    if temprequest.find(' ')==-1:
        newrequest=temprequest
    else:
        newrequest=temprequest.replace(' ','%20')
    x = requests.get(newrequest)
    x=x.json()
    x=x['organizations']
    df = pd.DataFrame.from_dict(x)
    li.append(df)
    # print(li)
    df3 = pd.concat(li, axis=0, ignore_index=True)
    z = z + 1
    print(z)
    df3.to_csv(os.path.join(new_target_location,searchterm.upper())+'_'+str(z)+'_combined.csv', index=False)



