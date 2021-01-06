#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:16:26 2020

@author: poom
"""

import numpy as np
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# =============================================================================
# combine scrape data with nlp data
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

# clean data
#data = pd.read_pickle("/home/poom/Desktop/20200402.pkl")
#check the whole dataframe 
for (columnName, columnData) in data.iteritems():
    series_value = pd.Series(columnData.values)
    print('====================================================================')
    print('Colunm Name : ', columnName)
    print('Type: ', type(columnData.values[0]))
    print(series_value.describe())
    print('number of nan', series_value.isnull().sum())
#check specific column
col = 'country'
data[col].describe()
data[col].isnull().sum()
data.index[data[col].isnull()]
freq = data[col].value_counts(dropna=False)
#keep only rows with no nan
data = data[data[col].notna()]

#transform text in country column
#remove rows with work/language instead of country
data['country'].str.contains("Work: ").sum()
data = data[-data['country'].str.contains("Work: ")]
data['country'].str.contains("Speaks ").sum()
data = data[-data['country'].str.contains("Speaks ")]
#split off only the country name (word after last ','), trim off 'Lives in ', trim off 'The ' strip whitespace
data['country'] = data['country'].str.split(',').str[-1]
data['country'] = data['country'].str.replace('Lives in ', '')
data['country'] = data['country'].str.replace('The ', '')
data['country']  = data['country'].str.strip()
#consolidate us state to usa
states = pd.Series(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])
data['country'] = np.where(data['country'].str.lower().isin(states.str.lower()), 'United States', data['country'])
#USA-> United States
#Russian Federation->Russia
data['country'] = np.where(data['country']=="Russian Federation", 'Russia', data['country'])
#find countries with same name but diff capital letter
freq = data['country'].value_counts(dropna=False)
freq2 = data['country'].str.lower().value_counts(dropna=False)

#calculate cultural distance
#hofstede
data['cult_dst_4'] = np.nan
data['cult_dst_6'] = np.nan
def cult_dst (visitor, dim):
    visitor = hofstede.iloc[hofstede.index[hofstede['country']==visitor], 1:dim+1].values.flatten().tolist()
    sum = 0
    for i in range(dim):
        sum += pow((visitor[i]-host[i]), 2)/var[i]
    sum = sum/dim
    return sum
#retrieve a table of distance
hofstede = pd.read_csv('/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/hofstede.csv')
var = [450.4329004329, 574.634199134199, 361.29020979021, 528.674658674659, 587.190608802285, 491.695323937403]
host = hofstede.iloc[hofstede.index[hofstede['country']=='Italy'], 1:7].values.flatten().tolist()
data.reset_index(drop=True, inplace=True)
for i in range(len(data)):
    if hofstede.iloc[hofstede.index[hofstede['country']==data.country[i]], 7].values[0] == 0:
        data.cult_dst_4[i] = cult_dst (data.country[i], 4)
        data.cult_dst_6[i] = cult_dst (data.country[i], 6)
        continue
    if hofstede.iloc[hofstede.index[hofstede['country']==data.country[i]], 7].values[0] == 6:
        data.cult_dst_4[i] = cult_dst (data.country[i], 4)
        data.cult_dst_6[i] = cult_dst (data.country[i], 6)
        continue
    if hofstede.iloc[hofstede.index[hofstede['country']==data.country[i]], 7].values[0] == 4:
        data.cult_dst_4[i] = cult_dst (data.country[i], 4)
#remove rows with nan in both cult_dst columns
indexNames = data[ (data['cult_dst_4'].isnull()) & (data['cult_dst_6'].isnull()) ].index
data.drop(indexNames , inplace=True)
data.isna().any()
#schwartz
data['schwartz_dst'] = np.nan
hofstede = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/schwartz.csv')
hofstede['country'] = hofstede['country'].str.strip().str.lower()
var = [0.0908708228,	0.1639822152	, 0.1919787342,	0.0246385918	, 0.2763518354, 0.1520717563, 0.0716698576]
host = hofstede.iloc[hofstede.index[hofstede['country']=='italy'], 1:8].values.flatten().tolist()
data.reset_index(drop=True, inplace=True)
data['temp'] = np.where(data['country'].str.lower().isin(hofstede['country']), True, False)
for i in range(len(data)):
    if data.temp[i]:
        data.schwartz_dst[i] = cult_dst (data.country[i].lower(), 7)
#globe
data['globe1_dst'] = np.nan
hofstede = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/globe1.csv')
hofstede['country'] = hofstede['country'].str.strip().str.lower()
var = [0.360503278, 0.211280567, 0.203881333, 0.183653609, 0.21453894, 0.16442334, 0.584759576, 0.136189441, 0.139187594]
host = hofstede.iloc[hofstede.index[hofstede['country']=='italy'], 1:10].values.flatten().tolist()
data.reset_index(drop=True, inplace=True)
data['temp'] = np.where(data['country'].str.lower().isin(hofstede['country']), True, False)
for i in range(len(data)):
    if data.temp[i]:
        data.globe1_dst[i] = cult_dst (data.country[i].lower(), 9)
data['globe2_dst'] = np.nan
hofstede = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/globe2.csv')
hofstede['country'] = hofstede['country'].str.strip().str.lower()
var = [0.375933771, 0.265198149, 0.161550916, 0.248150664, 0.129028394, 0.318575258, 0.164253454, 0.236447185, 0.412399143]
host = hofstede.iloc[hofstede.index[hofstede['country']=='italy'], 1:10].values.flatten().tolist()
data.reset_index(drop=True, inplace=True)
data['temp'] = np.where(data['country'].str.lower().isin(hofstede['country']), True, False)
for i in range(len(data)):
    if data.temp[i]:
        data.globe2_dst[i] = cult_dst (data.country[i].lower(), 9)
#wvs
wvs = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/wvs.csv')
wvs['country'] = wvs['country'].str.strip().str.lower()
sse_h = 0.815306558740057
tsr_h = 0.382565436
wvs['wvs_dst'] = np.sqrt( np.square(wvs['sse']-sse_h) + np.square(wvs['tsr']-tsr_h) )
wvs = wvs[['country','wvs_dst']]
wvs=wvs.rename(columns = {'country':'key'})
data['key'] = data['country'].str.lower()
data = pd.merge(left=data, right=wvs, left_on='key', right_on='key', how='left')
#mahalanobis distance
#6 dim
def mahalanobis(x=None, data=None, cov=None):
    x_mu = x - hofstede.iloc[hofstede.index[hofstede['country']=='Italy'], 1:7].values.flatten().tolist()
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()
hofstede = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/hofstede.csv')
hofstede = hofstede[hofstede.columns[range(7)]]
hofstede = hofstede.dropna()
hofstede = hofstede.reset_index(drop=True)
hofstede['mahalanobis'] = mahalanobis(x=hofstede[hofstede.columns[-6:]], data=hofstede[hofstede.columns[-6:]],)
hofstede = hofstede[['country','mahalanobis']]
hofstede = hofstede.rename(columns = {'country':'key'})
data = pd.merge(left=data, right=hofstede, left_on='country', right_on='key', how='left')
del data['key']
#4 dim
def mahalanobis(x=None, data=None, cov=None):
    x_mu = x - hofstede.iloc[hofstede.index[hofstede['country']=='Italy'], 1:5].values.flatten().tolist()
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()
hofstede = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/hofstede.csv')
hofstede = hofstede[hofstede.columns[range(5)]]
hofstede = hofstede.dropna()
hofstede = hofstede.reset_index(drop=True)
hofstede['mahalanobis2'] = mahalanobis(x=hofstede[hofstede.columns[-4:]], data=hofstede[hofstede.columns[-4:]],)
hofstede = hofstede[['country','mahalanobis2']]
hofstede = hofstede.rename(columns = {'country':'key'})
data = pd.merge(left=data, right=hofstede, left_on='country', right_on='key', how='left')
del data['key']


#calculate great-circle distance
from geopy.distance import great_circle
#create a table of lat/long for each country
latlong = pd.read_csv("/home/poom/Desktop/phd/Dissertation/airbnb/cultural distance/latlong.csv")
latlong['gc_dst'] = np.nan
italy = (latlong.loc[latlong['country']=='Italy', 'lat'].iloc[0], latlong.loc[latlong['country']=='Italy', 'long'].iloc[0])
for i in range(len(latlong)):
    latlong.loc[i,'gc_dst'] = great_circle(italy, (latlong.lat[i],latlong.long[i])).km
data = data.merge(latlong, on='country', how='left')
# data.to_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data.pkl")
 
# =============================================================================
# NLP
# =============================================================================
from textblob import TextBlob
#from textblob.sentiments import NaiveBayesAnalyzer
import progressbar
import random
from time import sleep
data = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data.pkl")
data.isna().any()

#remove rows with unwanted comments
data['comments'].isnull().sum()
mask = data['comments'].str.len()==1
freq = data.loc[mask]
freq = freq['comments'].value_counts(dropna=False)
indexNames = data[ (data['comments'].str.len()==1) | (data['comments']=='...') | (data['comments']=='..') | (data['comments']=='. ') | (data['comments']=='N/a') | (data['comments']=='*****') ].index
data.drop(indexNames , inplace=True)

#language detection ensemble
data.reset_index(inplace=True, drop=True )
data['langEnsemble'] = np.nan
data['langdetect'] = np.where(data['langdetect'].str.contains('zh', na=False), 'zh', data['langdetect'])
data['cld2'] = np.where(data['cld2'].str.contains('zh', na=False), 'zh', data['cld2'])
for i in range(len(data)):
    if data.langdetect[i] == data.langid[i]:
        data.langEnsemble[i] = data.langdetect[i]
    elif data.langdetect[i] == data.cld2[i]:
        data.langEnsemble[i] = data.langdetect[i]
    elif data.langid[i] == data.cld2[i]:
        data.langEnsemble[i] = data.langid[i]
mask = data['comments'].str.len()==1
freq = data['langEnsemble'].value_counts(dropna=False)
mask = data['langEnsemble'].isnull()
freq2 = data.loc[mask]
indexNames = data[ (data['langEnsemble'].isnull()) ].index
data.drop(indexNames , inplace=True)

#translate
data.reset_index(inplace=True, drop=True )
from google.cloud import translate_v2 as translate
import argparse
import six
translate_client = translate.Client()
mask = data['langEnsemble'] != 'en'
foreign = data.loc[mask]
foreign['char_count'] = foreign['comments'].str.len()
sum(foreign['char_count'])
data['translation'] = np.nan
with progressbar.ProgressBar(max_value=len(data)) as bar:
    for i in range(344208, len(data)):
        bar.update(i)
        if data.langEnsemble[i] != 'en':
#            #using textblob
#            blob = TextBlob(data.comments[i])
#            data.translation[i] = blob.translate(to='en').string
            text = data.comments[i]
            if isinstance(text, six.binary_type):
                text = text.decode('utf-8')
            result = translate_client.translate(text, target_language='en')
            data.translation[i] = result['translatedText']
            sleep(0.2) 
            print(data.translation[i])
        if i%1000==0:
            data.to_pickle("/home/poom/Desktop/data_nlp.pkl")
sum(~(data['langEnsemble']=='en') & data['translation'].isnull())
data['translation'] = np.where(data['translation'].isnull(), data['comments'], data['translation'])

#sentiment analysis
data['sentiment_pl'] = np.nan
data['sentiment_sj'] = np.nan
with progressbar.ProgressBar(max_value=len(data)) as bar:
    for i in range(14000, len(data)):
        bar.update(i)
        if data.langEnsemble[i] != 'en':
            blob = TextBlob(data.translation[i])
            data.sentiment_pl[i] = blob.sentiment.polarity
            data.sentiment_sj[i] = blob.sentiment.subjectivity
        if i%1000==0:
            data.to_pickle("/home/poom/Desktop/data_nlp.pkl")
data['sentiment_pl'] = np.where(data['sentiment_pl'].isnull(), data['polarity'], data['sentiment_pl'])
data['sentiment_sj'] = np.where(data['sentiment_sj'].isnull(), data['subjectivity'], data['sentiment_sj'])
del data['polarity']
del data['subjectivity']

# data.to_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data_nlp.pkl")

#combine data with nlp
data = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data.pkl")
nlp = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data_nlp.pkl")
data['unique'] = data['listing_id'].astype(str) + "-" + data['id'].astype(str)
nlp['unique'] = nlp['listing_id'].astype(str) + "-" + nlp['id'].astype(str)
freq1 = data['unique'].value_counts(dropna=False)
freq2 = nlp['unique'].value_counts(dropna=False)
len(set(data['unique'])-set(nlp['unique']))
del data['polarity']
del data['subjectivity']
nlp = nlp[['langEnsemble','translation','sentiment_pl','sentiment_sj','unique']]
data = data.merge(nlp, on='unique', how='left')
temp = data.loc[data['sentiment_pl'].isnull(),]
# data.to_pickle("/home/poom/Desktop/data.pkl")

# =============================================================================
# ML
# =============================================================================
#separate data to batch run in colab
data = pd.read_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data.pkl")
    
d1 = data[0:50000][['listing_id', 'id', 'pic']]
d2 = data[50000:100000][['listing_id', 'id', 'pic']]
d3 = data[100000:150000][['listing_id', 'id', 'pic']]
d4 = data[150000:200000][['listing_id', 'id', 'pic']]
d5 = data[200000:250000][['listing_id', 'id', 'pic']]
d6 = data[250000:300000][['listing_id', 'id', 'pic']]
d7 = data[300000:350000][['listing_id', 'id', 'pic']]
d8 = data[350000:400000][['listing_id', 'id', 'pic']]
d9 = data[400000:450000][['listing_id', 'id', 'pic']]
d10 = data[450000:len(data)][['listing_id', 'id', 'pic']]

d1.reset_index(inplace=True)
d2.reset_index(inplace=True)
d3.reset_index(inplace=True)
d4.reset_index(inplace=True)
d5.reset_index(inplace=True)
d6.reset_index(inplace=True)
d7.reset_index(inplace=True)
d8.reset_index(inplace=True)
d9.reset_index(inplace=True)
d10.reset_index(inplace=True)

d1.to_pickle("/home/poom/Desktop/d1.pkl")
d2.to_pickle("/home/poom/Desktop/d2.pkl")
d3.to_pickle("/home/poom/Desktop/d3.pkl")
d4.to_pickle("/home/poom/Desktop/d4.pkl")
d5.to_pickle("/home/poom/Desktop/d5.pkl")
d6.to_pickle("/home/poom/Desktop/d6.pkl")
d7.to_pickle("/home/poom/Desktop/d7.pkl")
d8.to_pickle("/home/poom/Desktop/d8.pkl")
d9.to_pickle("/home/poom/Desktop/d9.pkl")
d10.to_pickle("/home/poom/Desktop/d10.pkl")

#combine the data
d1 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d1.pkl")
d2 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d2.pkl")
d3 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d3.pkl")
d4 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d4.pkl")
d5 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d5.pkl")
d6 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d6.pkl")
d7 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d7.pkl")
d8 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d8.pkl")
d9 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d9.pkl")
d10 = pd.read_pickle("C:/Users/ThisPC/Desktop/result_d10.pkl")
df = pd.concat([d1, d2, d3, d4, d5, d6, d7, d8, d9, d10])
df = df.set_index('index')
data['id'].equals(df['id'])
df = df[['face_num','age','gender','age_conf','gender_conf','face','points']]
data = pd.concat([data, df], axis=1)

# =============================================================================
# final cleaning
# =============================================================================
data=data[['listing_id','id','date','reviewer_id','reviewer_name','country','cult_dst_4','cult_dst_6','gc_dst','comments','translation','sentiment_pl','sentiment_sj','bayes_class','bayes_prob','pic','age','gender']]
#transform age
data['age'] = np.where(data['age']=='(0-2)', 1, data['age'])
data['age'] = np.where(data['age']=='(4-6)', 5, data['age'])
data['age'] = np.where(data['age']=='(8-12)', 10, data['age'])
data['age'] = np.where(data['age']=='(15-20)', 17.5, data['age'])
data['age'] = np.where(data['age']=='(25-32)', 28.5, data['age'])
data['age'] = np.where(data['age']=='(38-43)', 40.5, data['age'])
data['age'] = np.where(data['age']=='(48-53)', 50.5, data['age'])
data['age'] = np.where(data['age']=='(60-100)', 80, data['age'])
#remove duplicate id
data.drop_duplicates(subset='id', keep="first", inplace=True)
#convert auto generated review to n/a
freq = data['translation'].value_counts(dropna=False)
data['sentiment_pl'] = np.where(data['translation'].str.contains('This is an automated posting.', na=False), np.nan, data['sentiment_pl'])
data['bayes_class'] = np.where(data['translation'].str.contains('This is an automated posting.', na=False), np.nan, data['bayes_class'])

data.reset_index(inplace=True, drop=True )
data.to_pickle("C:/Users/ThisPC/Desktop/data_mini.pkl")

#add each cultural dimensions
data = pd.read_pickle("D:/PhD/Dissertation/airbnb/cultural distance/data_mini.pkl")
hofstede = pd.read_csv('D:/PhD/Dissertation/airbnb/cultural distance/hofstede.csv')
del hofstede['dim_num']
data = data.merge(hofstede, on='country', how='left')
data.to_pickle("C:/Users/ThisPC/Desktop/data_mini.pkl")

# #remove 25-32 age class
# indexNames = data[(data['age']==28.5)].index
# data.drop(indexNames , inplace=True)

#add VADER sentiment
data = pd.read_pickle("D:/PhD/Dissertation/airbnb/cultural distance/data_mini.pkl")
data['unique'] = data['listing_id'].astype(str) + "-" + data['id'].astype(str)
temp = data[['unique','translation']].copy()
indexNames = temp[ (temp['translation'].isnull()) ].index
temp.drop(indexNames , inplace=True)
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
temp['compound'] = temp['translation'].apply(lambda x: sia.polarity_scores(x)['compound'])
data = pd.merge(left=data, right=temp[['unique','compound']], left_on='unique', right_on='unique', how='left')
data['compound'] = np.where(data['translation'].str.contains('This is an automated posting.', na=False), np.nan, data['compound'])
data.to_pickle("C:/Users/ThisPC/Desktop/data_mini.pkl")

# =============================================================================
# combine listing level and review level data
# =============================================================================
# import listing level data
import feather
# feather.write_dataframe(df, "path/to/file")
df = feather.read_dataframe("C:/Users/ThisPC/Desktop/listing_clean.feather")
# check datatype of all columns
for (columnName, columnData) in df.iteritems():
    print('Colunm Name : ', columnName, 'Type: ', type(columnData.values[0]))

##review level merge
df = feather.read_dataframe("C:/Users/ThisPC/Desktop/listing_long_clean.feather")
df = df[['id_date','review_scores_rating','review_scores_accuracy','review_scores_value','number_of_reviews','price']]
data['id_date'] = data['listing_id'].apply(str) + "-" + data['date'].str[0:4] + data['date'].str[5:7]
data=data.rename(columns = {'id':'review_id'})
reg_dta = pd.merge(left=data, right=df, left_on='id_date', right_on='id_date', how='left')
del reg_dta['bayes_prob']
# found duplicate reviews, they are the same house but have different listing id
# some reviews are automated message when host cancel the booking
# temp.to_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data_final.pkl")

#listing level merge
temp = data[['listing_id','cult_dst_4','cult_dst_6','schwartz_dst','globe1_dst','globe2_dst','wvs_dst',
             'power_distance','individualism','masculinity','uncertainty_avoidance','LT_orientation',
             'indulgence','gc_dst','sentiment_pl','sentiment_sj','age']].copy()
temp['age'] = pd.to_numeric(temp['age'])
temp = temp.groupby('listing_id', as_index=False).mean()
#use only first 7 reviews
temp2 = data[['listing_id','sentiment_pl','sentiment_sj']]
freq = temp2['listing_id'].value_counts(dropna=False)
temp2 = temp2.groupby('listing_id').head(7)
temp2 = temp2.groupby('listing_id', as_index=False).mean()
temp2 = temp2[['sentiment_pl','sentiment_sj']]
temp2.columns = ['sentiment_pl_7', 'sentiment_sj_7']
temp = pd.concat([temp, temp2], axis=1)
reg_dta = pd.merge(left=df, right=temp, left_on='id', right_on='listing_id')

feather.write_dataframe(reg_dta, "/home/poom/Desktop/review.feather")
feather.write_dataframe(reg_dta, "C:/Users/ThisPC/Desktop/listing.feather")

# =============================================================================
# regression
# ============================================================================= 
import statsmodels.formula.api as sm
reg_dta['super_x_dst'] = reg_dta['host_is_superhost']*reg_dta['cult_dst_6']
reg = sm.ols("logit_perf ~ host_is_superhost + host_is_superhost:cult_dst_6 \
             + host_listings_count + number_of_reviews + price + bathrooms + bedrooms + review_scores_location", 
             data=reg_dta, missing='drop').fit()
result = reg.summary()
result

# =============================================================================
# make 2 datasets match
# ============================================================================= 
df1= feather.read_dataframe("C:/Users/ThisPC/Desktop/review_long.feather")
df2= feather.read_dataframe("C:/Users/ThisPC/Desktop/listing.feather")
#select used variables then drop all rows with na
df1 = df1[['listing_id', 'power_distance', 'individualism', 'masculinity', 'uncertainty_avoidance',
           'LT_orientation', 'indulgence', 'compound', 'review_scores_accuracy']]
df1.isna().sum()
df1 = df1.dropna()
df2 = df2[['id', 'host_is_superhost', 'host_listings_count', 'number_of_reviews', 'price', 'bathrooms',
           'bedrooms', 'review_scores_location', 'logit_perf', 'globe1_dst', 'age']]
df2.isna().sum()
df2 = df2.dropna()
#remove rows in review data with neutral sentiment
df1 = df1[(df1['compound']>=0.05) | (df1['compound']<=-0.05)]
#export to csv and check in excel
freq1 = df1['listing_id'].value_counts(dropna=False)
freq2 = df2['id'].value_counts(dropna=False)
freq1.to_csv(r'C:/Users/ThisPC/Desktop/temp.csv')
freq2.to_csv(r'C:/Users/ThisPC/Desktop/temp2.csv')
#check and remove in python
(~df2['id'].isin(df1['listing_id'])).sum()
df2 = df2[df2['id'].isin(df1['listing_id'])]
(~df1['listing_id'].isin(df2['id'])).sum()
df1 = df1[df1['listing_id'].isin(df2['id'])]





