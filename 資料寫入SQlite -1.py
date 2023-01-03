## 資料寫入 SQlite3
## 以大樂透為例(最後一行)

import pandas as pd
import sqlite3

conn = sqlite3.connect('中獎號碼.db')
# 連線物件

url = "https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx"

df=pd.read_html(url)

colName = ['期別', '開獎日', '兌獎截止', '銷售金額', '獎金總額', '獎號1', '獎號2', '獎號3', '獎號4', '獎號5', '獎號6', '特別號' ]
lotto = pd.DataFrame(columns=colName)
# 只單純建立一個只有欄位名稱，沒有資料的DataFrame

# 點df看整個表格資料，抓取大樂透的特定數值
for d in df[2:12]:
    data=[]
    data.append(d.iloc[1,0]) #期別
    data.append(d.iloc[1,1]) #開獎日
    data.append(d.iloc[1,3]) #兌獎截止
    data.append(d.iloc[1,5]) #銷售金額
    data.append(d.iloc[1,7]) #獎金總額
    for i in range(2,9): #六個中獎號與一個特別號
        data.append(d.iloc[4,i])
# 中獎號在表格中的第四列，所以列固定在4，而從小到大的號碼，分別在第二欄至第八欄的位置，所以用for迴圈抓取
    print(data)    
    dftemp = pd.DataFrame([data], columns=colName)
    # data是一維的串列，所以多加[]使它變成DataFrame的二維型態
    # dftemp是讓資料與欄位名稱寫入的物件。可以點左邊的dftemp查看
    lotto = pd.concat([lotto, dftemp])
    # 將空的欄位名稱lotto與資料dftemp串接
    print("-----")
    
lotto.to_sql('大樂透', conn, index=False, if_exists='replace')
# 寫入資料進sqlite(記得要先import sqlite3)


