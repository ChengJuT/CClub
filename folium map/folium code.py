#!/usr/bin/env python
# coding: utf-8


### 參考網站:
### https://python-visualization.github.io/folium/index.html
### https://towardsdatascience.com/creating-interactive-maps-for-instagram-with-python-and-folium-68bc4691d075
### https://pubs-of-oxfordshire-map.github.io
### https://stackoverflow.com/questions/59857949/
### https://getbootstrap.com/docs/3.3/components/

import folium
import json
import pandas as pd
from folium import plugins, Icon
from folium.plugins import LocateControl, MarkerCluster


### 建立地圖中心點 & 地圖顯示的參數設定

xmas_map = folium.Map(location = [23.97565, 120.9738819],  #參考座標位置,會位於地圖的中心位置
                      titles = "OpenStreetMap",        #地圖名稱,OpenStreetMap是default
#                      width = 1200, height = 800,    #地圖顯示尺寸,若未設定則依照user的畫面顯示
                      min_zoom = 7, max_zoom = 18,     #地圖可縮放的程度, default為0~18
                      zoom_start = 8,                  #地圖開啟時的縮放程度, default為10
                      control_scale = True,           #地圖左下角是否要顯示尺規
                      zoom_control = True,)            #地圖左上角是否要顯示縮放的icon


### 用pandas讀取景點csv檔

df = pd.read_csv("2021-12-12_2021-12-15.csv")
df = pd.read_csv("聖誕節1208_1214.csv")


### 加入地圖顯示的Cluster

marker_cluster = MarkerCluster(options = {"zoomToBoundsOnClick": True,     #點選cluster的點,會直接縮放到涵蓋的範圍
#                                          "disableClusteringAtZoom": 15,   #當縮放程度為15時會取消cluster
                                         }
                              ).add_to(xmas_map)


### 用for迴圈取用csv檔裡某一個欄位裡每一列的資料 (座標 & 名稱)

for index, row in df.iterrows():
#    print(row["Location_coord"], row["Location"])       #只要呼叫pandas欄位名稱就可以取得數值
    coord = row["Location_coord"].strip('()')            #把原始檔座標的括號()去掉
    numlist = [float(n) for n in coord.split(",")]       #再用逗號來區分list,定義經緯度
#    print(numlist[0],numlist[1])                        #測資確認:確認去括號()後的結果
    folium.Marker(numlist,                                                #上述去括號()後的標記地點座標
                  tooltip = row["Location"],                              #游標移到標記上時會顯示的文字
                  popup = row["Location"],                                #游標點選標記上會跳出的ig畫面or文字
                  icon = folium.Icon(color = "darkgreen", icon = "tree-conifer"),  #標記該地點的icon顏色(不能使用色碼)
                 ).add_to(marker_cluster)


### 用pandas讀取美食csv檔

df = pd.read_csv("美食熱門貼文.csv")
for index, row in df.iterrows():
    coord = row["Location_coord"].strip('()') 
    numlist = [float(n) for n in coord.split(",")] 
    folium.Marker(numlist, 
                  tooltip = row["Location"], 
                  popup = row["Location"], 
                  icon = folium.Icon(color = "red", icon = "thumbs-up"),
                 ).add_to(xmas_map)

### 定義地圖邊界線的粗細/顏色

border_style = {"color": "#000000",       #邊界線的顏色
                "weight": "1",            #邊界線的粗細
                "fillColor": "efebe7",    #界內區域的顏色
                "fillOpacity": 0.08}      #界內區域顏色的透明度,1會全黑


### 在地圖上建立邊界, 要先去GeoJson畫出邊界
### GeoJson網站: http://geojson.io/#map=2/20.0/0.0
### 用GeoJson畫邊界教學: https://ithelp.ithome.com.tw/articles/10208768
### 把畫好的geojson檔下載, 再上傳到資料夾裡

boundary = folium.GeoJson(open('taipeicity.geojson').read(), 
                          name = 'Taipei City', 
                          style_function = lambda x: border_style, 
                          overlay = False
                         ).add_to(xmas_map)


### 存檔
xmas_map.save('xmas_map.html')

xmas_map
