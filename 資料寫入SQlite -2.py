## 資料寫入 SQlite3 遇到 bug時
## 以大樂透為例(第35列開始)

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

    print(data)    
    dftemp = pd.DataFrame([data], columns=colName)

    #lotto = pd.concat([lotto, dftemp])
    ## 刪除上列的concat，直接用sq資料庫查是否有該期資料
    sql = 'Select * from 大樂透 where 期別="' + data[0] + '"'
    # 如果手動的把sq資料庫的檔案刪除，則會因讀去不到「大樂透」的檔名而出現DatabaseError，故使用 try except來解決
    try:
        dfcheck = pd.read_sql(sql, conn)
        # 如果發生錯誤，這個check就會錯誤，因此會執行 except的程式
    except:
        dfcheck = pd.DataFrame(columns=colName
                               )
    if len(dfcheck)==0:
        # 如果dfcheck查不到任何資料才進行寫入（或直接新增檔案寫入）
        dftemp.to_sql('大樂透', conn, if_exists='append', index=False)
    print("-----")
    
#lotto.to_sql('大樂透', conn, index=False, if_exists='replace')
# 因在for迴圈就陸續寫入資料進sq資料庫，因此以上這行即就不需要了
