
#有時候popup會出現instagram拒絕連線的情況

import folium
from folium.plugins import MarkerCluster
import pandas as pd

def Create_Popup(name, insta_post, website, directions):
    pub_html = folium.Html(f"""
                        <p style="text-align: center;">
                            <b>
                            <span style="font-family: Didot, serif;font-size: 18px;">
                                {name}
                                </b>
                            </span>
                        </p>
                        <p style="text-align: center;">
                        <iframe src={insta_post}embed width="220" height="270" frameborder="0" scrolling="auto" allowtransparency="true">
                        </iframe>
                        <p style="text-align: center;">
                            <a href={website} target="_blank" title="{name} Website">
                                <span style="font-family: Didot, serif; font-size: 14px;">
                                    Instagram Post
                                </span>
                            </a>
                        </p>
                        <p style="text-align: center;">
                            <a href={directions} target="_blank" title="Directions to {name}">
                                <span style="font-family: Didot, serif; font-size: 14px;">
                                    Directions to {name}
                                </span>
                            </a>
                        </p>
    """, script=True)

    popup = folium.Popup(pub_html, max_width=500)
    return popup


### 建立地圖 & 地圖顯示的參數設定

xmas_map = folium.Map(location = [25.0448, 121.5488],  #參考座標位置,會位於地圖的中心位置
                      titles = "OpenStreetMap",        #地圖名稱,OpenStreetMap是default
                    #   width = 800, height = 400,       #地圖尺寸
                      min_zoom = 7, max_zoom = 18,     #地圖可縮放的程度, default為0~18
                      zoom_start = 12,                 #地圖開啟時的縮放程度, default為10
                      control_scale = False,           #地圖左下角是否要顯示尺規
                      zoom_control = True,)            #地圖左上角是否要顯示縮放的icon

# create a marker cluster called "Public toilet cluster"
marker_cluster = MarkerCluster(name="Test").add_to(xmas_map)

# 讀取csv檔
df = pd.read_csv("H:\python\ccClub\期末專案\聖誕景點_12-12_12-21篩選_utf-8.csv")

# count = 0
for index, row in df.iterrows():
    row["Location_coord"] = list(map(float, row["Location_coord"][1:-1].split(", ")))
    name = row["Location"]
    insta_post = row["Post_url"] + "/"
    website = row["Post_url"]
    directions = row["Post_url"]
    popup = Create_Popup(name, insta_post, website, directions)
    # print(row["Location_coord"]) #只要呼叫pandas欄位名稱就可以取得數值
    folium.Marker(row["Location_coord"],           #要標記地點的座標
              popup = popup,             #要標記地點的名稱
              tooltip = row["Location"],       #游標移到標記上時會顯示的文字
            icon = folium.Icon(color = "darkgreen", icon = "tree-conifer")    #標記該地點的icon顏色
             ).add_to(marker_cluster)
    # count += 1
    # if count >= 1: break

### 存檔
xmas_map.save('xmas_map1.html')
xmas_map




