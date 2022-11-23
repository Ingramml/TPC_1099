import requests
import selenium
import pandas as pd
from bs4 import BeautifulSoup

#Searches for non profits with name from search term
searchterm = 'Police'
x = requests.get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm)
x=x.json()
x=x['organizations']
df=pd.DataFrame.from_dict(x)


url = 'https://projects.propublica.org/nonprofits/search'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

print(soup.prettify())






print(r.content)
#print(soup.prettify())




