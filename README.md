本程式包含5個步驟
 1. 爬蟲找IG景點貼文
 2. Folium 地圖標記並找熱區
 3. Google api 找熱區附近餐廳
 4. 爬蟲找美食貼文
 5. 介面呈現

1. 爬蟲找IG景點貼文
請執行 ./webscraping/Instagram_爬蟲1221.py
程式會要求使用者輸入IG的帳號密碼（以空白符號區隔）
修改line 134/135 的 since/until 以設定提取的貼文日期
修改line 127/128 的 keywords 以設定搜尋的關鍵字

2. Folium 地圖標記
請執行 ./Folium map/Folium Code_Instagram_Popup.py 輸出初步的景點標記地圖xmas_map.html

3. Google api 找熱區附近餐廳(需申請 google api key並開啟place api功能)  
	step1 修改 11行 mykey輸入google api key  
	step2 修改 input.txt 以行為格式單位分別輸入 地點名稱,latitude,longitude  
	step3 執行(到該檔案路徑) python Main.py  

4. 爬蟲找美食貼文
請執行 ./webscraping/Instagram_美食搜尋.py

5. 介面呈現
	請執行 ./Folium map/Folium Code_Instagram_Popup.py 輸出最終的地圖標記
	
	開啟電腦終端 terminal/cmd 使用pythonw 執行 ./Interface/HomePage.py 以開啟介面
	e.g.
	pythonw ./Interface/HomePage.py
	
	line 20/27 的 AREA/MAPS 字典以增減按鈕數量和指定開啟的地圖html檔，系統會以每排三個按鈕的方式自動排列其位置
