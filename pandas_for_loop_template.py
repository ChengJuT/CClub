import pandas as pd
'''把檔案讀進來'''
df = pd.read_csv("H:\python\ccClub\期末專案\Web_scraping\聖誕節1208_1214.csv")


'''用for迴圈取用某一個欄位裡每一列的資料'''
for index, row in df.iterrows():
    print(row["Location_coord"], row["Location"]) #只要呼叫pandas欄位名稱就可以取得數值