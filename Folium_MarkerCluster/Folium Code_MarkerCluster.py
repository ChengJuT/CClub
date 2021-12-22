
### 參考網站:
### https://python-visualization.github.io/folium/index.html
### https://towardsdatascience.com/creating-interactive-maps-for-instagram-with-python-and-folium-68bc4691d075

import folium
from folium.plugins import MarkerCluster
import pandas as pd


### 建立地圖 & 地圖顯示的參數設定

xmas_map = folium.Map(location = [25.0448, 121.5488],  #參考座標位置,會位於地圖的中心位置
                      titles = "OpenStreetMap",        #地圖名稱,OpenStreetMap是default
                      width = 800, height = 400,       #地圖尺寸
                      min_zoom = 7, max_zoom = 18,     #地圖可縮放的程度, default為0~18
                      zoom_start = 12,                 #地圖開啟時的縮放程度, default為10
                      control_scale = False,           #地圖左下角是否要顯示尺規
                      zoom_control = True,)            #地圖左上角是否要顯示縮放的icon

# create a marker cluster called "Public toilet cluster"
marker_cluster = MarkerCluster(name="Test").add_to(xmas_map)

# 讀取csv檔
df = pd.read_csv("H:\python\ccClub\期末專案\Web_scraping\\2021-12-12_2021-12-15.csv")

for index, row in df.iterrows():
    row["Location_coord"] = list(map(float, row["Location_coord"][1:-1].split(", ")))
    # print(row["Location_coord"]) #只要呼叫pandas欄位名稱就可以取得數值
    folium.Marker(row["Location_coord"],           #要標記地點的座標
              popup = row["Location"],             #要標記地點的名稱
              tooltip = "Click here!",       #游標移到標記上時會顯示的文字
              icon = folium.Icon(color = "red", icon = "info-sign"),    #標記該地點的icon顏色
             ).add_to(marker_cluster)

### 存檔
xmas_map.save('xmas_map.html')




