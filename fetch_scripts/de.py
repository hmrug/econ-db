import pandas as pd

def zew():
    """
    ZEW | ZEW Financial Market Survey & ZEW Indicator of Economic Sentiment
    Latest release: https://www.zew.de/en/publications/zew-expertises-research-reports/research-reports/business-cycle/zew-financial-market-survey
    """
    zew_url = "http://ftp.zew.de/pub/zew-docs/div/konjunktur.xls"
    zew = pd.read_excel(zew_url,
                        index_col='Date').iloc[:-1,:]
    zew.index = pd.to_datetime(zew.index).strftime('%b %Y')


def ifo():
    """
    ifo INSTITUTE | ifo Business Climate
    Latest release: https://www.ifo.de/en/umfragen/time-series
    """
    ifo_url = "https://www.ifo.de/sites/default/files/secure/timeseries/gsk-e-202203.xlsx"
    ifo = pd.read_excel(ifo_url,
                        header=7,sheet_name=0,index_col="Month/year").iloc[:,:3]
    ifo.index = pd.to_datetime(ifo.index).strftime('%b %Y')
    return ifo
