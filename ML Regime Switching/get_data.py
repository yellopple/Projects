# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 23:51:32 2020

@author: Li Jiahang
"""
import numpy as np
import pandas as pd
import os
    
path1='data/'
path2='output/'

notnum=[]
def change_to_num(x):
    global notnum
    if type(x)==str:
        x=x.replace(',','')
        if x[-1]=='M':
            return float(x[:-1])*1e6
        elif x[-1]=='B':
            return float(x[:-1])*1e9
        elif x[-1]=='K':
            return float(x[:-1])*1e3  
        elif x[-1]=='%':
            return float(x[:-1].replace(',',''))*1e-2
        elif x=='-':
            return np.nan
        return float(x)
    else:
        if x==x:
            return x
        else:
            notnum+=[str(x)]       

def get_Bond():
    Treasury_Yield_2Y=pd.read_csv(path1+'Bond/2Y_Treasury_Yield.csv',index_col=0,parse_dates=True)
    Treasury_Yield_2Y['Change']=Treasury_Yield_2Y['Change %'].map(change_to_num)
    Treasury_Yield_2Y.drop(columns=['Change %'],inplace=True)
    Treasury_Yield_2Y.columns=np.array(Treasury_Yield_2Y.columns)+'_Yield2y'
    Treasury_Yield_2Y=Treasury_Yield_2Y.iloc[::-1,:]
    Treasury_Yield_10Y=pd.read_csv(path1+'Bond/10Y_Treasury_Yield.csv',index_col=0,parse_dates=True)
    Treasury_Yield_10Y['Change']=Treasury_Yield_10Y['Change %'].map(change_to_num)
    Treasury_Yield_10Y.drop(columns=['Change %'],inplace=True)
    Treasury_Yield_10Y.columns=np.array(Treasury_Yield_10Y.columns)+'_Yield10y'
    Treasury_Yield_10Y=Treasury_Yield_10Y.iloc[::-1,:]
    Treasury_Yield_30Y=pd.read_csv(path1+'Bond/30Y_Treasury_Yield.csv',index_col=0,parse_dates=True)
    Treasury_Yield_30Y['Change']=Treasury_Yield_30Y['Change %'].map(change_to_num)
    Treasury_Yield_30Y.drop(columns=['Change %'],inplace=True)
    Treasury_Yield_30Y.columns=np.array(Treasury_Yield_30Y.columns)+'_Yield30y'
    Treasury_Yield_30Y=Treasury_Yield_30Y.iloc[::-1,:]
    Bond=pd.concat([Treasury_Yield_2Y,Treasury_Yield_10Y,Treasury_Yield_30Y],axis=1,join='outer')
    Bond.to_csv(path2+'Bond.csv')
    return Bond
    
def get_FX():
    Dollar_index=pd.read_csv(path1+'FX/US Dollar Index Historical Data.csv',index_col=0,parse_dates=True)
    Dollar_index['Change']=Dollar_index['Change %'].map(change_to_num)
    Dollar_index.drop(columns=['Change %'],inplace=True)
    Dollar_index.columns=np.array(Dollar_index.columns)+'_Dollar_index'
    Dollar_index=Dollar_index.iloc[::-1,:]
    FX=Dollar_index
    FX.to_csv(path2+'FX.csv')
    return FX
    
def get_Equity():
    df={}
    for info in os.listdir('data/Equity/'):
        domain = os.path.abspath(r'data/Equity/') #获取文件夹的路径
        data = pd.read_csv(os.path.join(domain,info),index_col=0,parse_dates=True)
        df[info]=data
    for key in df.keys():
        data=df[key]
        data_num=data.applymap(change_to_num)
        data_num.columns=np.array(data_num.columns)+'_'+key.split()[0].split('.')[0]
        df[key]=data_num
    Equity=pd.concat([df[key] for key in df.keys()],axis=1,join='outer')
    print(np.unique(notnum)) #data中存在的缺失数据以什么表示
    Equity.to_csv(path2+'Equity.csv')
    return Equity
    
def get_Commodity():
    folder=['PRECIOUS METALS','INDUSTRIAL METALS','ENERGY','AGRICULTURE']
    PRECIOUS_METALS,INDUSTRIAL_METALS,ENERGY,AGRICULTURE=np.nan,np.nan,np.nan,np.nan
    mid_df=[PRECIOUS_METALS,INDUSTRIAL_METALS,ENERGY,AGRICULTURE]
    for i in range(len(folder)):
        df={}
        f=folder[i]
        for info in os.listdir('data/Commodity/'+f):
            domain = os.path.abspath(r'data/Commodity/'+f) #获取文件夹的路径
            data = pd.read_csv(os.path.join(domain,info),index_col=0,parse_dates=True)
            df[info]=data
        for key in df.keys():
            data=df[key]
            data['Vol.']=data['Vol.'].map(change_to_num)
            data['Change']=data['Change %'].map(change_to_num)
            data.drop(columns=['Change %'],inplace=True)
            data[['Price','Open','High','Low']] = data[['Price','Open','High','Low']].applymap(change_to_num)
            data.columns=np.array(data.columns)+'_'+key[:-28]
            df[key]=data
        mid_df[i]=pd.concat([df[key] for key in df.keys()],axis=1,join='outer')
    Commodity=pd.concat(mid_df,axis=1,join='outer')
    Commodity.to_csv(path2+'Commodity.csv')
    return Commodity
    
def get_Other():
    VIX=pd.read_csv(path1+'Other\CBOE Volatility Index Historical Data_2.csv',index_col=0,parse_dates=True)
    VIX['Vol.']=VIX['Vol.'].map(change_to_num)
    VIX['Change']=VIX['Change %'].map(change_to_num)
    VIX.drop(columns=['Change %'],inplace=True)
    VIX.columns=np.array(VIX.columns)+'_VIX'
    FF5=pd.read_csv(path1+'Other\F-F_Research_Data_5_Factors_2x3_daily.csv',index_col=0,parse_dates=True)
    Other=pd.concat([VIX,FF5],axis=1,join='outer')
    Other.to_csv(path2+'Other.csv')
    return Other
    
def get_all_data():
    Bond=get_Bond()
    FX=get_FX()
    Commodity=get_Commodity()
    Equity=get_Equity()
    Other=get_Other()
    full=pd.concat([Bond,FX,Commodity,Equity,Other],axis=1,join='outer')
    full.to_csv(path2+'full.csv')
    return full

if __name__ == '__main__':
    print(get_Equity())