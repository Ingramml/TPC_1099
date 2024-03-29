import pandas as pd
import os
import glob
import xml.etree.ElementTree as ET
from tqdm import tqdm
#TPC990 testing
files = glob.glob('/Volumes/SSD/TPC990/TPC_xml/*.xml')
dir_name_of_dirname = os.path.dirname(os.path.dirname(files[0]))

target_location = dir_name_of_dirname
df2 = pd.DataFrame.empty
rows2 = []
for i in tqdm(files):
    tree = ET.parse(i)
    root = tree.getroot()
    GrantorEIN_check = root[0].find('./*{http://www.irs.gov/efile}EIN')
    GrantorEIN = GrantorEIN_check.text
    decoding = os.path.basename(i)[0:-6]
    filenumber = os.path.basename(i)[0:-11]
    docending = i.find('_public.xml')
    Docnumber = i[0:-docending]
    begindate_check = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDate')
    begindate_chcek2 = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDt')
    begindate = begindate_check.text if ET.iselement(
        begindate_check) else begindate_chcek2.text if ET.iselement(begindate_chcek2) else ''
    year = begindate[0:4]
    rows2.append([GrantorEIN, filenumber,year])
df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber','year'])
df2.to_csv(target_location + '/' + 'EIN_Docnumber_Dictionary.csv')

