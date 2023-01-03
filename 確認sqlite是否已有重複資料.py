import pandas as pd
import requests
import sqlite3
import time

conn = sqlite3.connect('台銀.db')

dayData = pd.date_range("20210801","20210831")
for daytemp in dayData:
    yearMonthDay = str(daytemp)[:10]

    url = "https://rate.bot.com.tw/xrt/all/" + yearMonthDay
    time.sleep(5)

    list1 = pd.read_html(url)
    df = list1[0]
    if len(df) > 1:
        df = df.iloc[:,:5]
        df.columns=['幣別','現金買入','現金賣出','即期買入','即期賣出']
        df['幣別代號']=df['幣別'].str.split(' ').str[1].str.replace('(','').str.replace(')','')
        df['幣別']=df['幣別'].str.split(' ').str[0]
        
        for i in range(1,5):
            df.iloc[:,i]=pd.to_numeric(df.iloc[:,i], errors="coerce")
        
        df=df.set_index('幣別代號')
        df['日期']=yearMonthDay
        sql = 'Select * from 匯率 where 日期="'+yearMonthDay +'"'
        
        try:
            dfcheck = pd.read_sql(sql, conn)
        except:
            dfcheck = pd.DataFrame()
        
        if len(dfcheck) == 0:
            df.to_sql("匯率", conn, if_exists="append")