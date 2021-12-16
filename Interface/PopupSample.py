import folium


m = folium.Map(location=[45.5236, -122.6750])
tooltip = "Click me!"

'''
folium.Marker(
    [45.3288, -122.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
).add_to(m)
'''



delay=5
icon_img = './icon.png'
custom_icon = folium.CustomIcon(icon_img, icon_size=(35, 35), popup_anchor=(0, -22))


name = "Name"
#insta_post = "./pic.png"
insta_post = "https://www.instagram.com/p/CXiTJfJPbvf/"
website = "https://www.google.com/"
directions = "https://www.google.com/"

pub_html = folium.Html(f"""<p style="text-align: center;"><b><span style="font-family: Didot, serif; font-size: 18px;">{name}</b></span></p>
<p style="text-align: center;"><iframe src={insta_post}embed width="220" height="270" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
<p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 14px;">{name} Website</span></a></p>
<p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 14px;">Directions to {name}</span></a></p>
""", script=True)

popup = folium.Popup(pub_html, max_width=220)

custom_marker = folium.Marker(location= [45.3288, -122.6625], icon=custom_icon, popup=popup)

custom_marker.add_to(m)

m.save("map.html")

