import pandas as pd
from plotnine import *

data = pd.read_csv('state_county_death.csv')
data.head()

data['YearDiff_FL'] = data['Year'] - 2010
data['YearDiff_TX'] = data['Year'] - 2007
data['YearDiff_WA'] = data['Year'] - 2012

# FL - Feb 2010
pre_FL = (ggplot(data[data['State'] == 'Florida'], aes(x = 'YearDiff_FL', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00013, label='Policy Change') +
        annotate('text', x = -5, y = 0.00018, label='95% confidence level') +
        labs(title="Pre-post Model Graph, Florida (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab("Overdose Death Proportion")
)
pre_FL
ggsave(plot = pre_FL, filename = 'FL_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# TX - Jan 2007
pre_TX = (ggplot(data[data['State'] == 'Texas'], aes(x = 'YearDiff_TX', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00008, label='Policy Change') +
        annotate('text', x = -3, y = 0.00014, label='95% confidence level') +
        labs(title="Pre-post Model Graph, Texas (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-5, 7)
)
pre_TX
ggsave(plot = pre_TX, filename = 'TX_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# WA - Jan 2012
pre_WA = (ggplot(data[data['State'] == 'Washington'], aes(x = 'YearDiff_WA', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00013, label='Policy Change') +
        annotate('text', x = -5, y = 0.00016, label='95% confidence level') +
        labs(title="Pre-post Model Graph, Washington (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-7, 5)
)
pre_WA
ggsave(plot = pre_WA, filename = 'WA_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# FL - Feb 2010
# ['LA', 'MS', 'SC']
nearFL = data[data['State'].isin(['Louisiana', 'Mississippi', 'South Carolina'])]
avgNearFL = nearFL.groupby('Year', as_index = False).mean().drop('OverdoseProp', axis = 1)
avgNearFL['OverdoseProp'] = avgNearFL['TotalOverdose'] / avgNearFL['POP']
avgNearFL['State'] = 'NearbyStates'
mergedFL = data[data['State'] == 'Florida'].append(avgNearFL, ignore_index = True)
diff_FL = (ggplot(mergedFL, aes(y='OverdoseProp', color = 'State')) +
        geom_smooth(mergedFL[(mergedFL['Year'] < 2010)], aes(x = 'YearDiff_FL'), method = 'lm', level = 0.95) +
        geom_smooth(mergedFL[(mergedFL['Year'] >= 2010)], aes(x = 'YearDiff_FL'), method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00010, label='Policy Change') +
        annotate('text', x = -5, y = 0.00018, label='95% confidence level') +
        labs(title="Diff-in-Diff Model Graph, Florida (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion')
)
diff_FL
ggsave(plot = diff_FL, filename = 'FL_diff_overdose', path = "C:/Users/renha/Desktop/graph")

# TX - Jan 2007
# ['AR', 'NM', 'KS']
nearTX = data[data['State'].isin(['Arkansas', 'New Mexico', 'Kansas'])]
avgNearTX = nearTX.groupby('Year', as_index = False).mean().drop('OverdoseProp', axis = 1)
avgNearTX['OverdoseProp'] = avgNearTX['TotalOverdose'] / avgNearTX['POP']
avgNearTX['State'] = 'NearbyStates'
mergedTX = data[data['State'] == 'Texas'].append(avgNearTX, ignore_index = True)
diff_TX = (ggplot(mergedTX, aes(y='OverdoseProp', color = 'State')) +
        geom_smooth(mergedTX[(mergedTX['Year'] < 2007)], aes(x = 'YearDiff_TX'), method = 'lm', level = 0.95) +
        geom_smooth(mergedTX[(mergedTX['Year'] >= 2007)], aes(x = 'YearDiff_TX'), method = 'lm', level = 0.95) +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00008, label='Policy Change') +
        annotate('text', x = -3, y = 0.00018, label='95% confidence level') +
        labs(title="Diff-in-Diff Model Graph, Texas (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-5, 10)
)
diff_TX
ggsave(plot = diff_TX, filename = 'TX_diff_overdose', path = "C:/Users/renha/Desktop/graph")

# WA - Jan 2012
# ['CO', 'OR', 'CA']
nearWA = data[data['State'].isin(['Colorado', 'Oregon', 'California'])]
avgNearWA = nearWA.groupby('Year', as_index = False).mean().drop('OverdoseProp', axis = 1)
avgNearWA['OverdoseProp'] = avgNearWA['TotalOverdose'] / avgNearWA['POP']
avgNearWA['State'] = 'NearbyStates'
mergedWA = data[data['State'] == 'Washington'].append(avgNearWA, ignore_index = True)
diff_WA = (ggplot(mergedWA, aes(y='OverdoseProp', color = 'State')) +
        geom_smooth(mergedWA[(mergedWA['Year'] < 2012)], aes(x = 'YearDiff_WA'), method = 'lm') +
        geom_smooth(mergedWA[(mergedWA['Year'] >= 2012)], aes(x = 'YearDiff_WA'), method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.00009, label='Policy Change') +
        annotate('text', x = -7, y = 0.00018, label='95% confidence level') +
        labs(title="Diff-in-Diff Model Graph, Washington (State-County-Year-Level)") +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-10, 5)
)
diff_WA
ggsave(plot = diff_WA, filename = 'WA_diff_overdose', path = "C:/Users/renha/Desktop/graph")
