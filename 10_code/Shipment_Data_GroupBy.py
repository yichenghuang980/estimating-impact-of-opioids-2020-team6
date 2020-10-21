# Read the csv created by Shipment_Data_Extraction (Group1: FL & 3 Other States) 
import pandas as pd
FL= pd.read_csv("shipment_FL.csv")
FL.head()
#Rename YEAR Column
FL=FL.rename(columns={"YEAR": "YEAR/MONTH"})
#Drop the unnecessary columns
drop=['TRANSACTION_DATE', 'DRUG_CODE', 'CALC_BASE_WT_IN_GM', 'MME_Conversion_Factor','BUYER_ZIP']
FL1=FL.drop(axis=1,columns=drop)
#Group By State, County, and Year
FL_agg=FL1.groupby(['BUYER_STATE','BUYER_COUNTY','YEAR/MONTH'],as_index=False).sum()
FL_agg.head()

# Read the csv created by Shipment_Data_Extraction (Group2: TX & 3 Other States) 
TX= pd.read_csv("shipment_TX.csv")
TX.head()
#Rename MONTH Column
TX=TX.rename(columns={"MONTH": "YEAR/MONTH"})
#Drop the unnecessary columns
TX1=TX.drop(axis=1,columns=drop)
#Group By State, County, and Year
TX_agg=TX1.groupby(['BUYER_STATE','BUYER_COUNTY','YEAR/MONTH'],as_index=False).sum()
TX_agg.head()

# Read the csv created by Shipment_Data_Extraction (Group2: WA & 3 Other States) 
WA= pd.read_csv("shipment_WA.csv")
WA.head()
#Rename MONTH Column
WA=WA.rename(columns={"MONTH": "YEAR/MONTH"})
#Drop the unnecessary columns
WA1=WA.drop(axis=1,columns=drop)
#Group By State, County, and Year
WA_agg=WA1.groupby(['BUYER_STATE','BUYER_COUNTY','YEAR/MONTH'],as_index=False).sum()
WA_agg.head()
#Concatenate the dataframes into one
SHIPMENT_agg = pd.concat([FL_agg, TX_agg, WA_agg], axis=0)
#Convert to CSV
SHIPMENT_agg.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/SHIPMENT_agg.csv',index=False, header=True)