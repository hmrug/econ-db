#!/usr/bin/env python
# --- Economic data: U.S. ---
# --- Autor: Hubert Mrugala (hubertmrugala.com) ---

import numpy as np
import pandas as pd
import datetime as dt

# CENSUS
# US Census datasets: https://www.census.gov/econ/currentdata/datasets/index

def inventories():
    """
    CENSUS | Manufacturing and Trade Inventories, sa
    Latest release: https://www.census.gov/mtis/index.html
    Release date: Around 14th each month
    """
    inv = pd.read_excel('https://www.census.gov/mtis/www/data/text/timeseries1.xlsx').iloc[14:-1,:]
    
    month_start = inv.iloc[-1,0][:3]
    year_start = inv.iloc[-1,1]
    month_end = inv.iloc[0,0][:3]
    year_end =inv.iloc[0,1]
    inv_start = dt.datetime.strptime(str(month_start)+str(year_start),'%b%Y')
    inv_end = dt.datetime.strptime(str(month_end)+str(year_end),'%b%Y')+dt.timedelta(weeks=6)
    
    idx = pd.date_range(inv_start,inv_end,freq='M')
    idx = idx.sort_values(ascending=False)
    inv.index = idx
    
    inv = inv.iloc[:,2:]
    inv.columns = ['Total Business','Total Manufacturing','Retail Trade','Total Wholesalers']
    inv.index.name = 'Date'
    inv.sort_index(ascending=False)
    return inv.iloc[::-1]

def retail():
    """
    CENSUS | Advanced Retail Trade (Sales), sa
    Latest release: https://www.census.gov/retail/index.html
    Release date: Around 16th each month
    """
    zip_url = 'https://www.census.gov/econ/currentdata/datasets/MARTS-mf.zip'
    content = requests.get(zip_url)
    file = ZipFile(BytesIO(content.content))
    #zf = zipfile.ZipFile('~/downloads/MARTS-mf.csv'') # an alternative
    # get name of the csv file inside of the zip folder
    # read the csv in 3 parts: dataset names, dates and actual values  
    cat_desc = pd.read_csv(file.open('MARTS-mf.csv'),delimiter=',',header=1,on_bad_lines='skip').iloc[:21,2]
    dates = pd.read_csv(file.open('MARTS-mf.csv'),delimiter=',',header=35,on_bad_lines='skip').iloc[:-5,:]['per_name']
    df = pd.read_csv(file.open('MARTS-mf.csv'),delimiter=',',header=402)

    names = list(cat_desc)

    start = dt.datetime.strptime(dates.iloc[0],'%b%Y')
    end = dt.datetime.strptime(dates.iloc[-1],'%b%Y')+dt.timedelta(weeks=6)
    data_range = pd.date_range(start,end,freq='M')

    l = []
    for i in range(1,22):
        df_i = df[df['cat_idx']==i]
        # seasonally adjusted values
        df_i = df_i[df_i['is_adj']==1]
        # no error (?)
        df_i = df_i[df_i['et_idx']==0]
        # nominal values
        df_i = df_i[df_i['dt_idx']==1]
        df_i.index = data_range
        l.append(df_i.iloc[:,-1])

    df_all =pd.concat(l,axis=1).sort_index(ascending=False)
    df_all.columns = names
    return df_all.iloc[::-1]


# ISM | Composite PMI
# Latest release: https://www.census.gov/mtis/index.html
# Release date: Around 14th each month

quandl.get("ISM/MAN_PMI")

## BLS

# Core CPI
# core_cpi = pdr.DataReader('CPILFESL','fred')
#
# item_codes_df = pd.read_table('https://download.bls.gov/pub/time.series/cu/cu.item')
# ic = item_codes_df[item_codes_df['item_name'].isin(lst_2)].iloc[:,:-3]
# ic_lst = [i for i in ic['item_code']]
# lst_1 = ['All items','Commodities','Services','Food','Food at home','Food away from home',
#          'Energy','Energy commodities','Energy services','All items less food and energy',
#          'Commodities less food and energy commodities','Services less energy services',
#          'Commodities less food, energy, and used cars and trucks']
#
# codes = []
# for i in range(len(ic_lst)):
#     cd = cpi_code_base+ic_lst[i]
#     codes.append(cd)
#     
# df = pd.DataFrame()
#
# for series in json_data['Results']['series']:
#     x=prettytable.PrettyTable(["series id","year","periodName","value"])
#     seriesId = series['seriesID']
#     for item in series['data']:
#         year = item['year']
#         period = item['periodName']
#         value = item['value']
#         x.add_row([seriesId,year,period[:3],value])
#     # df.append(x)
#     # output = open('cpi_data/'+seriesId + '.txt','w')
#     # output.write (x.get_string())
#     # output.close()
    

## TIC
tic_positions = pd.read_html('https://home.treasury.gov/news/press-releases/jy0559')[0].iloc[6:-20,5].dropna()
tic_positions = [i for i in tic_positions]

# Monthly Releases and Archives of Treasury International Capital (TIC) Data {Across-U.S. Border Financial Flows}
# TIC monthly reports on Cross-Border Portfolio Financial Flows
# ($ millions)
tic_monthly_all = pd.read_csv('https://treasury.gov/resource-center/data-chart-center/tic/Documents/npr_history.csv',
                  header=17,index_col='Unnamed: 0').dropna()
tic_monthly_all.index = pd.to_datetime(tic_monthly_all.index).strftime('%b \'%y')
tic_names = ['Gross Purch. of Domes. US L-T Secur.','Gross Foreign Sales of Domes. US L-T Secur.',
               'Domes L-T Secur. Purch., net','Private, net','Private Treas Bonds & Notes, net','Private Gov\'t Agency Bonds, net',
               'Private Corp Bonds, net','Private Equities, net','Official, net','Official Treas Bonds & Notes, net',
               'Official Gov\'t Agency Bonds, net','Official Corp Bonds, net	','Official Equities, net',
               'Gross Purch. of Foreign L-T Secur. from US',
              'Gross Foreign Sales of Foreign Secur. to US','Foreign L-T Securities Purch., net','Foreign Bonds Purch., net',
              'Foreign Equities Purch., net','Net L-T Secur. Transactions','Other Acquis. of L-T Secur., net ',
               'Net Foreign Acquis. of L-T Secur.',
               'Increase in Foreign Holdings of Dollar-denom S-T U.S. Sec. and Other Custody Liabs.',
               'U.S. Treasury Bills','Private, net','Official, net','Other Negot. Instr. & Select. Other Liabs.',
               'Private, net','Official, net','Change in Banks\' Own Net Dollar-denom. Liabs.',
               'Monthly Net TIC Flows','Private, net','Official, net']
tic_monthly_all.columns = tic_names

# Monthly Holdings of Securities (foreign holdings of U.S. securities, and U.S. holdings of foreign securities)

mhs = pd.read_csv('https://treasury.gov/resource-center/data-chart-center/tic/Documents/mfhhis01.csv',header=4,)

mhs_months = [i for i in mhs.iloc[0,1:-1]]
mhs = mhs.replace('------',np.nan)
mhs['Unnamed: 0'] = mhs['Unnamed: 0'].replace('Country','Year')
mhs = mhs.iloc[:,:-1].dropna()
mhs.index = mhs['Unnamed: 0']
mhs = mhs.iloc[:,1:]
mhs.columns = mhs_months
mhs.index.name = None

tc = pd.read_fwf('https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/snetus.txt',index_col='Unnamed: 0',header=5)

