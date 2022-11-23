
import pandas as pd
import os
import glob
import xml.etree.ElementTree as ET
import time
from tqdm import tqdm

import Zipfiles

start_time = time.time()


allxml = glob.glob(Zipfiles.openlocation+'/*.xml')
basename = os.path.basename(allxml[1])
dirname = os.path.basename(allxml[1])

Yearfolder = os.path.join('/Users/michaelingram/Documents', str(basename[0:4]))
os.makedirs(Yearfolder, exist_ok=True)
rows2 = []
df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])

for i in tqdm(allxml):
    tree = ET.parse(i)
    root = tree.getroot()
    GrantorEIN_check = root[0].find('./*{http://www.irs.gov/efile}EIN')
    # OrganizationName_check = root[0].find("./*/*{http://www.irs.gov/efile}BusinessNameLine1Txt")
    GrantorEIN = GrantorEIN_check.text
    # OrganizationName = OrganizationName_check.text
    # creates csv dictionary to allow checking for accuracy
    decoding = os.path.basename(i)[0:-11]
    print(i)
    Docnumber = decoding  #may be unneccasary
    rows2.append([GrantorEIN, Docnumber])
    df2 = pd.DataFrame(rows2, columns=['EIN', 'Docnumber'])

    filecheck = Yearfolder + '/' + GrantorEIN + '.csv'
    if os.path.isfile(filecheck) == True:
        pass
    else:
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
                recipient_EIN = recipient_EIN_check.text if ET.iselement(recipient_EIN_check) == True else ''

                business_name_check = recipient.find('./*/{http://www.irs.gov/efile}BusinessNameLine1Txt')
                business_name_check2 = recipient.find('./{http://www.irs.gov/efile}RecipientPersonNm')
                business_name_check3 = recipient.find('./*/{http://www.irs.gov/efile}BusinessNameLine1')
                business_name = business_name_check.text if ET.iselement(
                    business_name_check) == True else business_name_check3.text if ET.iselement(
                    business_name_check3) == True else business_name_check2.text if ET.iselement(
                    business_name_check2) == True else ''

                address_element_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine1Txt')
                address_element_line1 = address_element_check.text if ET.iselement(
                    address_element_check) == True else ''

                address_element_line2_check = recipient.find('.*/{http://www.irs.gov/efile}AddressLine2Txt')
                address_element_line2 = address_element_line2_check.text if ET.iselement(
                    address_element_line2_check) == True else ''

                address_element_city_check = recipient.find('.*/{http://www.irs.gov/efile}CityNm')
                address_element_city = address_element_city_check.text if ET.iselement(
                    address_element_city_check) == True else ''

                address_element_state_check = recipient.find('.*/{http://www.irs.gov/efile}StateAbbreviationCd')
                address_element_state = address_element_state_check.text if ET.iselement(
                    address_element_state_check) == True else ''

                address_element_zip_check = recipient.find('.*/{http://www.irs.gov/efile}ZIPCd')
                address_element_zip = address_element_zip_check.text if ET.iselement(
                    address_element_zip_check) == True else ''

                amount_element_check = recipient.find('./{http://www.irs.gov/efile}CashGrantAmt')
                amount_element = amount_element_check.text if ET.iselement(amount_element_check) == True else ''

                status_element_check = recipient.find('./{http://www.irs.gov/efile}IRCSectionDesc')
                status_element = status_element_check.text if ET.iselement(status_element_check) == True else ''

                purpose_element_check = recipient.find('./{http://www.irs.gov/efile}PurposeOfGrantTxt')
                purpose_element = purpose_element_check.text if ET.iselement(purpose_element_check) == True else ''

                address = address_element_line1 + ' ' + address_element_line2 + ' ' + address_element_city + ' ' + address_element_state + ' ' + address_element_zip

                rows.append([GrantorEIN, None, recipient_EIN, business_name, address, amount_element,
                             status_element, purpose_element])

            df = pd.DataFrame(rows, columns=["grantor_EIN", "grantor_name", "EIN", "orgnizaiton", "address", "amount",
                                             "status", "purpose"])  # creats df of orgs donations
            df.to_csv(filecheck)
        elif ET.iselement(GrantOrContributionPdDurYrGrp_check) == True:
            grants_list = root[1].findall("./*/*/{http://www.irs.gov/efile}GrantOrContributionPdDurYrGrp")
            rows = []
            for recipient in grants_list:
                # EINs
                recipient_EIN_check = recipient.find('./{http://www.irs.gov/efile}RecipientEIN')
                recipient_EIN = recipient_EIN_check.text if ET.iselement(recipient_EIN_check) == True else ''
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
                amount_element = amount_element_check.text if ET.iselement(amount_element_check) == True else ''
                # Org Status
                status_element_check = recipient.find('./{http://www.irs.gov/efile}Status')
                status_element = status_element_check.text if ET.iselement(status_element_check) == True else ''
                # Puurpose
                purpose_element_check = recipient.find('./{http://www.irs.gov/efile}GrantOrContributionPurposeTxt')
                purpose_element = purpose_element_check.text if ET.iselement(purpose_element_check) == True else ''
                # combines Element
                address = address_element_line1 + ' ' + address_element_line2 + ' ' + address_element_city + ' ' + address_element_state + ' ' + address_element_zip

                rows.append([GrantorEIN, None, recipient_EIN, business_name, address, amount_element,
                             status_element, purpose_element])

            df = pd.DataFrame(rows, columns=["grantor_EIN", "grantor_name", "EIN", "orgnizaiton", "address", "amount",
                                             "status", "purpose"])
            df.to_csv(filecheck)
        else:
            rows = []
            df = pd.DataFrame(rows, columns=["grantor_EIN", "grantor_name", "EIN", "orgnizaiton", "address", "amount",
                                             "status", "purpose"])  # creats df of orgs donations
            df.to_csv(Yearfolder + '/' + GrantorEIN + '.csv')
df2.to_csv(Zipfiles.openlocation + '/'+str(os.path.basename(Zipfiles.openlocation))+'-'+'EIN_DocnumberDictionary.csv')


filetype = 'csv'
all_files = glob.glob(Yearfolder + "/*." + filetype)
print(len(all_files))

filetype = "csv"
all_files = glob.glob(Yearfolder + "/*." + filetype)

for file in all_files:
    df = pd.read_csv(file)
    if df.empty:
        os.remove(file)
    else:
        pass

li = []
all_files_2 = glob.glob(Yearfolder + "/*." + filetype)
for filename in all_files_2:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv(Yearfolder + '/'+str(Zipfiles.openlocation[-6:])+'combines.csv', index=False)

end_time = time.time()

print('Search took ' + str((end_time - start_time)) + ' in seconds')
