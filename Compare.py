import pandas as pd

amazon='/Volumes/Storage/TPC990/Amazon990_csv_boardmembers/2000_990_Amazon990_csv_boardmembers_combined.csv'
irs='/Volumes/Storage/TPC990/Irs_ boardmembers/2000_990_Irs_ boardmembers_combined.csv'

dfamazon=pd.read_csv(amazon)
dfirs=pd.read_csv(irs)

print(dfamazon.dtypes)
print(dfirs.dtypes)

print(dfamazon.reset_index(drop=True).equals(dfirs.reset_index(drop=True)))


