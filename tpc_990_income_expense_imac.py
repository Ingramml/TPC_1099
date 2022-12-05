import glob
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import os

files = glob.glob('/Volumes/SSD/TPC990/Amazon_XMLs/*/*.xml')  #Xml files
target_location = '/Volumes/SSD/TPC990/Amazon990_2_csv'
for i in tqdm(files):
    rows = []
    rows2 = []
    rows3 = []
    df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
    tree = ET.parse(i)
    root = tree.getroot()
    GrantorEIN_check = root[0].find('./*{http://www.irs.gov/efile}EIN')
    begindate_check = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDate')
    begindate_chcek2 =root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDt')
    begindate = begindate_check.text if ET.iselement(begindate_check) == True else begindate_chcek2.text if \
        ET.iselement(begindate_chcek2) == True else ''
    year = begindate[0:4]


    #root[1].find('./{http://www.irs.gov/efile}ActivityOrMissionDescription/ActivityOrMissionDesc

    # Year the or started
    formationYear_check = root[1].find('./*{http://www.irs.gov/efile}YearFormation')
    formationYear_check2= root[1].find('./*{http://www.irs.gov/efile}FormationYr')
    formationYear = formationYear_check.text if ET.iselement(formationYear_check) else formationYear_check2.text \
    if ET.iselement(formationYear_check2) else ''

    #Year of the tax return
    taxYear_check = root[0].find('./{http://www.irs.gov/efile}TaxYear')
    taxYear_check2 =  root[0].find('./{http://www.irs.gov/efile}TaxYr')
    taxYear = taxYear_check.text if ET.iselement(taxYear_check) else taxYear_check2.text if \
        ET.iselement(taxYear_check) else ''

    #Mission
    missionCheck = root[1].find('./*{http://www.irs.gov/efile}ActivityOrMissionDescription')
    missionCheck_2 = root[1].find('./*{http://www.irs.gov/efile}ActivityOrMissionDesc')
    #ActivityOrMissionDescription
    mission = missionCheck.text if ET.iselement(missionCheck) else missionCheck_2.text if ET.iselement(missionCheck_2) \
        else ''

    GrantorEIN = GrantorEIN_check.text
    #Creates folder based on begining year of tax return(begindate)

    if ET.iselement(GrantorEIN_check):
        folder = os.path.join(target_location, begindate[0:4])
        if os.path.exists(folder):
            pass
        else:
            os.makedirs(folder, exist_ok=True)
    else:
        os.rename(i, '/Volumes/Storage/TPC990/Errors/'+os.path.basename(i))
        #print(os.path.basename(i) + ' moved')

    GrantorEIN = GrantorEIN_check.text

    filecheck_profile = target_location + '/' + year + '/profile_' + GrantorEIN + '.csv'
    filecheck_income_expense=target_location + '/' + year + '/income_expenses_' + GrantorEIN + '.csv'

    #needs new addition
    """
    if os.path.isfile(filecheck_profile) or os.path.isfile(filecheck_income_expense):
        decoding = os.path.basename(i)[0:-11]
        Docnumber = decoding  # may be unnecessary
        rows2.append([GrantorEIN, Docnumber])
        #df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
        pass
    else:
        # OrganizationName = OrganizationName_check.text
        # creates csv dictionary to allow checking for accuracy
        decoding = os.path.basename(i)[0:-11]
        Docnumber = decoding  # may be unnecessary
        rows2.append([GrantorEIN, Docnumber])
        #df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
    """

    #returntype
    return_check1 = root[0].find('./{http://www.irs.gov/efile}ReturnType')
    return_check2 = root[0].find('./{http://www.irs.gov/efile}ReturnTypeCd')

    returntype = return_check1.text if ET.iselement(return_check1) else return_check2.text if \
        ET.iselement(return_check2) else ''

    #Orgnames
    Filer=root[0].find('./{http://www.irs.gov/efile}Filer')

    #line1check
    businessname_check_ln1  = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine1') #2010 2013
    businessname_check2_ln1 = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine1Txt') #2020 2014 2016

    businessname_ln1 = businessname_check_ln1.text.upper() if ET.iselement(businessname_check_ln1) else \
        businessname_check2_ln1.text.upper() if ET.iselement(businessname_check2_ln1) else ''
    #line2check
    businessname_check_ln2 =  Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine2')
    businessname_check2_ln2 = Filer.find('./*{http://www.irs.gov/efile}BusinessNameLine2Txt')
    businessname_ln2 = businessname_check_ln2.text.upper() if ET.iselement(businessname_check_ln2) else \
        businessname_check2_ln2.text.upper() if ET.iselement(businessname_check2_ln2) else ''

    #Yearly Revenue
    Revenue_check = root[1].find('./*{http://www.irs.gov/efile}TotalRevenueCurrentYear') #works
    Revenue_check2 = root[1].find('./*{http://www.irs.gov/efile}Revenue')
    Revenue_check3 = root[1].find('./*{http://www.irs.gov/efile}CYTotalRevenueAmt')
    Revenue_check4 = root[1].find('./*{http://www.irs.gov/efile}TotalRevenueAmt')
    Revenue_check5 = root[1].find('./*{http://www.irs.gov/efile}TotalRevenue')

    Revenue = Revenue_check.text if ET.iselement(Revenue_check) == True \
        else Revenue_check2.text if ET.iselement(Revenue_check2) else \
        Revenue_check3.text if ET.iselement(Revenue_check3)==True else Revenue_check4.text if \
    ET.iselement(Revenue_check4) else Revenue_check5.text if ET.iselement(Revenue_check5) else ''

    #Yearly Expense
    Expense_check = root[1].find('./*{http://www.irs.gov/efile}TotalExpensesCurrentYear')  # works
    Expense_check2 = root[1].find('./*{http://www.irs.gov/efile}Expenses')
    Expense_check3 = root[1].find('./*{http://www.irs.gov/efile}CYTotalExpensesAmt')
    Expense_check4 = root[1].find('./*{http://www.irs.gov/efile}TotalExpensesAmt')
    Expense_check5 = root[1].find('./*{http://www.irs.gov/efile}TotalExpenses')
    Expense = Expense_check.text if ET.iselement(Expense_check)  \
        else Revenue_check2.text if ET.iselement(Expense_check2) else \
        Expense_check3.text if ET.iselement(Expense_check3) else Expense_check4.text if ET.iselement(Expense_check2) \
        else Expense_check5.text if ET.iselement(Expense_check5) else ''

    #print(Revenue+' '+ Expense)

    #Address line1
    address_element_check = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine1Txt')
    address_element_check2 = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine1')
    address_element_line1 = address_element_check.text if ET.iselement(
        address_element_check) == True else address_element_check2.text if ET.iselement(
        address_element_check2) == True else ''

    #address line2
    address_element_line2_check = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine2Txt')
    address_element_line22_check = root[0].find('.*/*{http://www.irs.gov/efile}AddressLine2')
    address_element_line2 = address_element_line2_check.text if ET.iselement(
        address_element_line2_check) == True else address_element_line22_check.text if ET.iselement(
        address_element_line22_check) == True else ''
    #Address city
    address_element_city_check = root[0].find('.*/*{http://www.irs.gov/efile}CityNm')
    address_element_city_check2 = root[0].find('.*/*{http://www.irs.gov/efile}City')
    address_element_city = address_element_city_check.text if ET.iselement(
        address_element_city_check) == True else address_element_city_check2.text if ET.iselement(
        address_element_city_check2) == True else ''
    #Address_state
    address_element_state_check = root[0].find('.*/*{http://www.irs.gov/efile}StateAbbreviationCd')
    address_element_state_check2 = root[0].find('.*/*{http://www.irs.gov/efile}State')
    address_element_state = address_element_state_check.text if ET.iselement(
        address_element_state_check) else address_element_state_check2.text if ET.iselement(
        address_element_state_check2) else ''

    #Address_zip
    address_element_zip_check = root[0].find('.*/*{http://www.irs.gov/efile}ZIPCd')
    address_element_zip_check2 = root[0].find('.*/*{http://www.irs.gov/efile}ZIPCode')
    address_element_zip = address_element_zip_check.text if ET.iselement(
        address_element_zip_check) else address_element_zip_check2.text if ET.iselement(
        address_element_zip_check2)  else ''

    #Website
    website_element_check = root[1].find('./*{http://www.irs.gov/efile}WebsiteAddressTxt')
    website_element_check2 = root[1].find('./*{http://www.irs.gov/efile}WebSite')
    website_element = website_element_check.text.upper() if ET.iselement(website_element_check) \
        else website_element_check2.text.upper() if ET.iselement(website_element_check2) else ''

    #Status

    status_check = root[1].find('./*{http://www.irs.gov/efile}Organization501cInd') #need attribute['organization501cTypeTx'] taxyears 2013,2016
    status_check2 = root[1].find('./*{http://www.irs.gov/efile}Organization501c') #needs attribtue['typeOf501cOrganization'] taxyears 2010,2011,2012
    status_check3 = root[1].find('./*{http://www.irs.gov/efile}Organization501c3Ind') #ifequals x use 1st
    status_check4 = root[1].find('./*{http://www.irs.gov/efile}Organization501c3')
    status = "501(c)3" if ET.iselement(status_check3) and status_check3.text == 'X' else '501(c)'+ str(status_check.attrib['organization501cTypeTx']) \
        if ET.iselement(status_check) and ET.iselement(status_check.attrib)=='organization501cTypeTxt' else \
        '501(c)'+str(status_check2.attrib['typeOf501cOrganization']) if ET.iselement(status_check2) else '501(c)3' if \
        ET.iselement(status_check4) and status_check4.text=='X' else ''

    #appends
    #incomeespnse append
    rows.append([GrantorEIN, Revenue, Expense, year, website_element, returntype])
    #profileappend
    rows3.append([GrantorEIN, businessname_ln1, businessname_ln2, address_element_line1, address_element_line2, address_element_city, address_element_state,
                  address_element_zip, website_element, status, mission, formationYear])

    #income_expense
    df = pd.DataFrame(rows, columns=["ein", "revenue", "expenses", "year", "website",'returntype'], dtype="object")

    #profile
    df2 = pd.DataFrame(rows3, columns=['ein',"orgname_ln2","orgname_ln2", "address_1", "address_2", "city", "state", "zipcode", "website", "status",
                                      "mission", "yearstarted"], dtype="object")

    #df.to_csv(target_location + '/' + year + '/income_expenses_' + GrantorEIN + '.csv')

    df2.to_csv(target_location + '/' + year + '/profile_' + GrantorEIN + '.csv')
