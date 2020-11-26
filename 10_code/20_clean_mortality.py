import pandas as pd
from zipfile import ZipFile
import re

# read mortality data
original_zip = ZipFile('../00_source/US_VitalStatistics.zip', 'r')
new_zip = ZipFile('new_archve.zip', 'w')
for item in original_zip.infolist():
    buffer = original_zip.read(item.filename)
    if not str(item.filename).startswith('__MACOSX/'):
        new_zip.writestr(item, buffer)
new_zip.close()
original_zip.close()

new_zip = ZipFile('new_archve.zip', 'r')

dfs = {}

for text_file in new_zip.infolist():
    dfs[re.search('2\d\d\d', text_file.filename).group(0)] = pd.read_csv(new_zip.open(text_file.filename), sep = "\t", usecols = [1, 2, 3, 5, 7])[:-15]

new_zip.close()
!rm new_archve.zip

dfs.keys()
origin = pd.DataFrame({})
for key in dfs.keys():
    origin = origin.append(dfs[key])
    pass

# check whihc county has missing value
origin[origin['Deaths'] == 'Missing']['County'].unique()
# index_names = origin[origin['Deaths'] == 'Missing'].index
# origin = origin.drop(index_names)

# replace missing value with 10
origin['Deaths'] = origin['Deaths'].replace('Missing', 10)

origin['Deaths'] = origin['Deaths'].astype('int64')
origin['Year'] = origin['Year'].astype('int64')
origin['County Code'] = origin['County Code'].astype('int64')

# convert abbreviation to full name
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
origin['State'] = origin['State'].map(states)

# group by and sum overdose death
names = []
for name in origin['Drug/Alcohol Induced Cause'].unique():
    if re.match('Drug poisonings.*', name):
        names.append(name)
        pass
    pass

interDose = origin[origin['Drug/Alcohol Induced Cause'].isin(names)].copy()
finalDose = interDose.groupby(['State', 'County', 'Year'], as_index = False).sum()[['State', 'County', 'Year', 'Deaths']].rename({'Deaths':'TotalOverdose'}, axis = 'columns').copy()

# subset population dataset
pop = pd.read_csv('../20_intermediate_files/FinalPopDataset.csv')
states = finalDose.State.unique().copy()
subPop = pop[pop['STATE'].isin(states) & (pop['YEAR'] >= 2003) & (pop['YEAR'] <= 2015)].reset_index(drop = True).copy()
index_names = subPop[subPop['COUNTY'].isin(states)].index
subPop = subPop.drop(index_names)

final = pd.merge(subPop, finalDose, how = 'left', left_on = ['STATE', 'COUNTY', 'YEAR'], right_on = ['State', 'County', 'Year'], indicator = True)
final.value_counts('_merge')

final.drop(['County', 'Year', 'State'], axis = 1, inplace = True)
final['TotalOverdose'] = final['TotalOverdose'].fillna(0)
final.loc[final.TotalOverdose == 0, "TotalOverdose" ] = 10
final.loc[final.COUNTY == 'Loving County', "TotalOverdose" ] = 1
final.loc[final.COUNTY == 'King County', "TotalOverdose" ] = 1
final.loc[final.POP < 1000, "TotalOverdose" ] = 1
state_county = {}

# calculate overdose death
final.drop('_merge', axis = 1, inplace = True)
final['OverdoseProp'] = final['TotalOverdose'] / final['POP']
final['PolicyState'] = (final['STATE'] == 'Florida') | ((final['STATE'] == 'Texas')) | (final['STATE'] == 'Washington')
nearFL = ['Florida', 'Louisiana', 'Mississippi', 'South Carolina']
nearTX = ['Texas', 'Arkansas', 'New Mexico', 'Kansas']
nearWA = ['Washington', 'Colorado', 'Oregon', 'California']
final['Post'] = ((final['STATE'].isin(nearFL)) & (final['YEAR'] >= 2010)) | ((final['STATE'].isin(nearTX)) & (final['YEAR'] >= 2007)) | ((final['STATE'].isin(nearWA)) & (final['YEAR'] >= 2012))
len(final[final['STATE'] == 'Texas']['COUNTY'].unique())
final.to_csv('../20_intermediate_files/state_county_death.csv', index = False)

'''This is the loop before simplification'''
#deathTypes = origin['Drug/Alcohol Induced Cause'].unique().copy()
#years = final.YEAR.unique().copy()

#years = sorted(origin['Year'].unique()).copy()
#final = final[final['STATE'].isin(states) & (final['YEAR'] >= 2003) & (final['YEAR'] <= 2015)].reset_index(drop = True).copy()

#state_county = {}

#for state in states:
#    counties = final[final['STATE'] == state]['COUNTY'].unique().copy()
#    state_county[state] = counties
#    pass

#for state, counties in state_county.items():
#    for county in counties: 
#        for year in years:
#            window = final[(final['STATE'] == state) & (final['COUNTY'] == county) & (final['YEAR'] == year)].copy()
#            population = window['POP'].iloc[0]
#            for death in deathTypes:
#                existingDeath = window['Drug/Alcohol Induced Cause'].unique()
#                if death not in existingDeath:
#                    new_row = {'STATE':state, 'COUNTY':county, 'YEAR':year, 'POP':population, 'Drug/Alcohol Induced Cause':death, 'Deaths':0, '_merge':'Missing'}
#                    final = final.append(new_row, ignore_index=True).copy()

#sub = final.copy()
#index_names = sub[sub['_merge'] == 'left_only'].index
#sub = sub.drop(index_names)
#sub.value_counts('_merge')
#sub.drop('_merge', axis = 1, inplace = True)