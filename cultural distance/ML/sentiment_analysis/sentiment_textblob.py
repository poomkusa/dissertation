#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:00:11 2020

@author: poom
"""

# =============================================================================
# https://github.com/sloria/TextBlob
# https://github.com/thisandagain/sentiment
# https://pypi.org/project/cld2-cffi/
# =============================================================================

import pandas as pd
from textblob import TextBlob
#from textblob.sentiments import NaiveBayesAnalyzer
import progressbar
import random

df = pd.read_csv (r'/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/venice_reviews.csv')
df.comments.describe()
df.index[df['comments'].isnull() == True]

#create dataset for testing
#df = df.iloc[0:10]
#df = pd.read_pickle("/home/poom/Desktop/airbnb/cultural distance/ML/sentiment_analysis/sentiment_old.pkl")
#x = df.iloc[df.index[df['language'] == "ja"]].head()
#y = df.iloc[df.index[df['language'] == "de"]].head()
#z = df.iloc[df.index[df['language'] == "fr"]].head()
#df=pd.concat([df.head(), x, y, z], ignore_index=True)

df["lang"] = None
df["translation"] = None
df["polar"] = None
df["subject"] = None

#analyze sentiment
with progressbar.ProgressBar(max_value=len(df)) as bar:
    for index, row in df.iterrows():
        bar.update(index)
        try:
            df.loc[index, 'lang'] = TextBlob(row.comments).detect_language()
            if(df.loc[index, 'lang']=='en'):
                temp = TextBlob(row.comments).sentiment
                #The polarity score is a float within the range [-1.0, 1.0]. 
                #The subjectivity is a float within the range [0.0, 1.0] 
                #where 0.0 is very objective and 1.0 is very subjective.
                df.loc[index, 'polar'] = temp.polarity
                df.loc[index, 'subject'] = temp.subjectivity
            else:
                translation = TextBlob(row.comments).translate(to='en')
                temp = translation.sentiment
                df.loc[index, 'translation'] = translation.string
                df.loc[index, 'polar'] = temp.polarity
                df.loc[index, 'subject'] = temp.subjectivity
        except Exception as e:
            #if e==429 then change ip
# =============================================================================
#             store index, error message in a list
# =============================================================================
            print("================================index: "+str(index))
            print("---"+str(row.comments))
            print("---"+str(e))
        
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