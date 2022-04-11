#!/usr/bin/env python
# --- Economic data: Japan ---
# --- Autor: Hubert Mrugala (hubertmrugala.com) ---

import numpy as np
import pandas as pd

def hdr():
    return { "User-Agent": "Mozilla/5.0" }

# BoJ
# BoJ Time-Series Data Search: https://www.stat-search.boj.or.jp/index_en.html
# BoJ Statistics: https://www.boj.or.jp/en/statistics/index.htm/
def loans():
    """
    BoJ | Principal Figures of Financial Institutions: Loans and Discounts
    Latest release: https://www.boj.or.jp/en/statistics/dl/depo/kashi/index.htm/
    """
    loans = pd.read_html("https://www.stat-search.boj.or.jp/ssi/mtshtml/md13_m_1_en.html")[0]
    loans_cols = loans.iloc[1,:]
    loans = loans.iloc[7:,:]
    # Set column names
    loans.columns = loans_cols
    loans.set_index(loans.columns[0],inplace=True)
    loans.index.name = "Date"
    loans.index = pd.to_datetime(loans.index)
    loans.replace("ND",np.nan,inplace=True)
    loans = loans.astype(float)
    return loans

# METI
# Statistics: https://www.meti.go.jp/english/statistics/index.html

def sales():
    """
    METI 経済産業省 | Monthly Report on the Current Survey of Commerce
    Latest release: https://www.meti.go.jp/english/statistics/tyo/syoudou_kakuho/index.html
    Preliminary: https://www.meti.go.jp/english/statistics/tyo/syoudou/index.html
    """
    sales_url = "https://www.meti.go.jp/statistics/tyo/syoudou/result-2/excel/h2slt11j.xls"
    sales = pd.read_excel(sales_url,sheet_name=6,header=6,storage_options=hdr()) 

    sales = sales.set_index(sales.columns[0])
    sales.index = [str(i)[:4]+str(i)[-2:] for i in sales.index]
    sales.index = pd.to_datetime(sales.index,format="%Y%m").strftime('%b %Y')

    y_m = sales.pop("年月")
    sales["年月"] = y_m

    return sales

def ip():
    """
    METI 経済産業省 | (Preliminary) Industrial Production
    Latest release: https://www.meti.go.jp/english/statistics/tyo/iip/index.html
    """
    url = "https://www.meti.go.jp/english/statistics/tyo/iip/xls/b2015_gsm1e.xlsx"
    jp_ip = pd.read_excel(url,header=2,storage_options=hdr())
    jp_ip = jp_ip.T
    # Set columns row
    jp_ip.columns = jp_ip.iloc[1,:]
    # And get rid of it# And get rid of it# And get rid of it
    jp_ip = jp_ip.iloc[2:,:]
    # Save weights to another df
    weights = jp_ip.iloc[0,:]
    # Get rid of weights row
    jp_ip = jp_ip.iloc[1:,:]
    # Clean up index
    jp_ip.index = [str(i)[-6:] for i in jp_ip.index]
    jp_ip.index = pd.to_datetime(jp_ip.index,format="%Y%m")
    return jp_ip,weights

def ip_hist():
    url = "https://www.meti.go.jp/english/statistics/tyo/iip/xls/b2015_sgs1e.xls"
    ip_hist = pd.read_excel(url,header=2,storage_options=hdr(),index_col="ITEM NAME")
    ip_hist = ip_hist.iloc[1:,:]
    # Index
    ip_hist.index = pd.to_datetime(ip_hist.index,format="%Y%m")
    # Values
    ip_hist.replace("-",np.nan,inplace=True)
    return ip_hist.astype(float)

# Japan Cabinet Office
# Statistics: https://www.cao.go.jp/statistics/index.html
def watchers_sentiment():
    """
    Cabinet Office 経済産業省 | Economy Watchers Sentiment
    Latest release: https://www5.cao.go.jp/keizai3/watcher/watcher_menu.html
    """
    url = "https://www5.cao.go.jp/keizai3/watcher/watcher5.xls"
    watcher = pd.read_excel(url,sheet_name=0,header=5).iloc[:,1:]

    watcher_cols = ["Year","Month","Total", "Household trends","Ht: Retail","Ht: Food","Ht: Service",
        "Ht: Housing","Corporate trends","Ct: Manufacturing","Ct: Non-manufacturing","Employment"]
    watcher.columns = watcher_cols

    watcher["Year"].replace("", np.nan,inplace=True)
    watcher["Year"].replace(" ", np.nan,inplace=True)

    watcher["Year"].fillna(method="ffill",inplace=True)
    watcher["Year"] = [str(i)[:4] for i in watcher["Year"]]

    watcher.index = pd.to_datetime(watcher[["Year","Month"]].assign(Day=1))

    return watcher.iloc[:,2:]
 
