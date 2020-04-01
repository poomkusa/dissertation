# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
#import time
#from random import gauss

data = pd.read_csv("/home/poom/Desktop/reviewer_id.csv")
data["country"] = np.nan
data["pic"] = np.nan
#data = data.iloc[0:5]
selector = 'div._910j1c5'
i=0
first_time = True
error_count = 0
rownum = len(data)
while i!=rownum:
    try:
        if(first_time==True):
            print("loop number: "+str(i)+"/"+str(rownum))
        #ดึงข้อมูลจากเว็บที่เราสนใจ
        r = requests.get("https://www.airbnb.com/users/show/"+str(data.iloc[i,data.columns.get_loc("reviewer_id")]))
        #แปลงเป็น type bs4.BeautifulSoup
        html_page = BeautifulSoup(r.text, "html.parser")
        country = html_page.select_one(selector)
        data.iloc[i,data.columns.get_loc("country")] = country.text
#        delay = gauss(6, 2)
#        time.sleep(delay)
        i+=1
        error_count = 0
        first_time = True
        if(i%2==0):
            data.to_pickle("/home/poom/Desktop/dummy.pkl")
    except Exception as e:
        error_count+=1
        if(error_count==10):
            i+=1
            error_count = 0
            first_time = True
            continue
        first_time = False
        print("---"+str(e))
#data.to_pickle("/home/poom/Desktop/dummy.pkl")
#data = pd.read_pickle("/home/poom/Desktop/dummy.pkl")