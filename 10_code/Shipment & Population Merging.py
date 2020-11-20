# Load the required packages needed for performing data merging
get_ipython().run_line_magic('load_ext', 'lab_black')
import pandas as pd
import numpy as np
# Load shipment csv
ship = pd.read_csv(
    "C:/Users/Dean Huang/estimating-impact-of-opioids-2020-team6/00_source/SHIPMENT_agg.csv",
    sep=",",
)
# Check if there are anu duuplicate values
assert not ship.duplicated().any()
# Check if there are any null values
ship.isnull().any()
# Check the format of dataframe is correct
ship.head()
# Create a new column that only has Year (for merging)
ship["Year"] = ship["YEAR/MONTH"].astype(str).str[:4].astype(int)
ship[ship["BUYER_STATE"] == "WA"]
# Create a dictionary fpr mapping States to its abbreviation
States = {
    "FL": "Florida",
    "LA": "Louisiana",
    "MS": "Mississippi",
    "SC": "South Carolina",
    "WA": "Washington",
    "OR": "Oregon",
    "CO": "Colorado",
    "CA": "California",
    "TX": "Texas",
    "AR": "Arkansas",
    "NM": "New Mexico",
    "KS": "Kansas",
}
ship["FULL_STATES"] = ship["BUYER_STATE"].replace(States)
ship["FULL_STATES"].unique()
# Check if there are any null values
ship["FULL_STATES"].isnull().any()
# Load population 2000~2010 CSV
pop0 = pd.read_csv(
    "C:/Users/Dean Huang/estimating-impact-of-opioids-2020-team6/00_source/CensusEstimates2000-2010.csv",
    sep=",",
    encoding="ISO-8859-1",
)
pop0.head()

