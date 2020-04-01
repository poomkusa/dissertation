#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:41:12 2020

@author: poom
"""
# =============================================================================
# Haar Cascades + Levi and Hassner (2015)
# https://towardsdatascience.com/predict-age-and-gender-using-convolutional-neural-network-and-opencv-fd90390e3ce6
# https://www.learnopencv.com/age-gender-classification-using-opencv-deep-learning-c-python/
# https://data-flair.training/blogs/python-project-gender-age-detection/

# MTCNN
# https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/

# Rank-consistent Ordinal Regression for Neural Networks
# https://paperswithcode.com/paper/consistent-rank-logits-for-ordinal-regression#code

# race recognition
# https://github.com/HectorAnadon/Face-expression-and-ethnic-recognition
# =============================================================================

import cv2
import urllib.request
from urllib.error import HTTPError
import pandas as pd
from matplotlib import pyplot as plt
import progressbar
data = pd.read_pickle("/home/poom/Desktop/combine.pkl")
#data = data.iloc[0:99]

# =============================================================================
test_run = 0 #1=show result picture by picture, 0=run quietly for the whole list of pics
single_pic = 0 #if want a single run, save pic in the same folder as the code, file name has to be "pic"
# Haar Cascades parameters
#https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/
#https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php

# MTCNN parameters

# Levi and Hassner (2015) parameters

# =============================================================================

def highlightFace(frame):
    imgtest1 = frame.copy()
    imgtest = cv2.cvtColor(imgtest1, cv2.COLOR_BGR2GRAY) #convert to gray scale
    imgplot = cv2.cvtColor(imgtest1, cv2.COLOR_BGR2RGB) #create image for plotting, bc OpenCV uses BGR -> matplotlib uses RGB
    faceBoxes=[]
    faces = facecascade.detectMultiScale(imgtest, scaleFactor=1.2, minNeighbors=5)
    for (x, y, w, h) in faces:
        x1=x
        y1=y
        x2=x+w
        y2=y+h
        faceBoxes.append([x1,y1,x2,y2])
        cv2.rectangle(imgplot, (x1,y1), (x2,y2), (0,255,0), int(round(imgplot.shape[0]/150)), 8)
    return imgplot, faceBoxes
    
def analyze_pic():
    padding=20
    frame = cv2.imread('pic') #import pic from the local folder
    #get box coordination locating faces
    resultImg,faceBoxes=highlightFace(frame)

    gender_ret = []
    age_ret = [] 
    #if test run, predict all faces in the pic
    #if not test_run, predict only when theres only one face in the pic
    if (test_run==1 and len(faceBoxes)>0) or (test_run==0 and len(faceBoxes)==1):
        plt.figure(figsize=(8,8)) #set pic size
        for faceBox in faceBoxes:
            #crop only the face part
            face=frame[max(0,faceBox[1]-padding):
                       min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                       :min(faceBox[2]+padding, frame.shape[1]-1)]
    
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
            
            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
    if(test_run==1):
        plt.imshow(resultImg)    
        plt.show()
        if single_pic==0:
            input("Press Enter to continue...")
    plt.close() #if not close, plot will accumulate and fill the memory
    return len(faceBoxes), age_ret, gender_ret

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

data["face_num"] = None
data["age"] = None
data["gender"] = None
if single_pic==0:
    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for i in range(len(data)):
            bar.update(i)
            #skip if the user profile page no longer exists
            if(str(data.iloc[i,data.columns.get_loc("pic")])=="nan"):
                continue
            try:
                #save pic from the website into local folder
                pic = urllib.request.urlretrieve(data.iloc[i,data.columns.get_loc("pic")], "pic")
                face_ret, age_ret, gender_ret = analyze_pic()
                data.face_num[i] = face_ret
                data.age[i] = age_ret
                data.gender[i] = gender_ret
            #user profile page exists, but theres no profile picture
            except HTTPError:
#                print("")
#                print("profile pic not exist in web for index: "+str(i))
#                print("link: "+pic_link)
                continue
            except Exception as e:
                print("")
                print("index: "+str(i))
                print(str(e))
                print("=============================================================================")
                continue
            if(i%100==0 | i==516368):
                data.to_pickle("/home/poom/Desktop/dummy.pkl")
else:
    analyze_pic()