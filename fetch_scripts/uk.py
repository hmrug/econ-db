import requests
import pandas as pd

## Office for National Statistics

## Retail Sales Index
def retail_index():
    gb_retail_url = 'https://www.ons.gov.uk/file?uri=%2fbusinessindustryandtrade%2fretailindustry%2fdatasets%2fretailsalesindexreferencetables%2fcurrent/rsireferencetables.xlsx'
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"} #change the version of the browser accordingly

    resp = requests.get(gb_retail_url, headers = hdr)

    gb_retail = pd.read_excel(resp.content,sheet_name='CPSA',header=6).set_index('Time Period').iloc[2:]
    gb_retail_cols = ['All retailing including automotive fuel', 'All retailing excluding automotive fuel', 'Predominantly food stores',
                      'Total of predominantly non-food stores', 'Non-specialised stores', 'Textile, clothing and footwear stores',
                      'Household goods stores', 'Other stores', 'Non-store retailing', 'Predominantly automotive fuel']
    gb_retail.columns = gb_retail_cols

    gb_retail_nums = gb_retail.loc[:'Revision to index numbers'].iloc[:-2]
    gb_retail_nums.index = pd.to_datetime(gb_retail_nums.index).strftime('%b %Y')

    return gb_retail_nums,gb_retail_revisions

def retail_index_revisions():
    gb_retail_url = 'https://www.ons.gov.uk/file?uri=%2fbusinessindustryandtrade%2fretailindustry%2fdatasets%2fretailsalesindexreferencetables%2fcurrent/rsireferencetables.xlsx'
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"} #change the version of the browser accordingly

    resp = requests.get(gb_retail_url, headers = hdr)

    gb_retail = pd.read_excel(resp.content,sheet_name='CPSA',header=6).set_index('Time Period').iloc[2:]
    gb_retail_cols = ['All retailing including automotive fuel', 'All retailing excluding automotive fuel', 'Predominantly food stores',
                      'Total of predominantly non-food stores', 'Non-specialised stores', 'Textile, clothing and footwear stores',
                      'Household goods stores', 'Other stores', 'Non-store retailing', 'Predominantly automotive fuel']
    gb_retail.columns = gb_retail_cols

    gb_retail_revisions= gb_retail.loc['Revision to index numbers':]
    gb_retail_revisions = gb_retail_revisions.iloc[4:,:]
    gb_retail_revisions.index = pd.to_datetime(gb_retail_revisions.index).strftime('%b %Y')
    return gb_retail_revisions

## CPI
def cpi_db():
    url = 'https://www.ons.gov.uk/file?uri=/economy/inflationandpriceindices/datasets/consumerpriceindices/current/mm23.csv'
    storage_options = {'User-Agent': 'Mozilla/5.0'}
    cpi = pd.read_csv(url, storage_options=storage_options,index_col='Title')
    cpi = cpi.T.reset_index().T
    cpi.columns = cpi.iloc[1,:]
    return cpi

def cpi_indices(kind):
    cpi = cpi_db()
    index_ids = ['D7BT','D7BU','D7BV','D7BW','D7BX','D7BY','D7BZ','D7C2','D7C3','D7C4','D7C5','D7C6','D7C7','D7F4','D7F5','DKC6','L522']
    mm_ids = ['D7OE','D7JH','D7JI','D7JJ','D7JK','D7JL','D7JM','D7JN','D7JO','D7JP','D7JQ','D7JR','D7JS','D7MU','D7MV','DKI7','L59C']
    yy_ids = ['D7G7','D7G8','D7G9','D7GA','D7GB','D7GC','D7GD','D7GE','D7GF','D7GG','D7GH','D7GI','D7GJ','D7NM','D7NN','DKO8','L55O']
    cols = ['CPI', 'Food and non-alcoholic beverages', 'Alcoholic beverages and tobacco', 'Clothing and footwear',
            'Housing, water, electricity, gas and other fuels','Furniture, household equipment and maintenance','Health','Transport',
            'Communication','Recreation and culture','Education','Restaurants and hotels,','Misc goods and services',
            'All goods', 'All services', 'All items CPI ex Energy, food, alcoholic beverages and tobacco','CPIH']
    if kind=='index':
        df = cpi.loc[:,index_ids]
    elif kind=='mm':
        df = cpi.loc[:,mm_ids]
    elif kind=='yy':
        df = cpi.loc[:,yy_ids]
    df = df.T.set_index('index').T
    df.columns = cols
    df = df.iloc[6:,:]#.dropna()
    df = df.loc['1947 JUN':]
    df.index = pd.to_datetime(df.index).strftime('%b %Y')
    df.index.name = 'Date'
    return df

## GDP
## Employment
## Unemployment