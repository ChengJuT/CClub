"""
使用Instaloader收集特定hashtag貼文
"""
# -----錯誤訊息-----
'''instaloader.exceptions.ConnectionException: Login error: "fail" status, message "feedback_required".'''
'''代表爬蟲次數太頻繁被禁了，需等待一定時間後再登入'''
'''JSON Query to explore/locations/199494240937537/: HTTP error code 500. [retrying; skip with ^C]'''
'''似乎代表instaloader要求次數太多暫時被IG擋了，instaloader會自動等待一定時間(時間未知)再嘗試 直到可以繼續work'''
'''IG似乎有限制一天只能request500次?'''
import instaloader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import requests
import datetime
import os, time
import pandas as pd

def login_instagram(account, password):
        # -----開瀏覽器-----
        Chrome_driver.get('https://www.instagram.com/')
        # -----等待頁面出現-----
        WebDriverWait(Chrome_driver, 30).until(EC.presence_of_element_located((By.NAME, 'username'))) #等待最長30秒，直到輸入帳號的地方出現
        # -----輸入帳號密碼-----
        username_input = Chrome_driver.find_element(By.NAME, 'username')
        username_input.send_keys(account)
        password_input = Chrome_driver.find_element(By.NAME, 'password')
        password_input.send_keys(password)
        # -----找到登入按鈕並點擊-----
        login_click = WebDriverWait(Chrome_driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
        login_click.click()

def check_ospath(path, keyword):
        if not os.path.exists(os.path.join(path, keyword)):
                os.makedirs(os.path.join(path, keyword))

def get_img_link(post):
        try:
                img_link = post.url
        # -----若無法直接取得則需透過selenium手動取得-----
        except KeyError: 
                post_link = f"https://www.instagram.com/p/{post.shortcode}"
                Chrome_driver.get(post_link)
                try:
                        img_link = WebDriverWait(Chrome_driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'FFVAD'))).get_attribute('src')
                except TimeoutException:
                        time.sleep(300) #等待5分鐘再進行
                        Chrome_driver.refresh() #重新整理
                        img_link = WebDriverWait(Chrome_driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'FFVAD'))).get_attribute('src')
        return img_link

def save_img(keyword, post, img_link):
        save_as = os.path.join(path, keyword) + f'\\{keyword}_{post.likes}.jpg'
        file = requests.get(img_link)
        with open(save_as, mode='wb') as f:
                f.write(file.content)


# -----設定Selenium登入IG-----
my_Options = Options()
my_Options.add_argument("--headless")
my_Options.add_argument("--incognito")
Chrome_driver = webdriver.Chrome(options=my_Options)
login_instagram("daniel860305@gmail.com", "dANiel0938525509")

# -----設定Instaloader-----
driver = instaloader.Instaloader(download_pictures=True, download_comments=False, download_videos=False, download_video_thumbnails=True)
driver.login("daniel860305@gmail.com", "dANiel0938525509")

# -----設定儲存資料的Dataframe以及要搜尋關鍵字-----
data = pd.DataFrame({"Profile": [], "Profile_followers": [], "Likes": [], "Date": [],"Location": [], "Location_coord": [], "Post_url": [], "Img_link": []})
# keywords = ["聖誕節", "聖誕樹", "聖誕快樂", "聖誕節快樂", "聖誕景點"]
keywords = ["聖誕節", "聖誕樹"]
path = 'D:\\ccClub期末專案'

# -----設定特定時間貼文-----
since = datetime.datetime(2021, 12, 8)
until = datetime.datetime(2021, 12, 14)

searched_post = list()
for keyword in keywords:     
        # -----設定好存檔路徑-----
        # check_ospath(path, keyword)

        k = 0 #initiate k
        k_list = list() # for tuning k

        # -----產生貼文generator-----
        posts = instaloader.Hashtag.from_name(driver.context, keyword).get_top_posts()
        count = 0
        for post in posts:
                time.sleep(5)
                postdate = post.date_local
                # -----在特定時間之後的貼文才紀錄
                if postdate > until:
                        continue
                elif postdate < since:
                        k += 1
                        if k == 10:
                                break
                else:
                        # -----取得貼文資料(有地點的才記錄)-----
                        if post.location != None:
                                if post.location.lat != None:
                                        # -----取得貼文網址
                                        post_link = f"https://www.instagram.com/p/{post.shortcode}"
                                        if post_link in searched_post:
                                                continue
                                        searched_post.append(post_link)
                                        # -----取得貼文相關資料-----
                                        img_link = get_img_link(post)
                                        author = post.profile
                                        author_followees = instaloader.Profile.from_username(driver.context, post.profile).followees
                                        likes = post.likes
                                        date = post.date
                                        location = post.location.name
                                        coordinate = (post.location.lat, post.location.lng)
                                        # -----資料存入Dataframe，依序為發文者、發文者追蹤數、貼文讚數、貼文日期、地點、地點座標、貼文網址、圖片網址-----  
                                        data = data.append({"Profile": author, "Profile_followers": author_followees, 
                                                        "Likes": likes, "Date": date,"Location": location, "Location_coord": coordinate, "Post_url": post_link, "Img_link": img_link}, ignore_index=True)
                                        count += 1
                                        print(count)
                                        # -----儲存圖片、計數-----
                                        # try:
                                        #         save_img(keyword, post, img_link)
                                        #         count += 1
                                        #         print(count)
                                        # except:
                                        #         continue
                        k_list.append(k)
                        k = 0 # reset k to 0
                # -----每種關鍵字抓100個貼文-----                       
                if count >= 100: 
                        time.sleep(300)
                        break


# -----將dataframe排序並輸出成csv檔-----
data = data.sort_values(by=["Location", "Likes", "Profile_followers"], ascending=False)
data.to_csv("聖誕節熱門貼文.csv", encoding='utf-8-sig', index=False)
print(max(k_list))

