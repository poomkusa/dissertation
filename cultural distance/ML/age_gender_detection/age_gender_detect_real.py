#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:41:12 2020

@author: poom
"""

import cv2
from mtcnn.mtcnn import MTCNN
import urllib.request
from urllib.error import HTTPError
import pandas as pd
import numpy as np
import progressbar
data = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data.pkl")
#data = data.iloc[0:99]

# =============================================================================
# MTCNN parameters

# Haar Cascades parameters
#https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/
#https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
# =============================================================================

def detect_face_mtcnn(frame):
    imgtest1 = frame.copy()
    # convert to RGB, because OpenCV uses BGR -> mtcnn uses RGB
    imgplot = cv2.cvtColor(imgtest1, cv2.COLOR_BGR2RGB)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    resultList = detector.detect_faces(imgplot)
    
    faceBoxes=[]
    points=[]
    noseList=[]
    confidenceList=[]
    # plot each box
    for face in resultList:
        # draw the box
        x, y, width, height = face['box']
        x1=x
        y1=y
        x2=x+width
        y2=y+height
        faceBoxes.append([x1,y1,x2,y2])
        points.append(face['keypoints'])
        noseList.append(face['keypoints']['nose'])
        confidenceList.append(face['confidence'])
    return faceBoxes, points, noseList, confidenceList
    
def analyze_pic():
    frame = cv2.imread('pic') #import pic from the local folder
    #get box coordination locating faces
    faceBoxes, points, noseList, confidenceList = detect_face_mtcnn(frame)

    gender_ret = []
    age_ret = [] 
    agePreds=np.nan
    genderPreds=np.nan
    #predict only when theres only one face in the pic
    if (len(faceBoxes)==1):
        for faceBox, nose in zip(faceBoxes, noseList):
            #crop only the face part
            half_size = int( ( (faceBox[3]-faceBox[1])*1.2 )/2 )
            face=frame[max(0,nose[1]-half_size):
                       min(nose[1]+half_size,frame.shape[0]-1),max(0,nose[0]-half_size)
                       :min(nose[0]+half_size, frame.shape[1]-1)]
    
            #preprocessing
            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            
            genderNet.setInput(blob)
            genderPreds=genderNet.forward()
            gender=genderList[genderPreds[0].argmax()]
            gender_ret.append(gender)
    
            ageNet.setInput(blob)
            agePreds=ageNet.forward()
            age=ageList[agePreds[0].argmax()]
            age_ret.append(age)
    return len(faceBoxes), age_ret, gender_ret, agePreds, genderPreds, faceBoxes, points

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

data["face_num"] = np.nan
data["age"] = np.nan
data["gender"] = np.nan
data["age_conf"] = ""
data["gender_conf"] = ""
data["face"] = ""
data["points"] = ""
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