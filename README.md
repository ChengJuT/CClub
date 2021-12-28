本程式包含5個步驟
 1. 爬蟲找IG景點貼文
 2. Folium 地圖標記並找熱區
 3. Google api 找熱區附近餐廳
 4. 爬蟲找美食貼文
 5. 介面呈現

1. 爬蟲找IG景點貼文
爬聖誕景點請執行 ./webscraping/Instagram_爬蟲.py
	程式會要求使用者輸入IG的帳號密碼（以空白符號區隔）
	修改line 127/128 的 since/until 以設定提取的貼文日期
	修改line 121/122 的 keywords 以設定搜尋的關鍵字
	修改line 136 的 可自行設定檔案名稱

2. Folium 地圖標記  
	step1 修改 line 56 地圖的預設資訊, 如座標. 地圖縮放程度...等等  
	step2 修改 line 70 & line 88 欲讀取的csv檔  
	step3 執行 ./folium_map/folium code, 輸出景點標記地圖, 北中南依序為xmas1_map.html / xmas2_map.html / xmas3_map.html

3. Google api 找熱區附近餐廳(需申請 google api key並開啟place api功能)  
	step1 修改 11行 mykey輸入google api key  
	step2 修改 input.txt 以行為格式單位分別輸入 地點名稱,latitude,longitude  
	step3 執行(到該檔案路徑) python Main.py  

4. 爬蟲找美食貼文
爬美食景點請執行 ./webscraping/Instagram_美食搜尋.py
	預設使用Chrome瀏覽器，故務必確保chromedriver.exe與程式在同一個資料夾
	可修改line 90 的讀取json檔案，預設為自Google Places api取得

5. 介面呈現
	請執行 ./Folium map/Folium Code_Instagram_Popup.py 輸出最終的地圖標記
	
	開啟電腦終端 terminal/cmd 使用pythonw 執行 ./Interface/HomePage.py 以開啟介面
	e.g.
	pythonw ./Interface/HomePage.py
	
	line 20/27 的 AREA/MAPS 字典以增減按鈕數量和指定開啟的地圖html檔，系統會以每排三個按鈕的方式自動排列其位置
