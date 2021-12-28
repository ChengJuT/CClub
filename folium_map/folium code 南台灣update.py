### 參考網站:
### https://python-visualization.github.io/folium/index.html
### https://towardsdatascience.com/creating-interactive-maps-for-instagram-with-python-and-folium-68bc4691d075
### https://pubs-of-oxfordshire-map.github.io
### https://stackoverflow.com/questions/59857949/
### https://getbootstrap.com/docs/3.3/components/

import folium
import json
import pandas as pd
from folium import plugins, Icon, FeatureGroup
from folium.plugins import LocateControl, MarkerCluster
from selenium import webdriver
import webbrowser 

def Create_Popup_place(name, insta_post, website, directions):
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


def Create_Popup_food(name, insta_post, website, rating, directions):
    pub_html = folium.Html(f"""
                            <p style="text-align: center;">
                                <b>
                                <span style="font-family: Didot, serif;font-size: 18px;">
                                    {name}
                                    </b>
                                </span>
                            </p>
                            <p style="text-align: center;">
                                <b>
                                <span style="font-family: Didot, serif;font-size: 14px;">
                                    Rating: {rating}
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

### 建立地圖中心點 & 地圖顯示的參數設定

xmas_map3 = folium.Map(location = [22.7873025,120.3158033],  #參考座標位置,會位於地圖的中心位置
                      titles = "OpenStreetMap",            #地圖名稱,OpenStreetMap是default
#                      width = 1200, height = 800,         #地圖顯示尺寸,若未設定則依照user的畫面顯示
                      min_zoom = 7, max_zoom = 18,         #地圖可縮放的程度, default為0~18
                      zoom_start = 11,                      #地圖開啟時的縮放程度, default為10
                      control_scale = True,                #地圖左下角是否要顯示尺規
                      zoom_control = True,)                #地圖左上角是否要顯示縮放的icon


# create a marker cluster
marker_cluster = MarkerCluster(name = "Xmas Place_Layer").add_to(xmas_map3)
food = MarkerCluster(name = "Food_Layer").add_to(xmas_map3)

# 讀取csv檔
df = pd.read_csv("聖誕景點_12-12_12-21篩選_utf-8.csv")

for index, row in df.iterrows():
    row["Location_coord"] = list(map(float, row["Location_coord"][1:-1].split(", ")))
    name = row["Location"]
    insta_post = row["Post_url"] + "/"
    website = row["Post_url"]
    directions = "https://www.google.com/maps/search/?api=1&query=" + name.replace(" ", "")
    popup = Create_Popup_place(name, insta_post, website, directions)
    
    # print(row["Location_coord"])                      #只要呼叫pandas欄位名稱就可以取得數值
    folium.Marker(row["Location_coord"],                #要標記地點的座標
              popup = popup,                            #要標記地點的名稱
              tooltip = row["Location"],                #游標移到標記上時會顯示的文字
              icon = folium.Icon(color = "green", icon = "tree-conifer"),    #標記該地點的icon顏色
             ).add_to(marker_cluster)

### 用pandas讀取美食csv檔
df = pd.read_csv("熱區週邊美食店家資料.csv")
for index, row in df.iterrows():
    coord = row["Location_coord"].strip('()') 
    numlist = [float(n) for n in coord.split(",")]
    name = row["Location"]
    insta_post = row["Post_url"]
    website = row["Post_url"]
    rating = row["rating"]
    directions = "https://www.google.com/maps/search/?api=1&query=" + name.replace(" ", "")
    popup = Create_Popup_food(name, insta_post, website, rating, directions) 
    folium.Marker(numlist,
                  tooltip = row["Location"],
                  popup = popup,
                  icon = folium.Icon(color = "red", icon = "glass"),
                  ).add_to(food)

xmas_map3.add_child(marker_cluster)
xmas_map3.add_child(food)

folium.LayerControl().add_to(xmas_map3)

### 存檔
xmas_map3.save('xmas_map3.html')

xmas_map3