
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request
import shutil
import os
import pandas as pd
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#Searches for non-profits with name from search ter
#df=pd.read_csv("/Volumes/SSD/TPC990/WOMAN'S MEDICAL_combined.csv")
"""
eins = ['ein']
for ein in eins:
"""
ein = '721068329'
target_location='/Volumes/SSD/TPC990/TPC_xml'

html_doc=driver.get("https://projects.propublica.org/nonprofits/organizations/"+ein)

xmls=driver.find_elements(By.PARTIAL_LINK_TEXT,"990")
exisitnfiles=0
nonxmlfiles=0
filesdownloaded=0
print(len(xmls))
for xml in xmls:
    link = xml.get_attribute('href')
    #print(link)
    equallocator=link.find('=')
    filename=link[equallocator+1:] #pulls file number
    #  WebDriverWait(driver, timeout=10)
    if link.find('xml')!= -1:
        if os.path.exists(os.path.join(target_location,filename+'_public.xml')) == False:
            #print(os.path.join(target_location, filename + '.xml'))
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.'}
            request1 = urllib.request.Request(link, headers=headers)
            response = urllib.request.urlopen(request1)
            with open(os.path.join(target_location,filename+"_public.xml"), 'wb') as outfile:
                shutil.copyfileobj(response, outfile)
            filesdownloaded=filesdownloaded+1
        else:
            exisitnfiles = exisitnfiles+1
    else:
        nonxmlfiles = nonxmlfiles+1
driver.quit()
print(str(ein)+" searched")
print('files downloaded ' + str(filesdownloaded))
print('number of existing files ' + str(exisitnfiles))
print('non xml files ' + str(nonxmlfiles))