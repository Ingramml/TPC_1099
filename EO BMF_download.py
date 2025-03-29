#downloadd files from IRS website
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request
import shutil
import os
#run monthly

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
html_doc=driver.get("https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf")

csvs=driver.find_elements(By.PARTIAL_LINK_TEXT,"(CSV)")
target_location='/Volumes/SSD/TPC990/EOBMF'
for csv in csvs[0:4]:
    link=csv.get_attribute('href')
    filename=link[-7:]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.'}
    request1 = urllib.request.Request(link, headers=headers)
    response = urllib.request.urlopen(request1)
    with open(os.path.join(target_location,filename), 'wb') as outfile:
        shutil.copyfileobj(response, outfile)
