import glob
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import os


files = glob.glob('/Volumes/SSD/download990mxls/*.xml')
target_location = '/Volumes/SSD/TPC990/testresults'
for i in tqdm(files):
    rows2 = []
    df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
    tree = ET.parse(i)
    root = tree.getroot()
    GrantorEIN_check = root[0].find('./*{http://www.irs.gov/efile}EIN')
    begindate_check = root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDate')
    begindate_chcek2 =root[0].find('./{http://www.irs.gov/efile}TaxPeriodBeginDt')
    begindate = begindate_check.text if ET.iselement(begindate_check)==True else begindate_chcek2.text if ET.iselement(begindate_chcek2)==True else ''
    year = begindate[0:4]
    #print(os.path.join(target_location, begindate[0:4]))
    #Creates folder based on begining year of tax return(begindate)

    if ET.iselement(GrantorEIN_check):
        folder = os.path.join(target_location, begindate[0:4])
        if os.path.exists(folder):
            pass
        else:
            os.makedirs(folder, exist_ok=True)
    else:
        os.rename(i, '/Volumes/Storage/TPC990/Errors/'+os.path.basename(i))

    GrantorEIN = GrantorEIN_check.text

    filecheck = target_location + '/' + year + '/' + GrantorEIN + '.csv'
    if os.path.isfile(filecheck):
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

        filecheck = target_location + '/' + year + '/' + GrantorEIN + '.csv'
        ScheduleI = root[1].find('{http://www.irs.gov/efile}IRS990ScheduleI')
        GrantOrContributionPdDurYrGrp_check = root[1].find(
            "./*/*/{http://www.irs.gov/efile}GrantOrContributionPdDurYrGrp")

        GrantOrContributionPdDurYrGrp = root[1].findall("./*/*/{http://www.irs.gov/efile}GrantOrContributionPdDurYrGrp")
        if ET.iselement(ScheduleI) == True and ET.iselement(ScheduleI.find('{http://www.irs.gov/efile}RecipientTable')):
            RecipientTable = ScheduleI.find('{http://www.irs.gov/efile}RecipientTable')
            RecipientTablelist = ScheduleI.findall('{http://www.irs.gov/efile}RecipientTable')
            rows = []
            for recipient in RecipientTablelist:
                recipient_EIN_check = recipient.find('./{http://www.irs.gov/efile}RecipientEIN')
                recipient_EIN_check2 = recipient.find('./{http://www.irs.gov/efile}EINOfRecipient')
                recipient_EIN = recipient_EIN_check.text if ET.iselement(recipient_EIN_check) == True else recipient_EIN_check2.text if ET.iselement(recipient_EIN_check2) else ''

                business_name_check = recipient.find('./*/{http://www.irs.gov/efile}BusinessNameLine1Txt')
                business_name_check2 = recipient.find('./{http://www.irs.gov/efile}RecipientPersonNm')
                business_name_check3 = recipient.find('./*/{http://www.irs.gov/efile}BusinessNameLine1')
                business_name = business_name_check.text if ET.iselement(
                    business_name_check) == True else business_name_check3.text if ET.iselement(
                    business_name_check3) == True else business_name_check2.text if ET.iselement(
                    business_name_check2) == True else ''

                address_element_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine1Txt')
                address_element_check2 = recipient.find('.*/{http://www.irs.gov/efile}AddressLine1')
                address_element_line1 = address_element_check.text if ET.iselement(
                    address_element_check) == True else address_element_check2.text if ET.iselement(address_element_check2)==True else ''

                address_element_line2_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine2Txt')
                address_element_line22_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine2')
                address_element_line2 = address_element_line2_check.text if ET.iselement(
                    address_element_line2_check) == True else address_element_line22_check.text  if ET.iselement(address_element_line22_check)==True else ''

                address_element_city_check = recipient.find('.*/{http://www.irs.gov/efile}CityNm')
                address_element_city_check2 = recipient.find('.*/{http://www.irs.gov/efile}City')
                address_element_city = address_element_city_check.text if ET.iselement(
                    address_element_city_check) == True else address_element_city_check2.text if ET.iselement(address_element_city_check2)==True else ''

                address_element_state_check = recipient.find('.*/{http://www.irs.gov/efile}StateAbbreviationCd')
                address_element_state_check2 = recipient.find('.*/{http://www.irs.gov/efile}State')
                address_element_state = address_element_state_check.text if ET.iselement(
                    address_element_state_check) == True else address_element_state_check2.text if ET.iselement(address_element_state_check2)==True else ''

                address_element_zip_check = recipient.find('.*/{http://www.irs.gov/efile}ZIPCd')
                address_element_zip_check2 = recipient.find('.*/{http://www.irs.gov/efile}ZIPCode')
                address_element_zip = address_element_zip_check.text if ET.iselement(
                    address_element_zip_check) == True else address_element_zip_check2.text if ET.iselement(address_element_zip_check2) == True else ''

                amount_element_check = recipient.find('./{http://www.irs.gov/efile}CashGrantAmt')
                amount_element_check2 = recipient.find('./{http://www.irs.gov/efile}AmountOfCashGrant')
                amount_element = amount_element_check.text if ET.iselement(amount_element_check) == True else amount_element_check2.text if ET.iselement(amount_element_check2)==True else ''

                status_element_check = recipient.find('./{http://www.irs.gov/efile}IRCSectionDesc')
                status_element_check2 = recipient.find('./{http://www.irs.gov/efile}IRCSection')
                status_element = status_element_check.text if ET.iselement(status_element_check) == True else status_element_check2.text if ET.iselement(status_element_check2)==True else ''

                purpose_element_check = recipient.find('./{http://www.irs.gov/efile}PurposeOfGrantTxt')
                purpose_element_check2 = recipient.find('./{http://www.irs.gov/efile}PurposeOfGrant')
                purpose_element = purpose_element_check.text if ET.iselement(purpose_element_check) == True else purpose_element_check2.text if ET.iselement(purpose_element_check2)==True else ''

                address = address_element_line1 + ' ' + address_element_line2 + ' ' + address_element_city + ' ' + address_element_state + ' ' + address_element_zip

                rows.append([GrantorEIN, None, recipient_EIN, business_name, address, amount_element,
                             status_element, purpose_element,year])

            df = pd.DataFrame(rows, columns=["grantor_EIN", "grantor_name", "EIN", "organization", "address", "amount",
                                             "status", "purpose","year"],dtype=object)  # creates df of orgs donations
            df.to_csv(filecheck)
        elif ET.iselement(GrantOrContributionPdDurYrGrp_check) == True:
            grants_list = root[1].findall("./*/*/{http://www.irs.gov/efile}GrantOrContributionPdDurYrGrp")
            rows = []
            for recipient in grants_list:
                # EINs
                recipient_EIN_check = recipient.find('./{http://www.irs.gov/efile}RecipientEIN')
                recipient_EIN = recipient_EIN_check.text if ET.iselement(recipient_EIN_check) == True else recipient.find('./{http://www.irs.gov/efile}EINOfRecipient')
                # Org Names
                business_name_check = recipient.find('./*/{http://www.irs.gov/efile}BusinessNameLine1Txt')
                business_name_check2 = recipient.find('./{http://www.irs.gov/efile}RecipientPersonNm')
                business_name_check3 = recipient.find('./*/{http://www.irs.gov/efile}BusinessNameLine1')
                business_name = business_name_check.text if ET.iselement(
                    business_name_check) == True else business_name_check3.text if ET.iselement(
                    business_name_check3) == True else business_name_check2.text if ET.iselement(
                    business_name_check2) == True else ''
                # address line 1
                address_element_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine1Txt')
                address_element_line1 = address_element_check.text if ET.iselement(
                    address_element_check) == True else ''
                # address line 2
                address_element_line2_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine2Txt')
                address_element_line2 = address_element_line2_check.text if ET.iselement(
                    address_element_line2_check) == True else ''
                # City
                address_element_city_check = recipient.find('.*/{http://www.irs.gov/efile}CityNm')
                address_element_city = address_element_city_check.text if ET.iselement(
                    address_element_city_check) == True else ''
                # State
                address_element_state_check = recipient.find('.*/{http://www.irs.gov/efile}StateAbbreviationCd')
                address_element_state = address_element_state_check.text if ET.iselement(
                    address_element_state_check) == True else ''
                # Zip
                address_element_zip_check = recipient.find('.*/{http://www.irs.gov/efile}ZIPCd')
                address_element_zip = address_element_zip_check.text if ET.iselement(
                    address_element_zip_check) == True else ''

                # Amount
                amount_element_check = recipient.find('./{http://www.irs.gov/efile}Amt')
                amount_element = amount_element_check.text if ET.iselement(amount_element_check) == True else recipient.find('./{http://www.irs.gov/efile}AmountOfCashGrant')
                # Org Status
                status_element_check = recipient.find('./{http://www.irs.gov/efile}Status')
                status_element = status_element_check.text if ET.iselement(status_element_check) == True else ''
                # Purpose
                purpose_element_check = recipient.find('./{http://www.irs.gov/efile}GrantOrContributionPurposeTxt')
                purpose_element = purpose_element_check.text if ET.iselement(purpose_element_check) == True else ''
                # combines Element
                address = address_element_line1 + ' ' + address_element_line2 + ' ' + address_element_city + ' ' + address_element_state + ' ' + address_element_zip

                rows.append([GrantorEIN, None, recipient_EIN, business_name, address, amount_element,
                             status_element, purpose_element,year])

            df = pd.DataFrame(rows, columns=["grantor_EIN", "grantor_name", "EIN", "organization", "address", "amount",
                                             "status", "purpose","year"],dtype="object")
            df.to_csv(filecheck)
        else:
            rows = []
            df = pd.DataFrame(rows, columns=["grantor_EIN", "grantor_name", "EIN", "organization", "address", "amount",
                                             "status", "purpose","year"],dtype="object")  # creates df of orgs donations
            df.to_csv(target_location + '/'+ year+ '/' + GrantorEIN + '.csv')
        df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])
#df2.to_csv(target_location + '/' + year + '-' + 'EIN_DocnumberDictionary.csv')


