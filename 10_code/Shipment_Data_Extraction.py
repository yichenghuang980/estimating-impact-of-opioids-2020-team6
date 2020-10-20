#Read file to understand the structure of the csv
import pandas as pd
df = pd.read_csv('arcos_all_washpost.gz', compression='gzip', header=0, sep= '\t',nrows=20)
df.head()
#Read chunksize 100000 at a time
import warnings
warnings.filterwarnings('ignore')
df1=pd.read_csv('arcos_all_washpost.gz', compression='gzip', header=0, sep= '\t', chunksize=100000)
#Filter out states we are interested in (Group 1: Florida & 3 Other States)
states=['FL','LA','MS','SC']
df_list=[chunk[chunk['BUYER_STATE'].isin(states)][['BUYER_STATE', 'BUYER_COUNTY', 'BUYER_ZIP','TRANSACTION_DATE', 'DRUG_CODE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor']] for chunk in df1]
# Concat all the chunks to a dataframe
shipment_FL=pd.concat(df_list)
# Extarct Year
shipment_FL['YEAR'] = shipment_FL['TRANSACTION_DATE'].astype(str).str[-4:].astype(int)
#Calculate MME
shipment_FL['MME'] = round(shipment_FL['CALC_BASE_WT_IN_GM']*shipment_FL['MME_Conversion_Factor'],2)
#Convert to CSV
shipment_FL.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/shipment_FL.csv',index=False, header=True)


#Repeat the same steps above and filtered out the states we are interested (Group2: WA & Other 3 States)
df1=pd.read_csv('arcos_all_washpost.gz', compression='gzip', header=0, sep= '\t', chunksize=100000)
states2=['WA','CA','CO','OR']
df_list2=[chunk[chunk['BUYER_STATE'].isin(states2)][['BUYER_STATE', 'BUYER_COUNTY', 'BUYER_ZIP','TRANSACTION_DATE', 'DRUG_CODE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor']] for chunk in df1]
shipment_WA=pd.concat(df_list2)
# Extarct Month
shipment_WA['MONTH'] = shipment_WA['TRANSACTION_DATE'].astype(str).str[:-6].astype(int)
#Calculate MME
shipment_WA['MME'] = round(shipment_WA['CALC_BASE_WT_IN_GM']*shipment_WA['MME_Conversion_Factor'],2)
#Convert to CSV
shipment_WA.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/shipment_WA.csv',index=False, header=True)

#Repeat the same steps above and filtered out the states we are interested (Group3: WA & Other 3 States)
import warnings
warnings.filterwarnings('ignore')
df1=pd.read_csv('arcos_all_washpost.gz', compression='gzip', header=0, sep= '\t', chunksize=100000)
states3=['TX','AR','NM','KS']
df_list3=[chunk[chunk['BUYER_STATE'].isin(states3)][['BUYER_STATE', 'BUYER_COUNTY', 'BUYER_ZIP','TRANSACTION_DATE', 'DRUG_CODE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor']] for chunk in df1]
shipment_TX=pd.concat(df_list3)
# Extarct Month
shipment_TX['MONTH'] = shipment_TX['TRANSACTION_DATE'].astype(str).str[:-6].astype(int)
#Calculate MME
shipment_TX['MME'] = round(shipment_TX['CALC_BASE_WT_IN_GM']*shipment_TX['MME_Conversion_Factor'],2)
#Convert to CSV
shipment_TX.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/shipment_TX.csv',index=False, header=True)