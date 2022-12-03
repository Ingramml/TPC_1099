import requests
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request
import shutil
import os

#Searches for non profits with name from search term
searchterm = 'Women Health'


x = requests.get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm)
x=x.json()
x=x['organizations']
df=pd.DataFrame.from_dict(x)
url = 'https://projects.propublica.org/nonprofits/organizations/'
y=0
for i in df['ein']:
    print(y)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    html_doc = driver.get(url+str(i))
    xmls = driver.find_elements(By.PARTIAL_LINK_TEXT, "990")
    targetlocation='/Volumes/SSD/TPC990/Amazon_XMLs/download990mxls/'
    for xml in xmls:
        link = xml.get_attribute('href')
        #print(link)
        equallocator = link.find('=')
        filename = link[equallocator + 1:]  # pulls file number
        WebDriverWait(driver, timeout=50)
        if os.path.exists(targetlocation + filename + "TPC_public.xml"):
            pass
        else:
            if link.find('xml') != -1:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.'}
                request1 = urllib.request.Request(link, headers=headers)
                response = urllib.request.urlopen(request1)
                with open(targetlocation + filename + "TPC_public.xml", 'wb') as outfile:
                    shutil.copyfileobj(response, outfile)
            else:
                pass

    y=y+1
    WebDriverWait(driver, timeout=50)

driver.quit()