from irs_file_downloading import irsdownload
import os
import datetime
import glob
import pandas as pd
from tpc_990_expenise_income import irs_expense_income
from Boardmember_xml_scrapping import irs_boardmember
from TPC_grants import irs_grants


#df=pd.read_csv('/Users/michaelingram/Downloads/newfiles.csv',index_col=False)
#file_list=df['filename'].tolist()


#irs_expense_income(file_list,'/Users/michaelingram/Downloads/Tpc')
#irs_grants(file_list,'/Users/michaelingram/Downloads/Tpc')
#irs_boardmember(file_list,'/Users/michaelingram/Downloads/Tpc')
keyword = 'profile'
file_location='/Users/michaelingram/Downloads/Tpc'

print(glob.glob(os.path.join((file_location ,'/*.cvs'))))
print(file_location+'/*.csv')
#print(files)