# Load population 2010~2019 CSV
pop1 = pd.read_csv(
    "C:/Users/Dean Huang/estimating-impact-of-opioids-2020-team6/00_source/CensusEstimates2010-2019 (Ship).csv",
    sep=",",
    encoding="ISO-8859-1",
)
pop1.head()
# Drop ESTIMATEBASE2000 because we are using CENSUS2000POP
pop0 = pop0.drop(["ESTIMATESBASE2000", "CENSUS2010POP", "POPESTIMATE2010"], axis=1)
pop0.head()
# Drop ESTIMATEBASE2010 because we are using CENSUS2010POP
pop1 = pop1.drop(["ESTIMATESBASE2010", "POPESTIMATE2010"], axis=1)
# Change CENSUS2010POP  to CENSUS2010
pop1.rename(columns={"CENSUS2010POP": "CENSUS2010"}, inplace=True)
pop1.head()
# Subset only the states we are interested
States = [
    "Florida",
    "Louisiana",
    "Mississippi",
    "South Carolina",
    "Washington",
    "Oregon",
    "Colorado",
    "California",
    "Texas",
    "Arkansas",
    "New Mexico",
    "Kansas",
]
pop0_final = pop0[pop0["STNAME"].isin(States) == True]
pop1_final = pop1[pop1["STNAME"].isin(States) == True]
# Check the subset datafram only contain the states mentioned in the list
pop0_final["STNAME"].unique()
# Check the subset datafram only contain the states mentioned in the list
pop1_final["STNAME"].unique()
# Melt the dataframe so all the years is in one column
pop0_melt = pd.melt(
    pop0_final,
    ["SUMLEV", "REGION", "DIVISION", "STATE", "COUNTY", "STNAME", "CTYNAME"],
    var_name="Year",
    value_name="Population",
)
pop0_melt.head()
# Check population is correct after melting the dataframe
pop0_final[pop0_final["POPESTIMATE2000"] == 20776]
# Melt the dataframe so all the years is in one column
pop1_melt = pd.melt(
    pop1_final,
    ["SUMLEV", "REGION", "DIVISION", "STATE", "COUNTY", "STNAME", "CTYNAME"],
    var_name="Year",
    value_name="Population",
)
pop1_melt.head()
# Check population is correct after melting the dataframe
pop1_final[pop1_final["CENSUS2010"] == 19019.0]
# Concatenate these two dataframes into 1
popc = pd.concat([pop0_melt, pop1_melt], axis=0)
popc.head()
# Check everything is concatenate together
popc["Year"].unique()
# Remove county=0
popc = popc[popc["COUNTY"] != 0]
assert not (popc["COUNTY"] == 0).any()
# Remove the word 'County' & capitalize the name
# popc["CTYNAME"] = popc["CTYNAME"].str.replace("County", "").str.upper().replace(" ", "")
popc["CTYNAME"] = popc["CTYNAME"].str.rsplit(" ", 1)
popc["CTYNAME"] = popc["CTYNAME"].str[0]
popc["CTYNAME"] = popc["CTYNAME"].str.upper()
# popc["CTYNAME"] = popc["CTYNAME"].str.upper()
popc.head()
# Only keep the four digits for year
popc["Year"] = popc["Year"].str[-4:].astype(int)
# Remove unnecessary columns for population
drop = ["SUMLEV", "REGION", "DIVISION", "STATE", "COUNTY"]
popc1 = popc.drop(drop, axis=1)
# Replace 'DEWITT' with 'DE WITT'
popc1["CTYNAME"].replace("DEWITT", "DE WITT", inplace=True)
popc1[popc1["CTYNAME"] == "DE WITT"]
# Replace 'Doña Ana" with "DONA ANA"
popc1["CTYNAME"].replace("DOÑA ANA", "DONA ANA", inplace=True)
popc1[popc1["CTYNAME"] == "DONA ANA"]
# Replace 'ST" with "SAINT"
popc1["CTYNAME"].replace("ST\.", "SAINT", regex=True, inplace=True)
popc1[popc1["CTYNAME"] == "SAINT FRANCIS"]
# Replace 'SAINT JOHN THE BAPTIST" with "ST JOHN THE BAPTIST"
popc1["CTYNAME"].replace("SAINT JOHN THE BAPTIST", "ST JOHN THE BAPTIST", inplace=True)
popc1[popc1["CTYNAME"] == "ST JOHN THE BAPTIST"]
# Replace 'LASALLE" with "LA SALLE"
popc1["CTYNAME"].replace("LASALLE", "LA SALLE", inplace=True)
popc1[popc1["CTYNAME"] == "LA SALLE"]
# Replace 'DESOTO" with "DE SOTO"
popc1["CTYNAME"].replace("DESOTO", "DE SOTO", inplace=True)
popc1[popc1["CTYNAME"] == "DE SOTO"]
# Extract years from 2006~2012
popc2 = popc1[popc1.Year.isin([2006, 2007, 2008, 2009.2010, 2011, 2012])]
# Left Join Shipment & Population
merge = pd.merge(
    ship,
    popc1,
    how="left",
    left_on=["BUYER_COUNTY", "Year", "FULL_STATES"],
    right_on=["CTYNAME", "Year", "STNAME"],
)
# Look for null values
merge[merge["CTYNAME"].isnull()]
# Drop duplicated Columns
merge = merge.drop(["CTYNAME", "STNAME"], axis=1)
# Create a column call MME/CAP
merge["MME/CAP"] = round(merge["MME"] / merge["Population"], 4)
merge.head()
# Group by state and county then count the number of values
merge["checker"] = merge.groupby(["BUYER_STATE", "BUYER_COUNTY"], as_index=False)[
    ["YEAR/MONTH"]
].transform("count")
# Dop unnecessary columns
merge1 = merge.drop(["Year", "MME", "Population"], axis=1)
# For FL, LA, MS, SC the count should be equal to 7
# Subset dataframe that has incomplete values
missing1 = merge1[
    (merge1["checker"] != 7) & (merge1.BUYER_STATE.isin(["FL", "LA", "MS", "SC"]))
]
missing1.shape
# Removed the 6 "incomplete" rows
merge_clean = merge1[
    ~((merge1["checker"] != 7) & (merge1.BUYER_STATE.isin(["FL", "LA", "MS", "SC"])))
]
merge_clean.shape
# For the rest of states the count should be equal to 84
# Subset dataframe that has incomplete values
missing2 = merge_clean[
    (merge_clean["checker"] != 84)
    & (~merge_clean.BUYER_STATE.isin(["FL", "LA", "MS", "SC"]))
]
# Removed the 1989 "incomplete" rows
merge_clean2 = merge_clean[
    ~(
        (merge_clean["checker"] != 84)
        & (~merge_clean.BUYER_STATE.isin(["FL", "LA", "MS", "SC"]))
    )
]
# Calculate the years that are not present
Complete = [2006, 2007, 2008, 2009, 2010, 2011, 2012]
Missing = {}
for i in missing1["BUYER_COUNTY"].unique():
    present = []
    for j in range(len(missing1.index)):
        if missing1.iloc[j, 1] == i:
            present.append(missing1.iloc[j, 2])
    mis = np.setdiff1d(Complete, present).tolist()
    Missing.update({i: mis})
# Create empty rows for the missing years
for key, value in Missing.items():
    for year in value:
        df = pd.DataFrame(
            [[np.nan, key, year, np.nan, 0, np.nan]],
            columns=[
                "BUYER_STATE",
                "BUYER_COUNTY",
                "YEAR/MONTH",
                "FULL_STATES",
                "MME/CAP",
                "checker",
            ],
        )
        missing1 = pd.concat([missing1, df], ignore_index=False)
