import glob
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import os

files = glob.glob('/Volumes/SSD/TPC990/TPC_xml/*.xml')
target_location = '/Volumes/SSD/production'

for i in tqdm(files):
    rows2 = []
    tree = ET.parse(i)
    root = tree.getroot()
    GrantorEIN_check = root[0].find('./*{http://www.irs.gov/efile}EIN')
    begindate_check = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDate')
    begindate_chcek2 = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDt')
    begindate = begindate_check.text if ET.iselement(
        begindate_check) else begindate_chcek2.text if ET.iselement(begindate_chcek2) else ''
    year = begindate[0:4]
    # Creates folder based on begining year of tax return(begindate)
    if ET.iselement(GrantorEIN_check):
        folder = os.path.join(target_location, begindate[0:4])
        if os.path.exists(folder):
            pass
        else:
            os.makedirs(folder, exist_ok=True)
    else:
        os.rename(i, '/Volumes/Storage/TPC990/Errors/' + os.path.basename(i))
        print(os.path.basename(i) + ' moved')

    columns = ['ein', 'name', 'title', 'averagehousperweek', 'indivualtrusteeordirector', 'compensation_from_org',
               'compensation_from_related_org', 'othercompens', 'year']
    boardmemebrs = root[1].findall('.//{http://www.irs.gov/efile}Form990PartVIISectionA') if \
        ET.iselement(root[1].find('.//{http://www.irs.gov/efile}Form990PartVIISectionA')) \
        else root[1].findall('.//{http://www.irs.gov/efile}Form990PartVIISectionAGrp') if \
        ET.iselement(root[1].find('.//{http://www.irs.gov/efile}Form990PartVIISectionAGrp')) else ''

    EIN = root[0].find('.//{http://www.irs.gov/efile}EIN').text
    rows = []

    filecheck = target_location + '/' + year + '/boardmembers_' + EIN + '.csv'
 
    for boardmemeber in boardmemebrs:
        """
        #finds board members names
        name_check=boardmemeber.find("{http://www.irs.gov/efile}NamePerson")
        name_check2 = boardmemeber.find("{http://www.irs.gov/efile}PersonNm")
         
        """

        Name = boardmemeber.find("{http://www.irs.gov/efile}NamePerson").text if ET.iselement(
            boardmemeber.find("{http://www.irs.gov/efile}NamePerson")) \
            else boardmemeber.find("{http://www.irs.gov/efile}PersonNm").text if ET.iselement(
            boardmemeber.find("{http://www.irs.gov/efile}PersonNm")) \
            else ''
        """
        finds board members title
        title_check = boardmemeber.find('{http://www.irs.gov/efile}Title')
        title_check2 = boardmemeber.find('{http://www.irs.gov/efile}TitleTxt')
        
        """

        Title = boardmemeber.find('{http://www.irs.gov/efile}Title').text if ET.iselement(
            boardmemeber.find('{http://www.irs.gov/efile}Title')) \
            else boardmemeber.find('{http://www.irs.gov/efile}TitleTxt').text if ET.iselement(
            boardmemeber.find('{http://www.irs.gov/efile}TitleTxt')) \
            else ''

        Averagehoursworked = boardmemeber.find('{http://www.irs.gov/efile}AverageHoursPerWeek').text if \
            ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}AverageHoursPerWeek')) \
            else boardmemeber.find('{http://www.irs.gov/efile}AverageHoursPerWeekRt').text if \
            ET.iselement(
                boardmemeber.find('{http://www.irs.gov/efile}AverageHoursPerWeekRt')) else ''  # boardmember[2].text

        Individualtrusteeordirector = boardmemeber.find('{http://www.irs.gov/efile}IndividualTrusteeOrDirector').text \
            if ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}IndividualTrusteeOrDirector')) else ''

        compensation_from_org = boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromOrganization').text if \
            ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromOrganization')) else \
            boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromOrgAmt').text if \
            ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromOrgAmt')) else ''

        compensation_from_related_org = boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromRelatedOrgs').text \
            if ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromRelatedOrgs')) \
            else boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromRltdOrgAmt').text if \
            ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}ReportableCompFromRltdOrgAmt')) else ''

        other_compensation = boardmemeber.find('{http://www.irs.gov/efile}OtherCompensation').text if \
            ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}OtherCompensation')) else \
            boardmemeber.find('{http://www.irs.gov/efile}OtherCompensationAmt').text if \
            ET.iselement(boardmemeber.find('{http://www.irs.gov/efile}OtherCompensationAmt')) else ''

        rows.append([EIN, Name, Title, Averagehoursworked, Individualtrusteeordirector, compensation_from_org,
                     compensation_from_related_org, other_compensation, year[0:4]])
        df = pd.DataFrame(rows, columns=columns)
        df.to_csv(filecheck)
