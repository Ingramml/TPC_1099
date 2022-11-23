import glob
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import os

file='/Volumes/Storage/TPC990/Amazon_XMLs/2011_amazon_XML/201013993493000040_public.xml'
tree = ET.parse(file)
root = tree.getroot()
ns = {'Return':'http://www.irs.gov/efile'}
boardmemebrs = root[1].findall('.//{http://www.irs.gov/efile}Form990PartVIISectionA') if \
        ET.iselement(root[1].find('.//{http://www.irs.gov/efile}Form990PartVIISectionA')) == True \
        else root[1].findall('.//{http://www.irs.gov/efile}Form990PartVIISectionAGrp') if \
        ET.iselement(root[1].find('.//{http://www.irs.gov/efile}Form990PartVIISectionAGrp')) else ''

print(root[1].findall('Return:ReturnHeader',ns))
'''
for boardmemebr in boardmemebrs:
    #Name=boardmemebr[0].text
    #Title=boardmemebr[1].text
    print(bo
'''







'''    
    Name = boardmemebr.find('{http://www.irs.gov/efile}NamePerson')
    Title = boardmemebr.find('{http://www.irs.gov/efile}Title').text
    Averagehoursworked = boardmemebr.find('{http://www.irs.gov/efile}AverageHoursPerWeek').text if \
        ET.iselement(boardmemebr.find('{http://www.irs.gov/efile}AverageHoursPerWeek')) \
        else boardmemebr.find('{http://www.irs.gov/efile}AverageHoursPerWeekRt').text if \
        ET.iselement(boardmemebr.find('{http://www.irs.gov/efile}AverageHoursPerWeekRt')) else ''

    Individualtrusteeordirector = ''
    compensation_from_org = boardmemebr.find('{http://www.irs.gov/efile}ReportableCompFromOrganization').text
    compensation_from_related_org = boardmemebr.find('{http://www.irs.gov/efile}ReportableCompFromRelatedOrgs').text
    compensation = boardmemebr.find('{http://www.irs.gov/efile}OtherCompensation').text
    rows.append([EIN, Name, Title, Averagehoursworked, Individualtrusteeordirector, compensation_from_org,
                 compensation_from_related_org, compensation, year[0:4]])
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(os.path.join(target_location, begindate[0:4]) + '/' + EIN + 'boardmembers.csv')
'''