import numpy as np
import pandas as pd

def get_rate_inflation_diff():
    path='data/'
    rate_inflation=pd.read_csv(path+'rate&inflation.csv',index_col=0,parse_dates=True)
    rate_inflation_diff = rate_inflation.diff()
    rate_inflation_diff.to_csv(path+'rate&inflation_diff.csv')
    return rate_inflation_diff

def get_rate_inflation_return_diff():
    path='data/'
    rate_inflation=pd.read_csv(path+'rate&inflation.csv',index_col=0,parse_dates=True)
    rate_inflation_return_diff = pd.DataFrame()
    rate_inflation_return_diff['b30-b20'] = rate_inflation['b30ret']-rate_inflation['b20ret']
    rate_inflation_return_diff['b30-b10'] = rate_inflation['b30ret']-rate_inflation['b10ret']
    rate_inflation_return_diff['b30-b7'] = rate_inflation['b30ret']-rate_inflation['b7ret']
    rate_inflation_return_diff['b30-b5'] = rate_inflation['b30ret']-rate_inflation['b5ret']
    rate_inflation_return_diff['b30-b2'] = rate_inflation['b30ret']-rate_inflation['b2ret']
    rate_inflation_return_diff['b30-b1'] = rate_inflation['b30ret']-rate_inflation['b1ret']
    rate_inflation_return_diff.to_csv(path+'rate&inflation_return_diff.csv')
    return rate_inflation_return_diff
    
def get_rate_inflation_index_diff():
    path='data/'
    rate_inflation=pd.read_csv(path+'rate&inflation.csv',index_col=0,parse_dates=True)
    rate_inflation_index_diff = pd.DataFrame()  
    rate_inflation_index_diff['b30-b20'] = rate_inflation['b30ind']-rate_inflation['b20ind']
    rate_inflation_index_diff['b30-b10'] = rate_inflation['b30ind']-rate_inflation['b10ind']
    rate_inflation_index_diff['b30-b7'] = rate_inflation['b30ind']-rate_inflation['b7ind']
    rate_inflation_index_diff['b30-b5'] = rate_inflation['b30ind']-rate_inflation['b5ind']
    rate_inflation_index_diff['b30-b2'] = rate_inflation['b30ind']-rate_inflation['b2ind']
    rate_inflation_index_diff['b30-b1'] = rate_inflation['b30ind']-rate_inflation['b1ind']
    rate_inflation_index_diff.to_csv(path+'rate&inflation_index_diff.csv')
    return rate_inflation_index_diff

def get_snp_spread():
    path='data/'
    SNP500ohlcv=pd.read_csv(path+'^GSPC S&P500 ohlcv.csv',index_col=0,parse_dates=True)
    SNP_spread = pd.DataFrame()
    SNP_spread['Close-Open']=SNP500ohlcv['Close']-SNP500ohlcv['Open']
    SNP_spread['High-Low']=SNP500ohlcv['High']-SNP500ohlcv['Low']
    SNP_spread.to_csv(path+'SNP_spread.csv')
    return SNP_spread

def get_SNP_Fu_Spot_spread():
    path='data/'
    SNPFu=pd.read_csv(path+'S&P 500 Futures Historical Data_2.csv',index_col=0,parse_dates=True)
    SNPFu = SNPFu.sort_index()
    SNPFu[['Price','Open','High','Low']] = SNPFu[['Price','Open','High','Low']].applymap(lambda x:float(x.replace(',','')))
    SNP_Fu_Spot_spread = pd.DataFrame()
    SNP_Fu_Spot_spread['Open']=SNPFu['Open']-SNP500ohlcv['Open']
    SNP_Fu_Spot_spread['High']=SNPFu['High']-SNP500ohlcv['High']
    SNP_Fu_Spot_spread['Low']=SNPFu['Low']-SNP500ohlcv['Low']
    SNP_Fu_Spot_spread['Close']=SNPFu['Price']-SNP500ohlcv['Close']
    SNP_Fu_Spot_spread=SNP_Fu_Spot_spread.dropna()
    SNP_Fu_Spot_spread.to_csv(path+'SNP_Fu_Spot_spread.csv')
    return SNP_Fu_Spot_spread