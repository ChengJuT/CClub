# -*- coding: utf-8 -*-
import googlemaps
import requests
import json

import time # 引入time
# nowTime = int(time.time()) # 取得現在時間
# struct_time = time.localtime(nowTime) # 轉換成時間元組
# time_stamp = int(time.mktime(struct_time)) # 轉成時間戳

mykey='AIzaSyC55bJbwsXFmlPhP6Y0p0MmmGP_9P-Okj0'
gmaps = googlemaps.Client(key=mykey) #只跟地址轉經緯度有關
#https://github.com/googlemaps/google-maps-services-python/tree/master/tests


def geocode (address): #地址轉經緯度
    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    # geocode_result = [{'address_components': [{'long_name': '121', 'short_name': '121', 'types': ['street_number']}, {'long_name': 'Banxin Road', 'short_name': 'Banxin Rd', 'types': ['route']}, {'long_name': '香丘里', 'short_name': '香丘里', 'types': ['administrative_area_level_4', 'political']}, {'long_name': 'Banqiao District', 'short_name': 'Banqiao District', 'types': ['administrative_area_level_3', 'political']}, {'long_name': 'New Taipei City', 'short_name': 'New Taipei City', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'Taiwan', 'short_name': 'TW', 'types': ['country', 'political']}, {'long_name': '220', 'short_name': '220', 'types': ['postal_code']}], 'formatted_address': 'No. 121, Banxin Rd, Banqiao District, New Taipei City, Taiwan 220', 'geometry': {'location': {'lat': 25.0150978, 'lng': 121.4711816}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 25.0164467802915, 'lng': 121.4725305802915}, 'southwest': {'lat': 25.0137488197085, 'lng': 121.4698326197085}}}, 'place_id': 'ChIJL9bZ3yKoQjQROQN0Btdj74o', 'plus_code': {'compound_code': '2F8C+2F Banqiao District, New Taipei City, Taiwan', 'global_code': '7QQ32F8C+2F'}, 'types': ['street_address']}]
    return (geocode_result[0]['geometry']['location'])

def findPlaces (findname): #名稱查經緯度 https://developers.google.com/maps/documentation/places/web-service/search-find-place
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+findname+"&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry%2Cplace_id&key="+mykey
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_result=json.loads(response.text)
    return(response_result['candidates'][0]['geometry']['location'])

    # test_response = '{"candidates" : [{"formatted_address" : "220台灣新北市板橋區中山路一段161號","geometry" : {"location" : {"lat" : 25.0122763,"lng" : 121.4655369},"viewport" : {"northeast" : {"lat" : 25.01352827989272,"lng" : 121.4669277798927},"southwest" : {"lat" : 25.01082862010728,"lng" : 121.4642281201072}}},"name" : "新北市政府 市民廣場 兒童藝術節","opening_hours" : {"open_now" : true},"place_id" : "ChIJq2QwKRmoQjQRMpx-0D_asa4","rating" : 4.4}],"status" : "OK"}'
    # test_response=json.loads(test_response)# string(json) to json
    # return (test_response['candidates'][0]['geometry']['location'])

