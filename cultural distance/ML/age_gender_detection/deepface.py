#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 07:14:54 2020

@author: poom
"""

from deepface import DeepFace
import urllib.request
from urllib.error import HTTPError
import pandas as pd
import numpy as np
import progressbar
data = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data.pkl")

data = data[['listing_id','id','pic']]
with progressbar.ProgressBar(max_value=len(data)) as bar:
    for i in range(len(data)):
        bar.update(i)
        #skip if the user profile page no longer exists
        if(str(data.iloc[i,data.columns.get_loc("pic")])=="nan"):
            continue
        try:
            #save pic from the website into local folder
            pic = urllib.request.urlretrieve(data.iloc[i,data.columns.get_loc("pic")], "pic")
            face_ret, age_ret, gender_ret, agePreds, genderPreds, faceBoxes, points = analyze_pic()
            data.face_num[i] = face_ret
            if face_ret == 1:
                data.age[i] = age_ret[0]
                data.gender[i] = gender_ret[0]
                data.age_conf[i] = agePreds[0]
                data.gender_conf[i] = genderPreds[0]
                data.face[i] = faceBoxes[0]
                data.points[i] = points
        #user profile page exists, but theres no profile picture
        except HTTPError:
            continue
        except Exception as e:
            print("")
            print("index: "+str(i))
            print(str(e))
            print("=============================================================================")
# ==================================================================================================================
        if(i%100==0 | i==len(data)-1):
            data.to_pickle("/home/poom/Desktop/dummy.pkl")
            
       
pic = urllib.request.urlretrieve(data.iloc[0,data.columns.get_loc("pic")], "pic")
demography = DeepFace.analyze(pic) #passing nothing as 2nd argument will find everything
#demography = DeepFace.analyze("img4.jpg", ['age', 'gender', 'race', 'emotion']) #identical to the line above
#demographies = DeepFace.analyze(["img1.jpg", "img2.jpg", "img3.jpg"]) #analyzing multiple faces same time
print("Age: ", demography["age"])
print("Gender: ", demography["gender"])
print("Emotion: ", demography["dominant_emotion"])
print("Race: ", demography["dominant_race"])











