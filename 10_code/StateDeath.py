import pandas as pd
from zipfile import ZipFile
import re

original_zip = ZipFile('US_VitalStatistics.zip', 'r')
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

totalDeath = origin.groupby(['County','Year','County Code'], as_index = False).sum()[['County','County Code','Year','Deaths']].rename({'Deaths':'TotalDeath'}, axis = 'columns')

names = []
for name in origin['Drug/Alcohol Induced Cause'].unique():
    if re.match('Drug poisonings.*', name):
        names.append(name)
        pass
    pass

interDose = origin[origin['Drug/Alcohol Induced Cause'].isin(names)]
finalDose = interDose.groupby(['County', 'County Code', 'Year'], as_index = False).sum()[['County','County Code','Year','Deaths']].rename({'Deaths':'TotalOverdose'}, axis = 'columns')

death = pd.merge(finalDose, totalDeath, on = ['County', 'County Code', 'Year'], validate='1:1', indicator = True)
death[['County','State']] = death.County.str.split(", ",expand=True,)

# ensure that every row has a corresponding row in the other dataframe
death._merge.value_counts()
death.drop(['_merge', 'County Code'], axis = 1, inplace = True)

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
death['State'] = death['State'].map(states)

# import population dataset
pop = pd.read_csv('FinalPopDataset.csv')
final = pd.merge(death, pop, left_on = ['State', 'County', 'Year'], right_on = ['STATE', 'COUNTY', 'YEAR'], validate='1:1', indicator = True)

# ensure that every row has a corresponding row in the other dataframe
final._merge.value_counts()
final.drop(['STATE', 'YEAR', 'COUNTY', '_merge'], axis = 1, inplace = True)

final['OverdoseProp'] = final['TotalOverdose'] / final['POP']

final['PolicyState'] = (final['State'] == 'Florida') | ((final['State'] == 'Texas')) | (final['State'] == 'Washington')

nearFL = ['Florida', 'Louisiana', 'Mississippi', 'South Carolina']
nearTX = ['Texas', 'Arkansas', 'New Mexico', 'Kansas']
nearWA = ['Washington', 'Colorado', 'Oregon', 'California']

final['Post'] = ((final['State'].isin(nearFL)) & (final['Year'] >= 2010)) | ((final['State'].isin(nearTX)) & (final['Year'] >= 2007)) | ((final['State'].isin(nearWA)) & (final['Year'] >= 2012))
final.to_csv('state_county_death.csv', index = False)
