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
data = data[['listing_id', 'id', 'pic']]
#data = data.iloc[0:99]

# =============================================================================
# MTCNN parameters

# Haar Cascades parameters
#https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/
#https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
# =============================================================================

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

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
    if(len(resultList)!=1):
        return len(resultList), faceBoxes, points
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
    return len(resultList), faceBoxes, points
    
def analyze_pic(url):
    frame = url_to_image(url) #import pic from the local folder
    #get box coordination locating faces
    face_num, faceBoxes, points = detect_face_mtcnn(frame)

    gender_ret = []
    age_ret = [] 
    genderPreds=np.nan
    agePreds=np.nan
    #predict only when theres only one face in the pic
    if (face_num==1):
        #crop only the face part
        for faceBox in faceBoxes:
            face = frame[max(0,faceBox[1]-padding):min(faceBox[3]+padding,frame.shape[0]-1),
                         max(0,faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]
            
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
    return frame, face_num, age_ret, gender_ret, agePreds, genderPreds, faceBoxes, points

#initialize ML var
ageProto="/home/poom/Desktop//age_deploy.prototxt"
ageModel="/home/poom/Desktop/age_net.caffemodel"
genderProto="/home/poom/Desktop/gender_deploy.prototxt"
genderModel="/home/poom/Desktop/gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

data["image"] = ""
data["face_num"] = np.nan
data["age"] = np.nan
data["gender"] = np.nan
data["age_conf"] = ""
data["gender_conf"] = ""
data["face"] = ""
data["points"] = ""
padding=20
with progressbar.ProgressBar(max_value=len(data)) as bar:
    for i in range(len(data)):
        bar.update(i)
        try:
            #skip if the user profile page no longer exists
            if(str(data.iloc[i,data.columns.get_loc("pic")])=="nan"):
                continue
            #skip if there's no profile pic
            if(data.pic[i]=="https://a0.muscache.com/defaults/user_pic-225x225.png?v=3"):
                continue
            image, face_ret, age_ret, gender_ret, agePreds, genderPreds, faceBoxes, points = analyze_pic(data.pic[i])
            data.at[i, 'image'] = image
            data.loc[i, 'face_num'] = face_ret
            if face_ret == 1:
                data.loc[i, 'age'] = age_ret[0]
                data.loc[i, 'gender'] = gender_ret[0]
                data.at[i, 'age_conf'] = agePreds[0]
                data.at[i, 'gender_conf'] = genderPreds[0]
                data.at[i, 'face'] = faceBoxes[0]
                data.at[i, 'points'] = points
        #user profile page exists, but theres no profile picture
        except HTTPError:
            continue
        except Exception as e:
            import pdb, traceback, sys
            # extype, value, tb = sys.exc_info()
            # traceback.print_exc()
            # pdb.post_mortem(tb)
            print("")
            print("index: "+str(i))
            print(str(e))
            print("=============================================================================")
# ==================================================================================================================
        if(i%100==0 | i==len(data)-1):
            data.to_pickle("/home/poom/Desktop/dummy.pkl")