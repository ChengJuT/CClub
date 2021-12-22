import folium
from folium import FeatureGroup

m = folium.Map(location = [25, -256])

locs = [[25, -253],[26, -255] , [25.5, -257], [24, -257]]

marker1 = folium.Marker(location= locs[0])
marker2 = folium.Marker(location= locs[1])
marker3 = folium.Marker(location= locs[2])
marker4 = folium.Marker(location= locs[3])

## 產生群組並把標示加入群組中
fg1 = FeatureGroup(name = "Feature Group1").add_to(m)
fg1.add_child(marker1)
## 群組內可容納多個標誌
fg2 = FeatureGroup(name = "Feature Group2").add_to(m)
fg2.add_child(marker2)
fg2.add_child(marker3)
## 但每個標誌只能存在一個群組內，重複定義會把先前的設定覆蓋
fg2.add_child(marker4)
fg1.add_child(marker4)
## 把群組加入地圖中
m.add_child(fg1)
m.add_child(fg2)
## 加入控制介面（地圖右上角的分層按鈕
folium.LayerControl().add_to(m)


points = locs
# 方塊會把所有點包起來
folium.Rectangle(bounds=points,stroke=True, weight = 0.5, color='#ff7800', fill=True, fill_color='#ffff00', fill_opacity=0.2).add_to(m)
# 多邊形會把所有點連起來
folium.Polygon(locations=points, stroke = False, color='#78ff00', fill=True, fill_color='#00ff00', fill_opacity=0.2).add_to(m)
# stroke : 是否描邊
# weight : 描邊線寬
# color / fill_color : ＲＧＢ三原色16近位制
# opacity : 不透明度 透明 0 <-----> 1 不透  

m.save("filterSampe.html")
