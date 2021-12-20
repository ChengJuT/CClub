# -----目前已知錯誤訊息-----
'''instaloader.exceptions.ConnectionException: Login error: "fail" status, message "feedback_required": 代表爬蟲次數太頻繁被禁了，需等待一定時間後再登入.'''
'''JSON Query to explore/locations/199494240937537/: HTTP error code 500. [retrying; skip with ^C]: 可能是爬蟲次數太頻繁導致伺服器暫時無回應 instaloader會等待一段時間後自動繼續 不需按任何按鍵'''
'''KeyError: 'edge_hashtag_to_top_posts: 和下面的400 Bad Request一起出現 目前無解'''
'''instaloader.exceptions.QueryReturnedBadRequestException: 400 Bad Request 帳號被blocked 目前無解'''
# 程式中有#######################的部分爬蟲過程會印在cmd裡面幫助了解爬到的資料情況 若不想顯示可以comment掉

# -----輸入IG帳號密碼-----
'''一開始會要求輸入帳號密碼'''
username, password = input("Please input your IG username (email) and password (空格隔開): ").split() 

import instaloader
from datetime import datetime
import time
import pandas as pd
import numpy as np

def check_location(post):
        # -----將座標進行四捨五入至小數第二位-----
        def round_to_even(lat, lng, decimal):
                lng = float(np.round(lng/2, decimal))*2
                lat = float(np.round(lat/2, decimal))*2
                return (lat, lng)
        # -----確認地點存在且位置位於中華民國管轄區域
        location = post.location
        if location != None:
                name = location[1]
                latitude = location[4]
                longtitude = location[5]
                if latitude != None and longtitude != None:
                        if (21.5 < latitude < 26.5) and (118 < longtitude < 122.5):
                                return {"name": name, "coord": (latitude, longtitude), "grid": round_to_even(latitude, longtitude, 2)}
        return False

def record_data(data, likes, postdate, post_link, location):
        data = data.append({"Likes": likes, "Date": postdate,"Location": location["name"], "Location_coord": location["coord"], 
                        "Grid_coord": location["grid"], "Post_url": post_link}, ignore_index=True)
        return data

def search_post(keywords, since, until, data, keyword_type):
        for keyword in keywords:
                # -----初始化k值-----   
                k = 0
                # -----產生貼文iterator-----
                posts = instaloader.Hashtag.from_name(driver.context, keyword).get_top_posts() if keyword_type == "top" else instaloader.Hashtag.from_name(driver.context, keyword).get_all_posts()

                count = 0
                for post in posts:
                        time.sleep(10)
                        postdate = post.date_local
                        ###############################################
                        print(postdate)
                        ###############################################
                        # -----在特定時間範圍的貼文才紀錄
                        if postdate > until:
                                continue
                        elif postdate < since:
                                # -----用k值檢查確保不是突然有一篇很舊的貼文出現，需要連續20篇舊貼文才會停止迴圈-----
                                k += 1
                                if k == 20:
                                        break
                        else:
                                # -----記錄k值、初始化k值
                                k_list.append(k)
                                k = 0
                                # -----取得貼文讚數-----
                                likes = post.likes
                                ###############################################
                                print(likes)
                                ###############################################
                                # -----對於熱門Hashtag，只選取讚數超過100的貼文
                                if keyword_type == "top":
                                        if likes < 100:
                                                continue
                                # -----取得貼文網址，檢查貼文是否重複-----
                                post_link = f"https://www.instagram.com/p/{post.shortcode}"
                                if post_link in searched_post:
                                        continue
                                searched_post.append(post_link)
                                # -----取得貼文資料(有地點的才記錄)-----
                                location = check_location(post)
                                if location:
                                        data = record_data(data, likes, postdate, post_link, location)
                                        count += 1
                                        ###############################################
                                        print(count)
                                        ###############################################
                                        # -----每種關鍵字抓50個貼文-----                       
                                        if count >= 50: 
                                                time.sleep(300)
                                                break
                                ###############################################
                                else:
                                        print("No location!")
                                ###############################################
        return data

# -----設定Instaloader-----
driver = instaloader.Instaloader(download_pictures=False, download_comments=False, download_videos=False, download_video_thumbnails=False)
driver.login(username, password)

# -----設定儲存資料的Dataframe以及搜尋關鍵字-----
data = pd.DataFrame({"Likes": [], "Date": [],
                "Location": [], "Location_coord": [],
                "Grid_coord": [], "Post_url": []})
keywords_1 = ["聖誕節", "聖誕樹"] #熱門關鍵字
keywords_2 = ["蒐集聖誕樹", "收集聖誕樹", "聖誕景點"] #其他關鍵字
searched_post = list() # 存取已出現並記錄過的貼文
k_list = [0] # 記錄k值作為tuning用途

# -----設定特定時間貼文-----
'''要改的地方在這裡'''
since = datetime(2021, 12, 15)
until = datetime(2021, 12, 18)

# -----執行search_post函式-----
data = search_post(keywords_1, since, until, data, "top")
data = search_post(keywords_2, since, until, data, "all")

# -----將dataframe排序並輸出成csv檔-----
data = data.sort_values(by=["Grid_coord", "Likes"], ascending=False)
data.to_csv(f"{since.date()}_{until.date()}.csv", encoding='utf-8-sig', index=False)

###############################################
print(f"max k is {max(k_list)}")
###############################################
