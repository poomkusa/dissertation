#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:16:26 2020

@author: poom
"""

import pandas as pd

# =============================================================================
# combine data
# =============================================================================

# combine langdetect, langid with cld2
data = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/ML/nlp/sentiment.pkl")
cld2 = pd.read_csv("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/ML/nlp/cld2.csv")
# compare comments column of two dataframes
cld2['compare'] = data['comments']
cld2['comments'].equals(cld2['compare'])
cld2['RowEqual'] = cld2['comments'] == cld2['comments']
cld2.index[cld2['RowEqual']==False]
# show rows that are not same
x = cld2.loc[cld2.index[cld2['RowEqual']==False], ['comments','compare']]
# if no problem, add language detected from cld2 to main data
data['cld2'] = cld2['cld2']

# combine nlp data with scraping data
scrape = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/scraping/user_data.pkl")
# compare reviewer_id column of two dataframes
scrape['compare'] = data['reviewer_id']
scrape['reviewer_id'].equals(scrape['compare'])
scrape['RowEqual'] = scrape['reviewer_id'] == scrape['compare']
scrape.index[scrape['RowEqual']==False]
# show rows that are not same
x = scrape.loc[scrape.index[scrape['RowEqual']==False], ['reviewer_id','compare']]
# if no problem, combine them ignoring identical column
# remove identical column
scrape = scrape.drop(['reviewer_id', 'face_num', 'gender', 'age', 'compare', 'RowNotEqual'], axis=1)
data = data.drop(['polaritySubjectivity'], axis=1)
data = pd.concat([data, scrape], axis=1)
#data.to_pickle("/home/poom/Desktop/20200402.pkl")

# =============================================================================
# clean data
# =============================================================================
# found duplicate reviews, they are the same house but have different listing id

# check data
data.comments.describe()
x = data['comments'].value_counts(dropna=False)