#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:00:11 2020

@author: poom
"""

import pandas as pd
from textblob import TextBlob
#from textblob.sentiments import NaiveBayesAnalyzer
from googletrans import Translator
import progressbar
import random

df = pd.read_csv (r'/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/venice_reviews.csv')
df.comments.describe()
df.index[df['comments'].isnull() == True]

#create dataset for testing
#df = df.iloc[0:10]
#df = pd.read_pickle("/home/poom/Desktop/sentiment_old.pkl")
#x = df.iloc[df.index[df['language'] == "ja"]].head()
#y = df.iloc[df.index[df['language'] == "de"]].head()
#z = df.iloc[df.index[df['language'] == "fr"]].head()
#df=pd.concat([df.head(), x, y, z], ignore_index=True)

df["missing_comment"] = None
df["lang"] = None
df["translation"] = None
df["polar"] = None
df["subject"] = None

#dont need 4 lines below if it can translate NaN
df.index[df['comments'].isnull() == True]
df.index[df['comments'] == " "]
df.loc[df['comments'].isnull() == True, 'missing_comment'] = True
df.loc[df['comments'].isnull() == True, 'comments'] = "nan"
translations = Translator().translate(df['comments'].tolist())
with progressbar.ProgressBar(max_value=len(df)) as bar:
    for i in range(len(df)):
        df.lang[i] = translations[i].src
        df.translation[i] = translations[i].text
        temp = TextBlob(df.translation[i]).sentiment
        df.polar[i] = temp.polarity
        df.subject[i] = temp.subjectivity
        bar.update(i)
        
#df.to_pickle("/home/poom/Desktop/airbnb/cultural distance/ML/sentiment.pkl")
#df = pd.read_pickle("/home/poom/Desktop/airbnb/cultural distance/ML/sentiment.pkl")
#test
df.language.unique()
df.iloc[df.index[df['language'] == "ja"]]
j = random.randint(0, len(df)-1)
print("review: "+df.comments[j])
print("translation: "+df.translation[j])
print("polarity: "+str(df.polarity[j]))
print("subjectivity: "+str(df.subjectivity[j]))