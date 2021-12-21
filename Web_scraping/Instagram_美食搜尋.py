# 程式中有#######################的部分爬蟲過程會印在cmd裡面幫助了解爬到的資料情況 若不想顯示可以comment掉

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import re
import time
import json
import pandas as pd

def login_instagram(account, password):
        # -----開瀏覽器-----
        driver.get('https://www.instagram.com/')
        # -----等待頁面出現-----
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'username'))) #等待最長30秒，直到輸入帳號的地方出現
        # -----輸入帳號密碼-----
        username_input = driver.find_element(By.NAME, 'username')
        username_input.send_keys(account)
        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys(password)
        # -----找到登入按鈕並點擊-----
        login_click = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
        login_click.click()

def record_data(data, food, post_link):
        data = data.append({"Location": food["name"], "Location_coord": (food["location"]["lat"], food["location"]["lng"]),
                                        "rating": food["rating"], "Post_url": post_link}, ignore_index=True)
        return data

def search_post(Foods, data):
        for food in Foods:
                # -----根據店家名稱搜尋貼文-----
                name = re.sub(r'[^\w]', "", food["name"].replace(" ", ""))
                ################################
                print(name)
                ################################
                search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
                search.send_keys(name)
                time.sleep(1)
                try:
                        # -----找到搜尋結果並點入-----
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '-qQT3')))
                        search.send_keys(Keys.RETURN)
                        time.sleep(1)
                        search.send_keys(Keys.RETURN)
                        time.sleep(10)
                        # -----找到第一篇貼文的網址-----        
                        try:
                                post = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')))
                                post_link = post.find_element_by_tag_name('a').get_attribute("href")
                                ########################
                                print(post_link)
                                ########################
                                data = record_data(data, food, post_link)
                                time.sleep(5)
                        except TimeoutException:
                                # -----有時候瀏覽器會遇到HTTP 500無回應 須等5分鐘重新整理-----
                                time.sleep(300) #等待5分鐘再進行
                                driver.refresh() #重新整理
                                try:
                                        post = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')))
                                        post_link = post.find_element_by_tag_name('a').get_attribute("href")
                                        ########################
                                        print(post_link)
                                        ########################
                                        data = record_data(data, food, post_link)
                                        time.sleep(5)
                                except TimeoutException:
                                        print("No posts.")
                                        continue
                except TimeoutException:
                        print(f"Posts with {name} not found.")
                        search.clear()
                        time.sleep(1)
                        continue
        return data

# -----輸入IG帳號密碼-----
'''一開始會要求輸入帳號密碼'''
username, password = input("Please input your IG username (email) and password (空格隔開): ").split()

# -----設定Selenium登入IG-----
my_Options = Options()
# my_Options.add_argument("--headless")
my_Options.add_argument("--incognito")
driver = webdriver.Chrome("E:\python\ccClub\期末專案\Web_scraping\chromedriver.exe", options=my_Options)
login_instagram(username, password)

# -----設定儲存資料的Dataframe以及搜尋關鍵字-----
data = pd.DataFrame({"Location": [], "Location_coord": [], "rating": [], "Post_url": []})

# -----讀取美食店家資料-----
with open("E:\python\ccClub\期末專案\Web_scraping\信義A13.json", mode="r", encoding= "utf-8-sig") as f:
        Foods = json.load(f)

# -----執行search_post函式-----
data = search_post(Foods, data)
# -----將dataframe排序並輸出成csv檔-----
data.to_csv("美食熱門貼文.csv", encoding='utf-8-sig', index=False)

