import pandas as pd

# Produced and Import Prices
#https://www.bfs.admin.ch/bfs/en/home/statistiken/prices/producer-prices-import-prices/total-offer.html
ch_ppi = pd.read_excel('https://www.bfs.admin.ch/bfsstatic/dam/assets/21424933/master',
                       header=6,index_col='Datum').iloc[73:-13,2:-2]
ch_ppi = ch_ppi.replace('...',np.nan)
ch_ppi.index = pd.to_datetime(ch_ppi.index)

# CPI
#https://www.bfs.admin.ch/bfs/en/home/statistics/prices/consumer-price-index.html
ch_cpi = pd.read_excel('https://www.bfs.admin.ch/bfsstatic/dam/assets/21484861/master',header=3,index_col='Datum / Date').iloc[:-2,:]
ch_cpi.columns = ['Jun 1914=100', 'Aug 1939=100', 'Sep 1966=100', 'Sep 1977=100', 'Dec 1982=100',
                  'May 1993=100','May 2000=100','Dec 2005=100','Dec 2010=100','Dec 2015=100',
                  'Dec 2020=100','% m/m','% y/y']