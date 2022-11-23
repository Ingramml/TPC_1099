import pandas as pd
import os
import time

start_time=time.time()
file='/Users/michaelingram/Downloads/TPC_990_2017-2015.csv'
df=pd.read_csv(file)
basename=os.path.basename(file)[0:-4]

# define string
string = "Python is awesome, isn't it?"
substring = "is"
count = string.count(substring)
police='Police'
count_police=string.count(police)

columns=['org_name','ein','police','cheif','Law_enforcement','officer','detecive','investigator','corporal','seargent','lieutenant','sheriff', \
        'deputy','highway_patrol','trooper','detention','correction','border_patrol','immigration&custom_enforcement*','Total_count'] #18 rows
rows=[]

for index, row in df.iterrows():
        org_name = row['organization']
        EIN=row['ein']
        string = row['organization'].lower()
        police = string.count('police') #2
        chief = string.count('chief')+string.count('cheif') #3
        law_enforcement = string.count('law enforcement') #4
        officer = string.count('officer') #5
        detective = string.count('detecive') #6
        investigator = string.count('investigator') #7
        corporal = string.count('corporal') #8
        seargent = string.count('seargent') #9
        lieutenant = string.count('lieutenant') #10
        sheriff = string.count('sheriff') +string.count('sherif') #11
        deputy = string.count('deputy')  #12
        highway_patrol = string.count('highway patrol') #13
        trooper = string.count('trooper') #14
        detention = string.count('detention') #15
        correction = string.count('correction') #16
        border_patrol = string.count('border patrol') #17
        immigration_custom_enforcement = string.count('custom') #18

        total_count = police+chief+law_enforcement+officer+detective+investigator+corporal+seargent+lieutenant+sheriff+deputy+highway_patrol+trooper+detention+correction+border_patrol+immigration_custom_enforcement


        rows.append([org_name,EIN,police,chief,law_enforcement,officer,detective,investigator,corporal,seargent
                     ,lieutenant,sheriff,deputy,highway_patrol,trooper,detention,correction,border_patrol,immigration_custom_enforcement,total_count])
        df2=pd.DataFrame(rows,columns=columns)
#df2.to_csv('/Users/michaelingram/Downloads/'+basename+'keyworcount.csv')
end_time=time.time()
print(str(end_time-start_time)+' seconds')
