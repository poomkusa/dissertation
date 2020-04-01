#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:00:11 2020

@author: poom
"""

# =============================================================================
# https://github.com/fedelopez77/langdetect
# https://github.com/saffsd/langid.py
# =============================================================================

import pandas as pd
import langid
import pycld2 as cld2
import progressbar

df = pd.read_pickle("/home/poom/Desktop/sentiment_old.pkl")
#df.to_pickle("/home/poom/Desktop/sentiment.pkl")
df.comments.describe()
df.index[df['comments'].isnull() == True]
df.index[df['comments'] == ""]

df["langid"] = None
with progressbar.ProgressBar(max_value=len(df)) as bar:
    for i in range(len(df)):
        bar.update(i)
        if type(df.comments[i])==str:
            df.langid[i] = langid.classify(df.comments[i])[0]
        
#test
