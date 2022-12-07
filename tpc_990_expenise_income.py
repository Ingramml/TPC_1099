import glob
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import os

files = glob.glob('/Volumes/SSD/TPC990/TPC_xml/*.xml')  # Xml files
target_location = '/Volumes/SSD/production'
for i in tqdm(files):
    # print(i)
    rows_income_expense = []
    rows2_profile = []
    tree = ET.parse(i)
    root = tree.getroot()
    GrantorEIN_check = root[0].find('./*{http://www.irs.gov/efile}EIN')
    begindate_check = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDate')
    begindate_chcek2 = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDt')
    begindate = begindate_check.text if ET.iselement(begindate_check) else begindate_chcek2.text if \
        ET.iselement(begindate_chcek2) else ''

    year = begindate[0:4]

    GrantorEIN = GrantorEIN_check.text
    # Creates folder based on begining year of tax return(begindate)

    if ET.iselement(GrantorEIN_check):
        folder = os.path.join(target_location, begindate[0:4])
        if os.path.exists(folder):
            pass
        else:
            os.makedirs(folder, exist_ok=True)
    else:
        os.rename(i,'/Volumes/Storage/TPC990/Errors/'+os.path.basename(i))
        # print(os.path.basename(i) + ' moved')

    GrantorEIN = GrantorEIN_check.text

    filecheck_income = target_location + '/' + year + '/income_expenses_' + GrantorEIN + '.csv'
    filecheck_Profile = target_location + '/' + year + '/profile_' + GrantorEIN + '.csv'
    """
    if os.path.isfile(filecheck_income) or os.path.isfile(filecheck_profile):
        decoding = os.path.basename(i)[0:-11]
        Docnumber = decoding  # may be unnecessary
        rows2.append([GrantorEIN, Docnumber])
        # df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
        pass
    else:
        # OrganizationName = OrganizationName_check.text
        # creates csv dictionary to allow checking for accuracy
        decoding = os.path.basename(i)[0:-11]
        Docnumber = decoding  # may be unnecessary
        rows2.append([GrantorEIN, Docnumber])
        # df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
    """

    Filer = root[0].find('./{http://www.irs.gov/efile}Filer')

    # line1check
    businessname_check_ln1 = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine1')  # 2010 2013
    businessname_check2_ln1 = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine1Txt')  # 2020 2014 2016

    businessname_ln1 = businessname_check_ln1.text.upper() if ET.iselement(businessname_check_ln1) else \
        businessname_check2_ln1.text.upper() if ET.iselement(businessname_check2_ln1) else ''
    # line2check
    businessname_check_ln2 = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine2')
    businessname_check2_ln2 = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine2Txt')
    businessname_ln2 = businessname_check_ln2.text.upper() if ET.iselement(businessname_check_ln2) else \
        businessname_check2_ln2.text.upper() if ET.iselement(businessname_check2_ln2) else ''


    # returnType
    return_check1 = root[0].find('./{http://www.irs.gov/efile}ReturnType')
    return_check2 = root[0].find('./{http://www.irs.gov/efile}ReturnTypeCd')

    returnType = return_check1.text if ET.iselement(return_check1) else return_check2.text if \
        ET.iselement(return_check2) else ''

    #Yearly Revenue
    Revenue_check = root[1].find('./*{http://www.irs.gov/efile}TotalRevenueCurrentYear')  # works
    Revenue_check2 = root[1].find('./*{http://www.irs.gov/efile}Revenue')
    Revenue_check3 = root[1].find('./*{http://www.irs.gov/efile}CYTotalRevenueAmt')
    Revenue_check4 = root[1].find('./*{http://www.irs.gov/efile}TotalRevenueAmt')
    Revenue_check5 = root[1].find('./*{http://www.irs.gov/efile}TotalRevenue')

    Revenue = Revenue_check.text if ET.iselement(Revenue_check) == True \
        else Revenue_check2.text if ET.iselement(Revenue_check2) else \
        Revenue_check3.text if ET.iselement(Revenue_check3) == True else Revenue_check4.text if \
        ET.iselement(Revenue_check4) else Revenue_check5.text if ET.iselement(Revenue_check5) else ''

    # Yearly Expense
    Expense_check = root[1].find('./*{http://www.irs.gov/efile}TotalExpensesCurrentYear')  # works
    Expense_check2 = root[1].find('./*{http://www.irs.gov/efile}Expenses')
    Expense_check3 = root[1].find('./*{http://www.irs.gov/efile}CYTotalExpensesAmt')
    Expense_check4 = root[1].find('./*{http://www.irs.gov/efile}TotalExpensesAmt')
    Expense_check5 = root[1].find('./*{http://www.irs.gov/efile}TotalExpenses')
    Expense = Expense_check.text if ET.iselement(Expense_check) \
        else Revenue_check2.text if ET.iselement(Expense_check2) else \
        Expense_check3.text if ET.iselement(Expense_check3) else Expense_check4.text if ET.iselement(Expense_check2) \
            else Expense_check5.text if ET.iselement(Expense_check5) else ''

    address_element_check = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine1Txt')
    address_element_check2 = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine1')
    address_element_line1 = address_element_check.text if ET.iselement(
        address_element_check) else address_element_check2.text if ET.iselement(
        address_element_check2) else ''

    address_element_line2_check = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine2Txt')
    address_element_line22_check = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine2')
    address_element_line2 = address_element_line2_check.text if ET.iselement(
        address_element_line2_check) else address_element_line22_check.text if ET.iselement(
        address_element_line22_check) else ''

    address_element_city_check = root[0].find('.*/*{http://www.irs.gov/efile}CityNm')
    address_element_city_check2 = root[0].find('.*/*{http://www.irs.gov/efile}City')
    address_element_city = address_element_city_check.text if ET.iselement(
        address_element_city_check) else address_element_city_check2.text if ET.iselement(
        address_element_city_check2) else ''

    address_element_state_check = root[0].find('.*/*{http://www.irs.gov/efile}StateAbbreviationCd')
    address_element_state_check2 = root[0].find('.*/*{http://www.irs.gov/efile}State')
    address_element_state = address_element_state_check.text if ET.iselement(
        address_element_state_check) else address_element_state_check2.text if ET.iselement(
        address_element_state_check2) else ''

    address_element_zip_check = root[0].find('.*/*{http://www.irs.gov/efile}ZIPCd')
    address_element_zip_check2 = root[0].find('.*/*{http://www.irs.gov/efile}ZIPCode')
    address_element_zip = address_element_zip_check.text if ET.iselement(
        address_element_zip_check) else address_element_zip_check2.text if ET.iselement(
        address_element_zip_check2) else ''
    # Website
    website_element_check = root[1].find('./*{http://www.irs.gov/efile}WebsiteAddressTxt')
    website_element_check2 = root[1].find('./*{http://www.irs.gov/efile}WebSite')
    website_element = website_element_check.text.upper() if ET.iselement(website_element_check) \
        else website_element_check2.text.upper() if ET.iselement(website_element_check2) else ''

    total_assets_boy_check1 = root[1].find('./*{http://www.irs.gov/efile}TotalAssetsBOY')  # 2010 2015
    total_assets_boy_check2 = root[1].find('./*{http://www.irs.gov/efile}Form990TotalAssetsGrp/BOYAmt')
    total_assets_boy_check3 = root[1].find('./*{http://www.irs.gov/efile}TotalAssetsBOYAmt')  # 2020

    total_assets_boy = total_assets_boy_check1.text if ET.iselement(total_assets_boy_check1) else \
        total_assets_boy_check2.text if ET.iselement(total_assets_boy_check2) else total_assets_boy_check3.text \
        if ET.iselement(total_assets_boy_check3) else ''

    total_assets_eoy_check1 = root[1].find('./*{http://www.irs.gov/efile}TotalAssetsEOY')  # 2010
    total_assets_eoy_check2 = root[1].find('./*{http://www.irs.gov/efile}Form990TotalAssetsGrp/EOYAmt')
    total_assets_eoy_check3 = root[1].find('./*{http://www.irs.gov/efile}TotalAssetsEOYAmt')  # 2020

    total_assets_eoy = total_assets_eoy_check1.text if ET.iselement(total_assets_eoy_check1) else \
        total_assets_eoy_check3.text if ET.iselement(total_assets_eoy_check3) else total_assets_eoy_check2.text if \
        ET.iselement(total_assets_eoy_check2) else ''

    # Status
    #TODO need to deal with dictionary reuslts
    status_check = root[1].find(
        './*{http://www.irs.gov/efile}Organization501cInd')  # need attribute['organization501cTypeTx'] taxyears 2013,2016
    status_check2 = root[1].find(
        './*{http://www.irs.gov/efile}Organization501c')  # needs attribtue['typeOf501cOrganization'] taxyears 2010,2011,2012
    status_check3 = root[1].find('./*{http://www.irs.gov/efile}Organization501c3Ind')  # if equals x use 1st
    status_check4 = root[1].find('./*{http://www.irs.gov/efile}Organization501c3')
    status = "501(c)3" if ET.iselement(status_check3) and status_check3.text == 'X' else '501(c)' + str(
        status_check.attrib['organization501cTypeTx']) \
        if ET.iselement(status_check) and ET.iselement(status_check.attrib) == 'organization501cTypeTxt' else \
        '501(c)' + str(status_check2.attrib['typeOf501cOrganization']) if ET.iselement(status_check2) else '501(c)3' if \
            ET.iselement(status_check4) and status_check4.text == 'X' else ''

    #mission
    mission_check1 = root[1].find("./*{http://www.irs.gov/efile}ActivityOrMissionDesc")
    mission_check2 = root[1].find('./*{http://www.irs.gov/efile}PrimaryExemptPurposeTxt')
    mission_check3 = root[1].find('./*{http://www.irs.gov/efile}MissionDesc')
    mission_check4 = root[1].find('./*{http://www.irs.gov/efile}ActivityOrMissionDescription')


    mission = mission_check1.text if ET.iselement(mission_check1) else mission_check2.text if ET.iselement(mission_check2) \
        else mission_check3.text if ET.iselement(mission_check3) else mission_check4.text if ET.iselement(mission_check4) \
        else ''

    # Creates income expense csv
    rows_income_expense.append([GrantorEIN, Revenue, Expense, total_assets_boy, total_assets_eoy,
                               returnType, year])

    df = pd.DataFrame(rows_income_expense, columns=["ein","revenue", "expenses", "total_assets_boy",
                                                    "total_assets_eoy","return_type","year"], dtype="object")

    # Creates profiles Csv
    rows2_profile.append([GrantorEIN, businessname_ln1.upper(), businessname_ln2.upper(), address_element_line1.upper(),
                          address_element_line2.upper(), address_element_city.upper(), address_element_state,
                          address_element_zip, website_element, mission.upper(), status, year])

    df2 = pd.DataFrame(rows2_profile, columns=["ein", "org_name1", "org_name2", "address_1", "address_2", "city",
                                               "state", "zipcode", "website", "mission","status", "year"], dtype="object")
    df.to_csv(filecheck_income)
    df2.to_csv(filecheck_Profile)
