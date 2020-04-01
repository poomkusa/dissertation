#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 12:42:16 2020

@author: poom
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:41:12 2020

@author: poom
"""

import cv2
#import math
#import argparse
import urllib.request
import pandas as pd
from matplotlib import pyplot as plt
data = pd.read_pickle("/home/poom/Desktop/combine.pkl")
#data = data.iloc[0:99]

#initialize ML var
faceHaar="/home/poom/Desktop/haarcascade_frontalface_default.xml"
ageProto="/home/poom/Desktop//age_deploy.prototxt"
ageModel="/home/poom/Desktop/age_net.caffemodel"
genderProto="/home/poom/Desktop/gender_deploy.prototxt"
genderModel="/home/poom/Desktop/gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

facecascade = cv2.CascadeClassifier(faceHaar)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

pic_link=data.iloc[6,data.columns.get_loc("pic")]
urllib.request.urlretrieve(pic_link, "/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/pic")
padding=20
frame = cv2.imread('/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/pic')


imgtest1 = frame.copy()
imgtest = cv2.cvtColor(imgtest1, cv2.COLOR_BGR2GRAY)
faceBoxes=[]
faces = facecascade.detectMultiScale(imgtest, scaleFactor=1.2, minNeighbors=5)
for (x, y, w, h) in faces:
    x1=x
    y1=y
    x2=x+w
    y2=y+h
    faceBoxes.append([x1,y1,x2,y2])
    imgtest = cv2.rectangle(imgtest, (x1, y2), (x2, y2), (255, 0, 255), 2)
roi_gray = imgtest[y:y+h, x:x+w]
roi_color = imgtest[y:y+h, x:x+w]
plt.imshow(imgtest)


for faceBox in faceBoxes:
    coor1 = max(0,faceBox[1]-padding)
    coor2 = min(faceBox[3]+padding,frame.shape[0]-1)
    coor3 = max(0,faceBox[0]-padding)
    coor4 = min(faceBox[2]+padding, frame.shape[1]-1)
    face=frame[max(0,faceBox[1]-padding):
               min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
               :min(faceBox[2]+padding, frame.shape[1]-1)]
    
    blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds=genderNet.forward()
    gender=genderList[genderPreds[0].argmax()]
    print(f'Gender: {gender}')
    
    ageNet.setInput(blob)
    agePreds=ageNet.forward()
    age=ageList[agePreds[0].argmax()]
    print(f'Age: {age[1:-1]} years')
    
#cv2.imshow('ImageWindow', resultImg)
#cv2.waitKey()
#or
#cv2.imshow('ImageWindow', resultImg)
#cv2.waitKey(1000)
#cv2.destroyAllWindows()