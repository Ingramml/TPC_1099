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
        os.rename(i, '/Volumes/Storage/TPC990/Errors/'+os.path.basename(i))
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
    # filecheck = target_location + '/' + year + '/' + GrantorEIN + '.csv'
    Revenue_check = root[1].find('./*{http://www.irs.gov/efile}TotalRevenueCurrentYear')  # works
    Revenue_check2 = root[1].find('./*{http://www.irs.gov/efile}Revenue')
    Revenue_check3 = root[1].find('./*{http://www.irs.gov/efile}CYTotalRevenueAmt')
    Revenue = Revenue_check.text if ET.iselement(Revenue_check) \
        else Revenue_check2.text if ET.iselement(Revenue_check2) else \
        Revenue_check3.text if ET.iselement(Revenue_check3) else ''

    Expense_check = root[1].find('./*{http://www.irs.gov/efile}TotalExpensesCurrentYear')  # works
    Expense_check2 = root[1].find('./*{http://www.irs.gov/efile}Expenses')
    Expense_check3 = root[1].find('./*{http://www.irs.gov/efile}CYTotalExpensesAmt')
    Expense = Expense_check.text if ET.iselement(Expense_check)  \
        else Revenue_check2.text if ET.iselement(Expense_check2) else \
        Expense_check3.text if ET.iselement(Expense_check3) else ''

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

    # Creates income expense csv
    rows_income_expense.append([GrantorEIN, Revenue, Expense, total_assets_boy, total_assets_eoy,
                                website_element, year])

    df = pd.DataFrame(rows_income_expense, columns=["ein", "revenue", "expenses", "total_assets_boy",
                                                    "total_assets_eoy", "website", "year"], dtype="object")

    # Creates profiles Csv
    rows2_profile.append([GrantorEIN, address_element_line1.upper(), address_element_line2.upper(), address_element_city.upper(),
                          address_element_state, address_element_zip, website_element, year])

    df2 = pd.DataFrame(rows2_profile, columns=["ein", "address_1", "address_2", "city", "state", "zipcode", "website",
                                               "year"], dtype="object")
    df.to_csv(filecheck_income)
    df2.to_csv(filecheck_Profile)
