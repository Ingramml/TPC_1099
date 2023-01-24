import requests
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import urllib.request
import shutil
import os
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

#Searches for non profits with name from search term
searchterm = "Woman's Medical"
target_location='/Users/michaellingram/Downloads/xml_test/'


response = requests.get('https://projects.propublica.org/nonprofits/api/v2/search.json?q='+searchterm)
x=response.json()
page_num=x["num_pages"]
z=0
li=[]
df3=pd.DataFrame()

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
url = 'https://projects.propublica.org/nonprofits/organizations/'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
exisitnfiles=0
nonxmlfiles=0
filesdownloaded=0
for i in df3['ein']:
    WebDriverWait(driver, timeout=100)
    html_doc = driver.get(url+str(i))
    xmls = driver.find_elements(By.PARTIAL_LINK_TEXT, "990")
    WebDriverWait(driver, timeout=100)
    for xml in xmls:
        link = xml.get_attribute('href')
        # print(link)
        equallocator = link.find('=')
        filename = link[equallocator + 1:]  # pulls file number
        WebDriverWait(driver, timeout=100)
        if link.find('xml') != -1:
            if os.path.exists(os.path.join(target_location, filename + '_public.xml')) == False:
                # print(os.path.join(target_location, filename + '.xml'))
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.'}
                request1 = urllib.request.Request(link, headers=headers)
                response = urllib.request.urlopen(request1)
                with open(os.path.join(target_location, filename + "_public.xml"), 'wb') as outfile:
                    shutil.copyfileobj(response, outfile)
                filesdownloaded = filesdownloaded + 1
            else:
                exisitnfiles = exisitnfiles + 1
        else:
            nonxmlfiles = nonxmlfiles + 1
    driver.quit()

    print('files dowwnloaded ' + str(filesdownloaded))
    print('number of exising files ' + str(exisitnfiles))
    print('non xml files ' + str(nonxmlfiles))