import pandas as pd
from plotnine import *

data = pd.read_csv('state_death.csv')
data.head()

data['YearDiff_FL'] = data['Year'] - 2010
data['YearDiff_TX'] = data['Year'] - 2007
data['YearDiff_WA'] = data['Year'] - 2012

# FL - Feb 2010
pre_FL = (ggplot(data[data['State'] == 'FL'], aes(x = 'YearDiff_FL', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.013, label='Policy Change') +
        labs(title='Pre-post Model Graph, Florida') +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion')
)
ggsave(plot = pre_FL, filename = 'FL_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# TX - Jan 2007
pre_TX = (ggplot(data[data['State'] == 'TX'], aes(x = 'YearDiff_TX', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.013, label='Policy Change') +
        labs(title='Pre-post Model Graph, Texas') +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-5, 7)
)
ggsave(plot = pre_TX, filename = 'TX_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# WA - Jan 2012
pre_WA = (ggplot(data[data['State'] == 'WA'], aes(x = 'YearDiff_WA', y='OverdoseProp', color = 'Post')) +
        geom_smooth(method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.013, label='Policy Change') +
        labs(title='Pre-post Model Graph, Washington') +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-7, 5)
)
ggsave(plot = pre_WA, filename = 'WA_pre_overdose', path = "C:/Users/renha/Desktop/graph")

# FL - Feb 2010
# ['LA', 'MS', 'SC']
nearFL = data[data['State'].isin(['LA', 'MS', 'SC'])]
avgNearFL = nearFL.groupby('Year', as_index = False).mean().drop('OverdoseProp', axis = 1)
avgNearFL['OverdoseProp'] = avgNearFL['TotalOverdose'] / avgNearFL['TotalDeath']
avgNearFL['State'] = 'NearbyStates'
mergedFL = data[data['State'] == 'FL'].append(avgNearFL, ignore_index = True)
diff_FL = (ggplot(mergedFL, aes(y='OverdoseProp', color = 'State')) +
        geom_smooth(mergedFL[(mergedFL['Year'] < 2010)], aes(x = 'YearDiff_FL'), method = 'lm') +
        geom_smooth(mergedFL[(mergedFL['Year'] >= 2010)], aes(x = 'YearDiff_FL'), method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.013, label='Policy Change') +
        labs(title='Diff-in-Diff Model Graph, Florida') +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion')
)
ggsave(plot = diff_FL, filename = 'FL_diff_overdose', path = "C:/Users/renha/Desktop/graph")

# TX - Jan 2007
# ['AR', 'NM', 'KS']
nearTX = data[data['State'].isin(['AR', 'NM', 'KS'])]
avgNearTX = nearTX.groupby('Year', as_index = False).mean().drop('OverdoseProp', axis = 1)
avgNearTX['OverdoseProp'] = avgNearTX['TotalOverdose'] / avgNearTX['TotalDeath']
avgNearTX['State'] = 'NearbyStates'
mergedTX = data[data['State'] == 'TX'].append(avgNearTX, ignore_index = True)
diff_TX = (ggplot(mergedTX, aes(y='OverdoseProp', color = 'State')) +
        geom_smooth(mergedTX[(mergedTX['Year'] < 2007)], aes(x = 'YearDiff_TX'), method = 'lm') +
        geom_smooth(mergedTX[(mergedTX['Year'] >= 2007)], aes(x = 'YearDiff_TX'), method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.016, label='Policy Change') +
        labs(title='Diff-in-Diff Model Graph, Texas') +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-5, 10)
)
ggsave(plot = diff_TX, filename = 'TX_diff_overdose', path = "C:/Users/renha/Desktop/graph")

# WA - Jan 2012
# ['CO', 'OR', 'CA']
nearWA = data[data['State'].isin(['CO', 'OR', 'CA'])]
avgNearWA = nearWA.groupby('Year', as_index = False).mean().drop('OverdoseProp', axis = 1)
avgNearWA['OverdoseProp'] = avgNearWA['TotalOverdose'] / avgNearWA['TotalDeath']
avgNearWA['State'] = 'NearbyStates'
mergedWA = data[data['State'] == 'WA'].append(avgNearWA, ignore_index = True)
diff_WA = (ggplot(mergedWA, aes(y='OverdoseProp', color = 'State')) +
        geom_smooth(mergedWA[(mergedWA['Year'] < 2012)], aes(x = 'YearDiff_WA'), method = 'lm') +
        geom_smooth(mergedWA[(mergedWA['Year'] >= 2012)], aes(x = 'YearDiff_WA'), method = 'lm') +
        geom_vline(xintercept=0, show_legend = 'Policy Change') +
        annotate('text', x = 0, y = 0.014, label='Policy Change') +
        labs(title='Diff-in-Diff Model Graph, Washington') +
        xlab('Years from Policy Change') +
        ylab('Overdose Death Proportion') +
        xlim(-10, 5)
)
ggsave(plot = diff_WA, filename = 'WA_diff_overdose', path = "C:/Users/renha/Desktop/graph")
