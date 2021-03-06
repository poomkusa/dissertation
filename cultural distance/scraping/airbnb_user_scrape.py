import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import browsercookie #theres a newer browsercookie3
import re
import feather
import psutil
# import sys
# sys.setrecursionlimit(10000)
#import time
#from random import gauss

data = pd.read_csv("C:/Users/ThisPC/Desktop/New folder/2.csv")
data["country"] = np.nan
data["pic"] = np.nan
data["face_num"] = np.nan
data["gender"] = np.nan
data["age"] = np.nan
#data = data.iloc[0:5]
#create a selector based on class name in the website HTML
# selector = 'div._1ax9t0a'
picture_selector = 'img._9ofhsl'
#row number to begin with
i=0
#limit number of times the code try to access not found pages
first_time = True
error_count = 0
rownum = len(data)
#grab cookie from browser
cj = browsercookie.firefox()
ram = 0
while i!=rownum:
    try:
        if(first_time==True):
            print("loop number: "+str(i)+"/"+str(rownum))
            print(psutil.virtual_memory().percent)
        url = "https://www.airbnb.com/users/show/"+str(data.loc[i,"reviewer_id"])
        #ดึงข้อมูลจากเว็บที่เราสนใจ
        r = requests.get(url, cookies=cj)
        #แปลงเป็น type bs4.BeautifulSoup
        html_page = BeautifulSoup(r.text, "html.parser")
        # country = html_page.select_one(selector)
        country = str(html_page.find(text=re.compile('Lives in')))
        pic = str(html_page.select(picture_selector)[0]["src"])        
        if(not isinstance(data.loc[i,"country"], str)):
            # data.iloc[i,data.columns.get_loc("country")] = country.text
            data.loc[i,"country"] = str(country)
        if(not isinstance(data.loc[i,"pic"], str)):
            data.loc[i,"pic"] = str(pic)            
#        delay = gauss(6, 2)
#        time.sleep(delay)
        i+=1
        error_count = 0
        first_time = True        
        if(i%5000==0 or (psutil.virtual_memory().percent>95 and ram==0)):
            feather.write_dataframe(data, "C:/Users/ThisPC/Desktop/New folder/2.feather") 
            if(psutil.virtual_memory().percent>95):
                ram = 1           
    #stop and move on the next loop after 5 errors    
    except Exception as e:
        error_count+=1
        if(error_count==5):
            i+=1
            error_count = 0
            first_time = True
            continue
        first_time = False
        print("---"+str(e))
feather.write_dataframe(data, "C:/Users/ThisPC/Desktop/New folder/2.feather")
#data.to_pickle("/home/poom/Desktop/dummy.pkl")
#data = pd.read_pickle("/home/poom/Desktop/dummy.pkl")

#for finding the last scraped row when resuming the scrape
data.index[data['country'].isnull() == False]
data.iloc[data.index[data['country'].isnull() == False]].tail()
data.iloc[320997:321011]



#check and combine all scraped data
df1 = pd.read_pickle("/home/poom/Desktop/1.pkl")
df2 = pd.read_pickle("/home/poom/Desktop/6.pkl")
df = df1
df["compare"] = df2["country"]
df1.index[df1['country'].isnull() == False]
df2.index[df2['country'].isnull() == False]
df = df.iloc[400000:400999]
df['country'].equals(df['compare'])
df['RowNotEqual'] = df.country == df.compare
#combine
df1 = df1.iloc[0:400000]
df2 = df2.iloc[400000:516369]
x = pd.concat([df1, df2], ignore_index=True)
#check
x.loc[400000 - 5:400000 + 5,["country"]]
x.index[x["country"].isnull() == False]
x.index[x["country"].isnull() == True]
y = x.loc[0:219099,["country"]]
y.index[y["country"].isnull() == True]
x.to_pickle("/home/poom/Desktop/combine.pkl")
pd.DataFrame(data=x.country.unique())


import pickle

outfile = open("/home/poom/Desktop/user_data.pkl", 'wb') # 'wb' instead 'w' for binary file
pickle.dump(data, outfile)
outfile.close()   

infile = open("/home/poom/Desktop/dogs",'rb')
data = pickle.load(infile)
infile.close()
