# load packages
import pandas as pd
import numpy as np

# load in data from source folder
pop_2000_2009 = pd.read_csv(
    "../00_source/CensusEstimates2000-2010.csv", encoding="latin-1"
)
pop_2010_2019 = pd.read_csv(
    "../00_source/CensusEstimates2010-2019.csv", encoding="latin-1"
)

# Select state name, county name, and 2000-2009 population estimates
pop_2000_2009 = pop_2000_2009[
    [
        "STNAME",
        "CTYNAME",
        "POPESTIMATE2000",
        "POPESTIMATE2001",
        "POPESTIMATE2002",
        "POPESTIMATE2003",
        "POPESTIMATE2004",
        "POPESTIMATE2005",
        "POPESTIMATE2006",
        "POPESTIMATE2007",
        "POPESTIMATE2008",
        "POPESTIMATE2009",
    ]
]

# Select state name, county name, and 2010-2019 population estimates
pop_2010_2019 = pop_2010_2019[
    [
        "STNAME",
        "CTYNAME",
        "CENSUS2010POP",
        "POPESTIMATE2011",
        "POPESTIMATE2012",
        "POPESTIMATE2013",
        "POPESTIMATE2014",
        "POPESTIMATE2015",
        "POPESTIMATE2016",
        "POPESTIMATE2017",
        "POPESTIMATE2018",
        "POPESTIMATE2019",
    ]
]

# Rename the 2010 census population column so it ends in the year
pop_2010_2019.rename(columns={"CENSUS2010POP": "CENSUS2010"}, inplace=True)

# Drop duplicated rows from both datasets
pop_2000_2009.drop(328, inplace=True)
pop_2010_2019.drop(328, inplace=True)

# Test to ensure no duplicate rows in either dataset
assert not pop_2000_2009.duplicated().any()
assert not pop_2010_2019.duplicated().any()

# Convert population estimate columns to rows for State/County combinations
pop_00_09 = pd.melt(pop_2000_2009, ["STNAME", "CTYNAME"])
pop_10_19 = pd.melt(pop_2010_2019, ["STNAME", "CTYNAME"])

# Test to ensure no duplicates were introduced
assert not pop_00_09.duplicated().any()
assert not pop_10_19.duplicated().any()

# Rename population column to "POP", and year column to "YEAR"
pop_00_09.rename(columns={"variable": "YEAR", "value": "POP"}, inplace=True)
pop_10_19.rename(columns={"variable": "YEAR", "value": "POP"}, inplace=True)

# Convert values in "YEAR" column to year (year is last 4 characters)
pop_00_09["YEAR"] = pop_00_09["YEAR"].apply(lambda x: x[-4:])
pop_10_19["YEAR"] = pop_10_19["YEAR"].apply(lambda x: x[-4:])

# Test to ensure full representation of our target states in both datasets
states = ["Florida", "Texas", "Washington"]
for state in states:
    len1 = len(pop_00_09[pop_00_09["STNAME"] == state])
    len2 = len(pop_10_19[pop_10_19["STNAME"] == state])
    assert len1 == len2

# ############################################################
# Shannon County, SD -> Oglala Lakota County (2015)
# Need to correct La Salle Parish, LA to LaSalle Parish, LA
# Wade Hampton Census Area, AK -> Kusilvak Census Area, AK (2010)
# Petersburg Census Area, AK -> Petersburg Borough, AK
# Bedford City, VA incorporated into Bedford County, VA (2013)
# ############################################################

# Assign replacements for the name changes between two census (2010 correct)
replacements = [
    ("Virginia", ("Bedford city", "Bedford County")),
    ("South Dakota", ("Shannon County", "Oglala Lakota County")),
    ("Louisiana", ("La Salle Parish", "LaSalle Parish")),
    ("Alaska", ("Wade Hampton Census Area", "Kusilvak Census Area")),
    ("Alaska", ("Petersburg Census Area", "Petersburg Borough")),
]
# Replace the old names with the new names
for item in replacements:
    state, county = item
    old, new = county
    pop_00_09.loc[
        (pop_00_09["CTYNAME"] == old) & (pop_00_09["STNAME"] == state), "CTYNAME"
    ] = new

# Ensure the newly named groups are grouped correctly
pop_00_09 = pop_00_09.groupby(["STNAME", "CTYNAME", "YEAR"]).sum()
pop_00_09.reset_index(inplace=True)

# Test to ensure the two datasets are 1:1 for State/County combination
merge = pd.merge(
    pop_00_09, pop_10_19, on=["STNAME", "CTYNAME"], how="outer", indicator=True
)
assert merge[merge["_merge"] != "both"].isnull().all().all()

# Append 2010-2019 data onto 2000-2009 data
pop_00_19 = pop_00_09.append(pop_10_19)
pop_00_19 = pop_00_19.groupby(["STNAME", "CTYNAME", "YEAR"]).sum().reset_index()
assert not pop_00_19.duplicated().any()

# Rename columns
pop_00_19.rename(columns={"STNAME": "STATE", "CTYNAME": "COUNTY"}, inplace=True)

# Export as csv to intermediate files folder
pop_00_19.to_csv("../20_intermediate_files/FinalPopDataset.csv", index=False)