def findPlaces_range (lat,lng,radius,target,f_name): #經緯度查範圍 https://developers.google.com/maps/documentation/places/web-service/search-nearby

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?language=zh-TW&location="+lat+","+lng+"+&radius="+radius+"&type="+target+"&key="+mykey
    payload={}
    headers = {}
    mainarray = []
    count = 0
    response = requests.request("GET", url, headers=headers, data=payload)
    response_result=json.loads(response.text)
    print (url)

    # response = r"""{"html_attributions":[],"results":[{"business_status":"OPERATIONAL","geometry":{"location":{"lat":25.0118142,"lng":121.4659919},"viewport":{"northeast":{"lat":25.0132449302915,"lng":121.4672822802915},"southwest":{"lat":25.0105469697085,"lng":121.4645843197085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png","icon_background_color":"#FF9E67","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet","name":"Liu Biju Chaozhou casserole porridge a product Zhongshan headquarters","opening_hours":{"open_now":true},"photos":[{"height":2268,"html_attributions":["<a href=\"https://maps.google.com/maps/contrib/101991688570576153096\">六必居潮州一品沙鍋粥中山總店/板橋美食/新北美食</a>"],"photo_reference":"Aap_uEB_D9LCFD9znuhqTE2nGReDOiEIlRKANastngpsl13yfgz-g4fEHwYBFVAR4SS2SEu2JpJraDqZMNCxqGPgJ9X_cT6jkXXlfGCSxQp4rKLA8nyW-AtdJMkzKHlkpOIppsVefFnMINkyN0pXRPQx-IRaIOEqbmDfmZeIPTWpDI-b74-W","width":4032}],"place_id":"ChIJPwFtMx-oQjQRyDjE21ZvByc","plus_code":{"compound_code":"2F68+P9 Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+P9"},"price_level":2,"rating":4.2,"reference":"ChIJPwFtMx-oQjQRyDjE21ZvByc","scope":"GOOGLE","types":["restaurant","food","point_of_interest","establishment"],"user_ratings_total":4382,"vicinity":"No. 158號, Section 1, Zhongshan Road, Banqiao District"},{"business_status":"CLOSED_TEMPORARILY","geometry":{"location":{"lat":25.0117765,"lng":121.4658113},"viewport":{"northeast":{"lat":25.0131972802915,"lng":121.4671234802915},"southwest":{"lat":25.0104993197085,"lng":121.4644255197085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png","icon_background_color":"#FF9E67","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet","name":"寬心園精緻蔬食料理板橋中山店","permanently_closed":true,"photos":[{"height":2736,"html_attributions":["<a href=\"https://maps.google.com/maps/contrib/111390646225171052067\">HC C</a>"],"photo_reference":"Aap_uEBE0kreOX6cEa23Nwhvbv30kozkkwIUZbJi8I29E4cB_rkMGk3TJCUeNh9_7zmL2mviD6z1OH-RnXuLiJl37h3b_XoE6b8CMyZU-fdawh9nZmF2mjRPZ7lPB03ndZofAdL2rluxyCd5g0NCxsiD136tRkdU7umRGZfIWGzEK3iTEmM9","width":3648}],"place_id":"ChIJkUMeKR-oQjQRPrf5TU8lHt4","plus_code":{"compound_code":"2F68+P8 Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+P8"},"price_level":2,"rating":4,"reference":"ChIJkUMeKR-oQjQRPrf5TU8lHt4","scope":"GOOGLE","types":["restaurant","food","point_of_interest","establishment"],"user_ratings_total":807,"vicinity":"No. 158號, Section 1, Zhongshan Road, Banqiao District"},{"business_status":"OPERATIONAL","geometry":{"location":{"lat":25.0122763,"lng":121.4655369},"viewport":{"northeast":{"lat":25.0135274302915,"lng":121.4669269302915},"southwest":{"lat":25.0108294697085,"lng":121.4642289697085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png","icon_background_color":"#FF9E67","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet","name":"典藏33觀景餐廳","opening_hours":{"open_now":false},"photos":[{"height":667,"html_attributions":["<a href=\"https://maps.google.com/maps/contrib/102582533663713002718\">典藏33觀景餐廳</a>"],"photo_reference":"Aap_uEBuOqVre3lCKBT4Jb0jAPtvjokmvwrMz9dy95GABP7uMSesKng1bqTF7t3141RQnQRFUJixrMeooIpd8n4kMTIUfxIWYOU5OV9EsJPConcv859oCc0SOUbKOpAgEetMqvxlKH361Zz0lYIx-alWt665Zz4KaBmaPz74KZWE60DXVjF1","width":1000}],"place_id":"ChIJWWqX1R6oQjQRz9jEIsV5bIQ","plus_code":{"compound_code":"2F68+W6 Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+W6"},"price_level":3,"rating":4.1,"reference":"ChIJWWqX1R6oQjQRz9jEIsV5bIQ","scope":"GOOGLE","types":["bar","restaurant","food","point_of_interest","establishment"],"user_ratings_total":1221,"vicinity":"33樓, No. 161號, Section 1, Zhongshan Road, Banqiao District"},{"business_status":"OPERATIONAL","geometry":{"location":{"lat":25.012394,"lng":121.465286},"viewport":{"northeast":{"lat":25.01357383029151,"lng":121.4667743302915},"southwest":{"lat":25.0108758697085,"lng":121.4640763697085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png","icon_background_color":"#FF9E67","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet","name":"新北市政府員工餐廳","opening_hours":{"open_now":false},"photos":[{"height":3024,"html_attributions":["<a href=\"https://maps.google.com/maps/contrib/117155754004653593980\">幸福就好Sara</a>"],"photo_reference":"Aap_uEDqQT9os0nFfGgnHERunJpBQmdm4nc6G2mm9kMXyZYUIxdkf6ND_bBYpGTMGt3ohzjO_O0OY7xWYcNynyjl63rXYK4M3goeu-7g8oJbmxp9XIRRDkFE_J0OofifXzpNZNokDmTejpqFm2BOHAC0udFrXesjzcrcytfF9DSEmTrdM4HK","width":4032}],"place_id":"ChIJ76Ob1B6oQjQRxJj142dvXbY","plus_code":{"compound_code":"2F68+X4 Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+X4"},"price_level":1,"rating":4.1,"reference":"ChIJ76Ob1B6oQjQRxJj142dvXbY","scope":"GOOGLE","types":["restaurant","food","point_of_interest","establishment"],"user_ratings_total":110,"vicinity":"8樓, No. 161號, Section 1, Zhongshan Road, Banqiao District"},{"business_status":"OPERATIONAL","geometry":{"location":{"lat":25.0117723,"lng":121.4663207},"viewport":{"northeast":{"lat":25.01308888029151,"lng":121.4675942302915},"southwest":{"lat":25.0103909197085,"lng":121.4648962697085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png","icon_background_color":"#FF9E67","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet","name":"板橋鳴門和食料理","opening_hours":{"open_now":false},"photos":[{"height":3456,"html_attributions":["<a href=\"https://maps.google.com/maps/contrib/107995672993791603198\">鮮果棠</a>"],"photo_reference":"Aap_uEDwt8Io3jvfOxpECPvp5djH4FODwqUQmb1zlWMnTG4DVyB2u3NjFVRpMyLGho9zmu7nIphGxkr11iDIMr_MhZCx1D3bP5oIH4ZhiKG2No3sxGNHcxif7TFyqxrf01MEtlPmrC7rIrzmcPLW8e6ljdahufCTua5o-Y4PeW_CTMAE1Oza","width":4608}],"place_id":"ChIJx8QuLh-oQjQR7vRm6EYFTUg","plus_code":{"compound_code":"2F68+PG Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+PG"},"price_level":2,"rating":4,"reference":"ChIJx8QuLh-oQjQR7vRm6EYFTUg","scope":"GOOGLE","types":["restaurant","food","point_of_interest","establishment"],"user_ratings_total":201,"vicinity":"No. 3號, Lane 158, Section 1, Zhongshan Road, Banqiao District"},{"business_status":"OPERATIONAL","geometry":{"location":{"lat":25.0122763,"lng":121.4655369},"viewport":{"northeast":{"lat":25.0135274302915,"lng":121.4669269302915},"southwest":{"lat":25.0108294697085,"lng":121.4642289697085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png","icon_background_color":"#7B9EB0","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet","name":"彭園新板館｜婚宴場地 · 尾牙春酒 · 振興券優惠 · 年菜外帶","opening_hours":{"open_now":true},"photos":[{"height":1280,"html_attributions":["<a href=\"https://maps.google.com/maps/contrib/106577690922713967633\">彭園新板館｜婚宴場地 · 尾牙春酒 · 振興券優惠 · 年菜外帶</a>"],"photo_reference":"Aap_uEATdOsMwzAsDDXMEXvu2Nt2FxPJMVlW4FIjn7uUuVDIfyEDDefpZzwuzNdTgYIZ3eonj41WFOebQGa-TZo5cd3eJ2ORlUFJpBwYeBehNO0eqeL-FkF-eDQRPLMdm-J8R0t9TiHKSXhue7QZGcSSBAJ0Avna9ITHzUjKe1LVzL1877E","width":1920}],"place_id":"ChIJWWqX1R6oQjQRbfpbAaCZf3o","plus_code":{"compound_code":"2F68+W6 Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+W6"},"price_level":3,"rating":4,"reference":"ChIJWWqX1R6oQjQRbfpbAaCZf3o","scope":"GOOGLE","types":["meal_takeaway","restaurant","food","point_of_interest","establishment"],"user_ratings_total":1611,"vicinity":"1樓、8樓, No. 161號, Section 1, Zhongshan Road, Banqiao District"},{"business_status":"OPERATIONAL","geometry":{"location":{"lat":25.011805,"lng":121.4659791},"viewport":{"northeast":{"lat":25.0132364302915,"lng":121.4672665302915},"southwest":{"lat":25.0105384697085,"lng":121.4645685697085}}},"icon":"https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png","icon_background_color":"#FF9E67","icon_mask_base_uri":"https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet","name":"和緣餐飲有限公司","place_id":"ChIJ__8_Jx-oQjQRKvRWnBKQ6bs","plus_code":{"compound_code":"2F68+P9 Banqiao District, New Taipei City, Taiwan","global_code":"7QQ32F68+P9"},"reference":"ChIJ__8_Jx-oQjQRKvRWnBKQ6bs","scope":"GOOGLE","types":["restaurant","food","point_of_interest","establishment"],"vicinity":"1樓, No. 158, Section 1, Zhongshan Road, Banqiao District"}],"status":"OK"}"""
    # response_result = json.loads(response)# string(json) to json
    for item in response_result['results']:
        count += 1
        if 'rating' in item : #rating 星星數 但是不是每一家都有這個指標
            if item['rating']> 4: #rating 星星數閥值
                data = { #資料格式
                "name": (item['name']),
                "rating": item['rating'],
                "vicinity": item['vicinity'],
                "user_ratings_total":item['user_ratings_total'],
                "location":item['geometry']['location'],
                "place_id":item['place_id']
                }
                mainarray.append(data)

    while 'next_page_token' in response_result : #API只吐20筆所以必須用重複執行，繼續打API探詢資料直到沒有next_page_token
        url_ = url + "&pagetoken="+response_result['next_page_token']
        time.sleep(2)
        response = requests.request("GET", url_, headers=headers, data=payload)
        response_result=json.loads(response.text)
        print (url_)
        for item in response_result['results']:
            count += 1
            if 'rating' in item :
                if item['rating']> 4:
                    data = {
                    "name": (item['name']),
                    "rating": item['rating'],
                    "vicinity": item['vicinity'],
                    "user_ratings_total":item['user_ratings_total'],
                    "location":item['geometry']['location'],
                    "place_id":item['place_id']
                    }
                    mainarray.append(data)
    print ('總共比數',count)
    with open(f_name+".json", "w",encoding='utf8') as json_file: #因為有中文encoding='utf8'
        json.dump(mainarray, json_file, indent = 4, ensure_ascii=False)
    return (mainarray)


if __name__ == '__main__':
    #print (geocode('220新北市板橋區板新路121號'))
    #print (findPlaces('新北耶誕城'))
    #print ( findPlaces_range('25.03673346439152','121.56799188395895','500','restaurant',f_name) ) #'lat': 25.0122763,'lng': 121.4655369

    file_ = open("input.txt","r",encoding="utf-8")
    lines = file_.readlines()
    for line in lines:
        s=line.split(',')
        print (findPlaces_range(s[1],s[2],'500','restaurant',s[0])) # api參數 lat,lng,範圍,種類,檔名.json test
    file_.close()