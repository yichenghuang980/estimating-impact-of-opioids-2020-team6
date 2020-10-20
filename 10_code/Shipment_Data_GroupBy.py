# Read the csv created by Shipment_Data_Extraction (Group1: FL & 3 Other States) 
import pandas as pd
FL= pd.read_csv("shipment_FL.csv")
FL.head()
#Drop the unnecessary columns
drop=['TRANSACTION_DATE', 'DRUG_CODE', 'CALC_BASE_WT_IN_GM', 'MME_Conversion_Factor','BUYER_ZIP']
FL1=FL.drop(axis=1,columns=drop)
#Group By State, County, and Year
FL_agg=FL1.groupby(['BUYER_STATE','BUYER_COUNTY','YEAR'],as_index=False).sum()
FL_agg.head()
#Convert to CSV
FL_agg.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/FL_agg.csv',index=False, header=True)

# Read the csv created by Shipment_Data_Extraction (Group2: TX & 3 Other States) 
TX= pd.read_csv("shipment_TX.csv")
TX.head()
#Drop the unnecessary columns
TX1=TX.drop(axis=1,columns=drop)
#Group By State, County, and Year
TX_agg=TX1.groupby(['BUYER_STATE','BUYER_COUNTY','MONTH'],as_index=False).sum()
TX_agg.head()
# Convert to CSV
TX_agg.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/TX_agg.csv',index=False, header=True)

# Read the csv created by Shipment_Data_Extraction (Group2: WA & 3 Other States) 
WA= pd.read_csv("shipment_WA.csv")
WA.head()
#Drop the unnecessary columns
WA1=WA.drop(axis=1,columns=drop)
#Group By State, County, and Year
WA_agg=WA1.groupby(['BUYER_STATE','BUYER_COUNTY','MONTH'],as_index=False).sum()
WA_agg.head()
#Convert to CSV
WA_agg.to_csv(r'/Users/Dean Huang/Documents/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/WA_agg.csv',index=False, header=True)