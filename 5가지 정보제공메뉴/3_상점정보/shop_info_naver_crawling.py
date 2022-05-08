#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


df = pd.read_csv('C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/shops_seoul.csv', sep=',', encoding = 'cp949')  

columns = ['상호명', '상권업종대분류명','상권업종소분류명', 
           '시도명', '시군구명', '행정동명', '도로명주소', 
           '경도', '위도']
print(df.shape)
df=df[columns].copy()
df = df.loc[df['시군구명'] == '서대문구']
df_ = df.loc[df['상권업종대분류명'] =="음식"]
dong=sorted(set(list((df_['행정동명']))))
print(dong)
dong_list=[]
for i in range(len(dong)): 
    dong_list.append(df_.loc[df.행정동명==dong[i]])
    i+=1
dong_list[0]


# In[2]:


dong_list=[]
for i in range(len(dong)): 
    dong_list.append(df_.loc[df.행정동명==dong[i]])
    i+=1
dong_list[0]


# In[6]:


from selenium import webdriver
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


# In[4]:


chromedriver = 'C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/chromedriver.exe' 
driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options) 
dong_list[0]['naver_keyword'] = dong_list[0]['행정동명']+'%20'+dong_list[0]['상호명']
dong_list[0]['naver_map_url'] = ''

# url 가져오기

for i, keyword in enumerate(dong_list[0]['naver_keyword'].tolist()):
    print("이번에 찾을 키워드 :", i, f"/ {dong_list[0].shape[0] -1} 행", keyword)
    try:
        naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5"
        driver.get(naver_map_search_url)
        
        time.sleep(3.5)
        dong_list[0].iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')

        #검색결과 없는 경우
    except Exception as e1:
        if "li:nth-child(1)" in str(e1):
            try:
                dong_list[0].iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                dong_list[0].iloc[i,-1] = np.nan
                time.sleep(1)
        else:
            pass


driver.quit()


# url 만들어주기
dong_list[0]['naver_map_url'] = "https://m.place.naver.com/restaurant/" + dong_list[0]['naver_map_url']


# URL이 수집되지 않은 데이터는 제거합니다.
dong_list[0] = dong_list[0].loc[~dong_list[0]['naver_map_url'].isnull()]


# In[5]:


dong_list[0].head()


# In[6]:


CH = dong_list[0]

CH.to_csv("url포함_1.csv", mode='w')


# In[8]:


get_ipython().system('pip install tqdm')
from tqdm import tqdm_notebook


# In[9]:


get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')


# In[10]:


df['naver_map_url'][5]


# In[3]:


#참고: https://soyoung-new-challenge.tistory.com/20
#https://ltlkodae.tistory.com/18
from selenium import webdriver
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

get_ipython().system('pip install tqdm')
from tqdm import tqdm_notebook

import pandas as pd

import requests
from bs4 import BeautifulSoup
chromedriver = 'C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/chromedriver.exe' 
get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')

driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options) 

df = pd.read_csv('C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/url포함_1.csv', sep=',', encoding = 'utf-8-sig')

delivery_text_list=[]
delivery_bool_list=[]

for i, url in enumerate(tqdm_notebook(df['naver_map_url'])):
    req = requests.get(url, headers = {
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})
    ### 중간에 오류가 나길래 headers를 추가해줬습니다.
    req.encoding = 'utf-8'
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    driver.get(url)
    time.sleep(2)


    # 간단 정보 가져오기
    store_name = driver.find_element_by_css_selector("#_title > span._3XamX").text
    print("_____________________________")
    print('<',store_name,'>')
        
    try:    
        delivery_text = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin._18vYz > div > ul").text
        print('배달 가능 여부 포함 text: ',delivery_text)
        delivery_text_list.append(delivery_text)
        if '배달' in delivery_text_list[i]:
            delivery_bool_list.append('Yes')
        else:
            delivery_bool_list.append('n')
    except:
        print(f"{i}행 표시 없음")
        delivery_bool_list.append('n')
        
driver.quit()

df['delivery_bool'] = delivery_bool_list


# In[4]:


df.to_csv("배달여부포함_2.csv", mode='w')


# In[33]:


from selenium import webdriver
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

get_ipython().system('pip install tqdm')
from tqdm import tqdm_notebook

import pandas as pd

import requests
from bs4 import BeautifulSoup
chromedriver = 'C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/chromedriver.exe' 
get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')

driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options) 

df = pd.read_csv('C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/배달여부포함_2.csv')  

office_hour_start_list=[]

#밤에 돌리기(낮에는 주석처리): 영업 시작 시간
for i, url in enumerate(tqdm_notebook(df['naver_map_url'])):
    req = requests.get(url, headers = {
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})
    req.encoding = 'utf-8'
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    driver.get(url)
    time.sleep(2)


    # 간단 정보 가져오기
    store_name = driver.find_element_by_css_selector("#_title > span._3XamX").text
    print("_____________________________")
    print('<',store_name,'>')
    
    #새벽 3시에 돌리기: 영업 시작 시간
    try:    
        o_h_s = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._2KHqk > div > a > div > div > div > span").text
        print('영업 시간:' ,o_h_s)
        office_hour_start_list.append(o_h_s[:5])
    except:
        print(f"{i}행 표시 없음")
        office_hour_start_list.append('n')
        
#     try:
#         driver.find_element(By.CLASS_NAME, "_1aKLL").click()
#         time.sleep(1)
#     except: 
#         print('못 내림')

#     try:    
#         o_h_s = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._2KHqk > div > a").text
#         print('영업 시간:' ,o_h_s)  
#     except:
#         print(f"{i}행 표시 없음")
#         office_hour_start_list.append('n')
        
driver.quit()

df['office_hour_start'] = office_hour_start_list


# In[34]:


df.to_csv("영업시작포함_3.csv", mode='w')


# In[11]:


import pandas as pd
df = pd.read_csv('C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/일영업시작포함_3.csv') 
df1=df.rename(columns={'office_hour_start':'일_start'})
df1.to_csv("일영업시작포함_3.csv", mode='w')


# In[1]:


from selenium import webdriver
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

get_ipython().system('pip install tqdm')
from tqdm import tqdm_notebook

import pandas as pd

import requests
from bs4 import BeautifulSoup
chromedriver = 'C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/chromedriver.exe' 
get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')

driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options) 

df = pd.read_csv('C:/Users/ChaeWon/Documents/3-1/파이썬과데이터분석/crawling/일영업시작포함_3.csv')  

office_hour_end_list=[]

for i, url in enumerate(tqdm_notebook(df['naver_map_url'])):
    req = requests.get(url, headers = {
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})
    ### 중간에 오류가 나길래 headers를 추가해줬습니다.
    req.encoding = 'utf-8'
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    driver.get(url)
    time.sleep(2)


    # 간단 정보 가져오기
    store_name = driver.find_element_by_css_selector("#_title > span._3XamX").text
    print("_____________________________")
    print('<',store_name,'>')
            
    #오후 3:10에 돌리기: 영업 종료 시간        
    try:    
        o_h_end = driver.find_element_by_css_selector("#app-root > div > div > div > div:nth-child(5) > div > div.place_section.no_margin._18vYz > div > ul > li._1M_Iz._2KHqk > div > a > div > div > div > span").text
        print('영업 시간:' ,o_h_end)
        office_hour_end_list.append(o_h_end[:5])
    except:
        print(f"{i}행 표시 없음")
        office_hour_end_list.append('n')
        
driver.quit()

df['일_end'] = office_hour_end_list


# In[2]:


df.to_csv("영업시간_일_4.csv", mode='w')

