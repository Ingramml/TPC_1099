import pandas as pd
import glob
import os
import urllib.request
import json
json_files = glob.glob('/Users/michaelingram/Documents/index_*.json')
json_file = "/Users/michaelingram/Documents/index_2012.json"
# jf = open(json_file)
# data = json.load(jf)
df = pd.read_json(json_file)
#df = pd.json_normalize(data['Filings2012'])
#print(df)
for x in json_files:
    Filiingsdata = os.path.basename(x)
    Filings='Filings'+Filiingsdata[6:10]
    jf=open(x)
    print(Filings)
    data= json.load(jf)
    df = pd.json_normalize(data[str(Filings)])
    df.to_csv('/Users/michaelingram/Documents/'+str(Filings)+'dictionary.csv')