# Fill Missing States
missing1["BUYER_STATE"] = missing1.groupby("BUYER_COUNTY")["BUYER_STATE"].transform(
    lambda v: v.fillna(method="ffill")
# Fill Missing Full States
missing1["FULL_STATES"] = missing1.groupby("BUYER_COUNTY")["FULL_STATES"].transform(
    lambda v: v.fillna(method="ffill")
)
# Fill Missing Full Checker
missing1["checker"] = missing1.groupby("BUYER_COUNTY")["checker"].transform(
    lambda v: v.fillna(method="ffill")
)

#Create a complete date list
dates = []
for i in merge_clean[
    (merge_clean["BUYER_COUNTY"] == "ADAMS") & (merge_clean["BUYER_STATE"] == "WA")
]["YEAR/MONTH"]:
    dates.append(i)
# Calculate the months that are not present
Complete2 = dates
Missing2 = {}
for i in missing2["BUYER_COUNTY"].unique():
    present = []
    for j in range(len(missing2.index)):
        if missing2.iloc[j, 1] == i:
            present.append(missing2.iloc[j, 2])
    mis = np.setdiff1d(Complete2, present).tolist()
    Missing2.update({i: mis})
# Create empty rows for the missing months
for key, value in Missing2.items():
    for year in value:
        df = pd.DataFrame(
            [[np.nan, key, year, np.nan, 0, np.nan]],
            columns=[
                "BUYER_STATE",
                "BUYER_COUNTY",
                "YEAR/MONTH",
                "FULL_STATES",
                "MME/CAP",
                "checker",
            ],
        )
        missing2 = pd.concat([missing2, df], ignore_index=False)
# Fill Missing States
missing2["BUYER_STATE"] = missing2.groupby("BUYER_COUNTY")["BUYER_STATE"].transform(
    lambda v: v.fillna(method="ffill")
)
# Fill Missing Full States
missing2["FULL_STATES"] = missing2.groupby("BUYER_COUNTY")["FULL_STATES"].transform(
    lambda v: v.fillna(method="ffill")
)
# Fill Missing Checker
missing2["checker"] = missing2.groupby("BUYER_COUNTY")["checker"].transform(
    lambda v: v.fillna(method="ffill")
)
# Concatenate all dataframes together
merge_final = pd.concat([merge_clean2, missing1], ignore_index=False)
merge_final = pd.concat([merge_final, missing2], ignore_index=False)
# Group by state and county then count the number of values again
merge_final["final_checker"] = merge_final.groupby(
    ["BUYER_STATE", "BUYER_COUNTY"], as_index=False
)[["YEAR/MONTH"]].transform("count")
# Check if there are any missing rows again
merge_final[
    (merge_final["final_checker"] != 7)
    & (merge_final.BUYER_STATE.isin(["FL", "LA", "MS", "SC"]))
]
# For the rest of states the count should be equal to 84
# Subset dataframe that has incomplete values
merge_final[
    (merge_final["final_checker"] != 84)
    & (~merge_final.BUYER_STATE.isin(["FL", "LA", "MS", "SC"]))
]
# Create a column call "PolicyState"
merge_final["PolicyState"] = (
    (merge_final["BUYER_STATE"] == "FL")
    | ((merge_final["BUYER_STATE"] == "TX"))
    | (merge_final["BUYER_STATE"] == "WA")
)
# Create a column call Post
merge_final["Post"] = (
    (
        (
            (merge["BUYER_STATE"] == "FL")
            | (merge["BUYER_STATE"] == "LA")
            | (merge["BUYER_STATE"] == "MS")
            | (merge["BUYER_STATE"] == "SC")
        )
        & (merge["Year"] >= 2010)
    )
    | (
        (
            (merge["BUYER_STATE"] == "TX")
            | (merge["BUYER_STATE"] == "AR")
            | (merge["BUYER_STATE"] == "NM")
            | (merge["BUYER_STATE"] == "KS")
        )
        & (merge["Year"] >= 2007)
    )
    | (
        (
            (merge["BUYER_STATE"] == "WA")
            | (merge["BUYER_STATE"] == "OR")
            | (merge["BUYER_STATE"] == "CO")
            | (merge["BUYER_STATE"] == "CA")
        )
        & (merge["Year"] >= 2012)
    )
)
# Convert to CSV
merge_final.to_csv(
    r"D:/Duke University (MIDS 2022)/Fall 2020/IDS 720/Team Project/SHIPMENT_merge_v2.csv",
    index=False,
    header=True,
)

