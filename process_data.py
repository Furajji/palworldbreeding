import pandas as pd

pal_JP = pd.read_csv('palJP.csv').loc[:,'パルNo.':'名前'].astype(str)
pal_EN = pd.read_csv('palEN.csv',header=None)
pal_EN = pal_EN.iloc[:,0:2].astype(str)
pal_EN.columns=['パルNo.','名前']

pal_df = pd.merge(pal_JP,pal_EN,on='パルNo.',how='inner')
print(pal_df)
pal_df.to_csv('pal_tr.csv',index=None)