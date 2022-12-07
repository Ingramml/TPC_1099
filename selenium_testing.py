from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request
import shutil
import os


target_location='/Volumes/SSD/TPC990'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

html_doc=driver.get("https://projects.propublica.org/nonprofits/organizations/920132239")

xmls=driver.find_elements(By.PARTIAL_LINK_TEXT,"990")

for xml in xmls:
    link = xml.get_attribute('href')
    #print(link)
    equallocator=link.find('=')
    filename=link[equallocator+1:] #pulls file number
    #print(os.path.join(target_location,filename+'.xml'))
    if link.find('xml')!= -1 and os.path.exists(os.path.join(target_location,filename+'.xml')) == False:
        #print(os.path.join(target_location, filename + '.xml'))
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.'}
        request1 = urllib.request.Request(link, headers=headers)
        response = urllib.request.urlopen(request1)
        with open(os.path.join(target_location,filename+".xml"), 'wb') as outfile:
            shutil.copyfileobj(response, outfile)
    else:
        print('not xml file')
    WebDriverWait(driver, timeout=10000)


driver.quit()
print('files done')