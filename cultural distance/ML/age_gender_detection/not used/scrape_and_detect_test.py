#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:01:19 2020

@author: poom
"""

import cv2
#import math
#import argparse
import urllib.request
import pandas as pd
import random

data = pd.read_pickle("/home/poom/Desktop/combine.pkl")
#data = data.iloc[0:99]

def highlightFace(frame):
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
        cv2.rectangle(imgtest1, (x1,y1), (x2,y2), (0,255,0), int(round(imgtest1.shape[0]/150)), 8)
    return imgtest1, faceBoxes
    
def analyze_pic(pic_link):
#    parser=argparse.ArgumentParser()
#    parser.add_argument('--image')
    
#    args=parser.parse_args()
    
#    video=cv2.VideoCapture(args.image if args.image else 0)
    urllib.request.urlretrieve(pic_link, "pic")
    video = cv2.VideoCapture("pic")
    padding=20
    while cv2.waitKey(1)<0:
        hasFrame,frame=video.read()
        if not hasFrame:
            cv2.waitKey()
            break
    
        resultImg,faceBoxes=highlightFace(frame)
        if not faceBoxes:
            print("No face detected")
    
        for faceBox in faceBoxes:
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
    
            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
            cv2.imshow("Detecting age and gender", resultImg)

#initialize ML var
faceHaar="/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/haarcascade_frontalface_default.xml"
ageProto="/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/age_deploy.prototxt"
ageModel="/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/age_net.caffemodel"
genderProto="/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/gender_deploy.prototxt"
genderModel="/home/poom/Desktop/airbnb/cultural distance/ML/age_gender_detection/gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

facecascade = cv2.CascadeClassifier(faceHaar)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

#testing the accuracy of the scrapes
for i in range(len(data)):
    j = random.randint(0, len(data)-1)
#    j = i
    print("=============================================================================")
    print("reviewer id: "+str(data.iloc[j,data.columns.get_loc("reviewer_id")]))
    print("country: "+str(data.iloc[j,data.columns.get_loc("country")]))
    try:
        analyze_pic(data.iloc[j,data.columns.get_loc("pic")])
    except Exception as e:
        print(e)
        continue