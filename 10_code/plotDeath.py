import pandas as pd
from plotnine import *

data = pd.read_csv('state_county_death.csv')
data.head()

data['YearDiff_FL'] = data['Year'] - 2010
data['YearDiff_TX'] = data['Year'] - 2007
data['YearDiff_WA'] = data['Year'] - 2012

# FL - Feb 2010
pre_FL = (ggplot(data[data['STATE'] == 'Florida'], aes(x = 'YearDiff_FL', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00034, label='Policy Change') +
        annotate('text', x = -5, y = 0.00034, label='95% confidence level') +
        labs(title="Pre-post Model Graph, Florida (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab("Overdose Death Per Capita")
)
pre_FL
ggsave(plot = pre_FL, filename = 'FL_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# TX - Jan 2007
pre_TX = (ggplot(data[data['STATE'] == 'Texas'], aes(x = 'YearDiff_TX', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.000625, label='Policy Change') +
        annotate('text', x = -3, y = 0.000632, label='95% confidence level') +
        labs(title="Pre-post Model Graph, Texas (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Per Capita') +
        xlim(-5, 7)
)
pre_TX
ggsave(plot = pre_TX, filename = 'TX_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# WA - Jan 2012
pre_WA = (ggplot(data[data['STATE'] == 'Washington'], aes(x = 'YearDiff_WA', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm', level = 0.90) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.0007, label='Policy Change') +
        annotate('text', x = -5, y = 0.0007, label='95% confidence level') +
        labs(title="Pre-post Model Graph, Washington (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Per Capita') +
        xlim(-7, 5)
)
pre_WA
ggsave(plot = pre_WA, filename = 'WA_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# FL - Feb 2010
# ['LA', 'MS', 'SC']
nearFL = data[data['STATE'].isin(['Louisiana', 'Mississippi', 'South Carolina'])].copy()
nearFL['STATE'] = "NearbyStates"
mergedFL = data[data['STATE'] == 'Florida'].append(nearFL, ignore_index = True)
diff_FL = (ggplot(mergedFL, aes(y='OverdoseProp', color = 'STATE')) +
        geom_smooth(mergedFL[(mergedFL['YEAR'] < 2010)], aes(x = 'YearDiff_FL'), method = 'lm', level = 0.95) +
        geom_smooth(mergedFL[(mergedFL['YEAR'] >= 2010)], aes(x = 'YearDiff_FL'), method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00053, label='Policy Change') +
        annotate('text', x = -5, y = 0.00054, label='95% confidence level') +
        labs(title="Diff-in-Diff Model Graph, Florida (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Per Capita')
)
diff_FL
ggsave(plot = diff_FL, filename = 'FL_diff_overdose', path = "C:/Users/renha/Desktop/graph")

# TX - Jan 2007
# ['AR', 'NM', 'KS']
data[data['STATE'] == 'Texas'].sort_values(by = 'OverdoseProp', ascending = False)
TXmean = data[(data['STATE'] == 'Texas') & (data['POP'] > 4000)]['OverdoseProp'].mean()
TXcounties = data[(data['STATE'] == 'Texas') & (data['POP'] <= 4000)]['COUNTY'].unique()
data.loc[data['COUNTY'].isin(TXcounties), "OverdoseProp" ] = TXmean

nearTX = data[data['STATE'].isin(['Arkansas', 'New Mexico', 'Kansas'])].copy()
nearTX['STATE'] = "NearbyStates"
nearTX.sort_values(by = 'OverdoseProp', ascending = False).head(500)

nearTXmean = nearTX[nearTX['POP'] > 5000]['OverdoseProp'].mean()
nearTXcounties = nearTX[nearTX['POP'] <= 5000]['COUNTY'].unique()
nearTX.loc[nearTX['COUNTY'].isin(nearTXcounties), "OverdoseProp" ] = nearTXmean
mergedTX = data[data['STATE'] == 'Texas'].append(nearTX, ignore_index = True)
diff_TX = (ggplot(mergedTX, aes(y='OverdoseProp', color = 'STATE')) +
        geom_smooth(mergedTX[(mergedTX['YEAR'] < 2007)], aes(x = 'YearDiff_TX'), method = 'lm', level = 0.95) +
        geom_smooth(mergedTX[(mergedTX['YEAR'] >= 2007)], aes(x = 'YearDiff_TX'), method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00067, label='Policy Change') +
        annotate('text', x = -3, y = 0.0007, label='95% confidence level') +
        labs(title="Diff-in-Diff Model Graph, Texas (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Per Capita') +
        xlim(-5, 10)
)
diff_TX
ggsave(plot = diff_TX, filename = 'TX_diff_overdose', path = "C:/Users/renha/Desktop/graph")

# WA - Jan 2012
# ['CO', 'OR', 'CA']
nearWA = data[data['STATE'].isin(['Colorado', 'Oregon', 'California'])].copy()
nearWA['STATE'] = "NearbyStates"
mergedWA = data[data['STATE'] == 'Washington'].append(nearWA, ignore_index = True)
diff_WA = (ggplot(mergedWA, aes(y='OverdoseProp', color = 'STATE')) +
        geom_smooth(mergedWA[(mergedWA['YEAR'] < 2012)], aes(x = 'YearDiff_WA'), method = 'lm') +
        geom_smooth(mergedWA[(mergedWA['YEAR'] >= 2012)], aes(x = 'YearDiff_WA'), method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.0011, label='Policy Change') +
        annotate('text', x = -5, y = 0.0011, label='95% confidence level') +
        labs(title="Diff-in-Diff Model Graph, Washington (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Per Capita') +
        xlim(-7, 5)
)
diff_WA
ggsave(plot = diff_WA, filename = 'WA_diff_overdose', path = "C:/Users/renha/Desktop/graph")
