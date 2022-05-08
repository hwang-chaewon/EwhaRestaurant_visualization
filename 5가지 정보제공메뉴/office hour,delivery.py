#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
df = pd.read_csv('영업시간_일_4.csv',)  
day=input("오늘은 무슨 요일인가요?: ")
store=input("영업시간을 알고 싶은 가게 이름을 입력하세요: ")
#https://www.delftstack.com/ko/howto/python-pandas/pandas-get-index-of-row/
ii=df.index[df['상호명'].str.contains(store)].tolist() 
i=ii[0]
if day=='월' or day=='월요일':
    if df['월_start'][i]=='n':
        print(df['상호명'][i]+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['월_start'][i]+'~'+df['월_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
elif day=='화' or day=='화요일':
    if df['화_start'][i]=='n':
        print(df['상호명'][i]+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['화_start'][i]+'~'+df['화_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
elif day=='수' or day=='수요일':
    if df['수_start'][i]=='n':
        print('<'+df['상호명'][i]+'>'+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['수_start'][i]+'~'+df['수_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
elif day=='목' or day=='목요일':
    if df['목_start'][i]=='n':
        print('<'+df['상호명'][i]+'>'+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['목_start'][i]+'~'+df['목_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
elif day=='금' or day=='금요일':
    if df['금_start'][i]=='n':
        print('<'+df['상호명'][i]+'>'+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['금_start'][i]+'~'+df['금_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
elif day=='토' or day=='토요일':
    if df['토_start'][i]=='n':
        print('<'+df['상호명'][i]+'>'+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['토_start'][i]+'~'+df['토_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
elif day=='일' or day=='일요일':
    if df['일_start'][i]=='n':
        print('<'+df['상호명'][i]+'>'+"는 영업시간이 표시되어 있지 않은 가게입니다")
    else:
        print('<'+df['상호명'][i]+'>'+"의 영업시간: "+df['일_start'][i]+'~'+df['일_end'][i])
    if df['delivery_bool'][i]=='Yes':
        print("배달 가능한 가게입니다")
else:
    print('잘못된 입력입니다.')

