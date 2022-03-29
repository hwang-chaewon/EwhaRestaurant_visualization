#!/usr/bin/env python
# coding: utf-8

# In[1]:


#https://data101.oopy.io/recommendation-engine-cosine-similarity-naver-version-code-sharing

import pandas as pd
import numpy as np

df = pd.read_csv('shops.csv', sep=',')  

columns = ['상호명', '상권업종대분류명','상권업종소분류명', 
           '시도명', '시군구명', '행정동명', '도로명주소', 
           '경도', '위도']
df=df[columns].copy()

df = df.loc[(df['시군구명'] == '서대문구')]  #서대문구에 있는 음식점만

df_ = df.loc[df.상권업종대분류명 =="음식"]  #음식점만

dong=list(sorted(set(list((df_['행정동명'])))))
len(dong)
dong

dong_list=[]
for i in range(len(dong)): 
    dong_list.append(df_.loc[df.행정동명==dong[i]])
    i+=1
dong_list[0]


# In[2]:


get_ipython().system('pip install selenium')


# In[3]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

chromedriver = 'C:/Users/ChaeWon/crawling/chromedriver.exe' 
driver = webdriver.Chrome(chromedriver) 
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

dong_list[0]

CH = dong_list[0]

CH.to_csv("충현동.csv", mode='w')


# In[4]:


naver_map_type_list = []
blog_review_list = []
blog_review_qty_list = []
naver_map_star_review_stars_list = []
naver_map_star_review_qty_list = []
chromedriver = 'C:/Users/ChaeWon/crawling/chromedriver.exe' 

# 메인 드라이버 : 별점 등을 크롤링
driver = webdriver.Chrome(chromedriver) 

# 서브 드라이버 : 블로그 리뷰 텍스트를 리뷰 탭 들어가서 크롤링
sub_driver = webdriver.Chrome(chromedriver)

for i, url in enumerate(dong_list[0]['naver_map_url']):

    driver.get(url)
    sub_driver.get(url+"/review/ugc")
    time.sleep(2)


    try:

        # 간단 정보 가져오기
        
        # 네이버 지도의 유형 분류
        naver_map_type = driver.find_element_by_css_selector("#_title > span._3ocDE").text

        # 블로그 리뷰 수
        blog_review_qty = driver.find_element_by_css_selector("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR > div > span:nth-child(3) > a > em").text

        # 블로그 별점 점수
        star_review_stars = driver.find_element_by_css_selector("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR > div > span._1Y6hi._1A8_M > em").text

        # 블로그 별점 평가 수
        star_review_qty = driver.find_element_by_css_selector("#app-root > div > div > div.place_detail_wrapper > div.place_section.no_margin.GCwOh > div > div > div._3XpyR > div > span:nth-child(2) > a > em").text
       

        # 블로그 리뷰 텍스트 가져오기
        review_text_list = [] # 임시 선언

        
        # 네이버 지도 블로그 리뷰 탭은 동적 웹사이트의 순서가 주문하기, 메뉴보기 등의 존재 여부로 다르기 때문에 css selector가 아니라 element 찾기로 진행
        review_text_crawl_list = sub_driver.find_elements_by_class_name("_2CbII")
        
        # find element's' 메소드를 통해 가져온 내용은 리스트로 저장되고, 리스트 타입을 풀어서(for문 사용) 임시 데이터에 모아 두어야 한다
        for review_crawl_data in review_text_crawl_list:
            review_text_list.append(review_crawl_data.find_element_by_tag_name('div').text)
        
        # 그 리스트에 저장된 텍스트 (한 식당에 대한 여러 리뷰들)를 한 텍스트 덩어리로 모아(join)줍니다.
        review_text = ','.join(review_text_list)


        blog_review_list.append(review_text) #리뷰 내용

        naver_map_type_list.append(naver_map_type)
        blog_review_qty_list.append(blog_review_qty)
        naver_map_star_review_stars_list.append(star_review_stars)
        naver_map_star_review_qty_list.append(star_review_qty)

    # 리뷰가 없는 업체는 크롤링에 오류가 뜨므로 표기해둡니다.
    except Exception as e1:
        print(f"{i}행 문제가 발생")
        
        # 리뷰가 없으므로 null을 임시로 넣어줍니다.
        blog_review_list.append('null')  
        naver_map_type_list.append('null')
        blog_review_qty_list.append('null')
        naver_map_star_review_stars_list.append('null')
        naver_map_star_review_qty_list.append('null')
 
driver.quit()
sub_driver.quit()


dong_list[0]['naver_store_type'] = naver_map_type_list  # 네이버 상세페이지에서 크롤링한 업체 유형
dong_list[0]['naver_star_point'] = naver_map_star_review_stars_list  # 네이버 상세페이지에서 평가한 별점 평점
dong_list[0]['naver_star_point_qty'] = naver_map_star_review_qty_list  # 네이버 상세페이지에서 별점 평가를 한 횟수
dong_list[0]['naver_blog_review_qty'] = blog_review_qty_list
dong_list[0]['naver_blog_review'] = blog_review_list


# In[5]:


dong_list[0] = dong_list[0].loc[~(dong_list[0]['naver_store_type'].str.contains('null'))]

dong_list[0][['naver_star_point', 'naver_star_point_qty', 'naver_blog_review_qty']] = dong_list[0][['naver_star_point', 'naver_star_point_qty', 'naver_blog_review_qty']].apply(pd.to_numeric)


# In[10]:


dong_list


# In[11]:


blog_review_list


# In[ ]:




