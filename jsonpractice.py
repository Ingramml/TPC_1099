import json
import pandas as pd


x=('/Users/michaelingram/Downloads/pregnacycnter.json')
import json

# Opening JSON file
x = open(x)
x=json.load(x)
x=x['organizations']
df=pd.DataFrame.from_dict(x)
df.to_csv('/Volumes/SSD/TPC990/testdownload.csv')