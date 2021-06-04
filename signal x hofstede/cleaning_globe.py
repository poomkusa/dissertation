# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 05:18:38 2021

@author: ThisPC
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 21:59:26 2021

@author: ThisPC
"""

import numpy as np
import pandas as pd
import feather

data = pd.read_pickle("D:/PhD/Dissertation/airbnb/cultural distance/data_mini.pkl")
#data = pd.read_pickle("/home/poom/Desktop/phd/Dissertation/airbnb/cultural distance/data_mini.pkl")
data = data[['listing_id', 'id', 'date', 'reviewer_id', 'country', 'globe1_dst', 'globe2_dst']].copy()
# data = data[['listing_id', 'id', 'date', 'reviewer_id', 'country', 'power_distance', 'individualism', 'masculinity', 'uncertainty_avoidance', 'LT_orientation', 'indulgence']].copy()
data['id_date'] = data['listing_id'].apply(str) + "-" + data['date'].str[0:4] + data['date'].str[5:7]
data['yyyymm'] = data['date'].str[0:4] + data['date'].str[5:7]
data = data.rename(columns = {'id':'review_id'})
#check for missing data in data
data.isna().sum()
data = data.dropna()

temp = feather.read_dataframe("D:/PhD/Dissertation/airbnb/cultural distance/review_long_final.feather")
data = data[data.review_id.isin(temp.review_id.tolist())]

df = feather.read_dataframe("D:/PhD/Dissertation/airbnb/cultural distance/listing_long_clean.feather")
#df = feather.read_dataframe("/home/poom/Desktop/phd/Dissertation/airbnb/cultural distance/listing_long_clean.feather")
df = df[['id', 'date', 'availability_30', 'host_is_superhost', 'host_listings_count', 'number_of_reviews', 'price', 'id_date', 'bathrooms', 'bedrooms', 'review_scores_location']]
df.date.unique()
df = df[df.date == "201909.csv"]
# df = df[df.date != "201507.csv"]
# df = df[df.date != "201705.csv"]
# df = df[df.date != "201804.csv"]
# df = df[df.date != "201805.csv"]
# df = df[df.date != "201806.csv"]
# df = df[df.date != "201807.csv"]
# df = df[df.date != "201808.csv"]
# df = df[df.date != "201809.csv"]
# df['yyyymm'] = df['date'].str[0:6]
df.isna().sum()
df = df[df['host_listings_count'].notna()]
df = df[df['bedrooms'].notna()]
df = df[df['bathrooms'].notna()]
df = df[df.host_is_superhost != ""]
df['host_is_superhost'] = np.where(df['host_is_superhost']=="t", 1, 0)
# data[data.listing_id.isin(df.id.tolist())]
# reg_dta = pd.merge(left=data, right=df, left_on='id_date', right_on='id_date', how='left')
# reg_dta.isna().sum()
len(data.listing_id.unique())
len(df.id.unique())
df = df[df.id.isin(data.listing_id.unique())]
df.isna().sum()

df = df.reset_index()
df['gid'] = df.index
# temp = df[['gid', 'id_date', 'host_is_superhost']].copy()
# data = pd.merge(left=data, right=temp, left_on='id_date', right_on='id_date', how='left')
temp = df[['gid', 'id', 'host_is_superhost']].copy()
data = pd.merge(left=data, right=temp, left_on='listing_id', right_on='id', how='left')
data.isna().sum()
data = data.dropna()
#data['interaction'] = data['host_is_superhost'] * data['cult_dst_6']
feather.write_dataframe(df, "C:/Users/ThisPC/Desktop/zdata.feather")
feather.write_dataframe(data, "C:/Users/ThisPC/Desktop/xdata.feather")

##convert to R file for colab
#library(feather)
#x <- read_feather("D:/PhD/Dissertation/airbnb/signal x hofstede/lvmlm/us vs asia/201804 onward/xdata.feather")
#save(x, file = 'D:/PhD/Dissertation/airbnb/signal x hofstede/lvmlm/us vs asia/201804 onward/xdata.RData')
#z <- read_feather("D:/PhD/Dissertation/airbnb/signal x hofstede/lvmlm/us vs asia/201804 onward/zdata.feather")
#save(z, file = 'D:/PhD/Dissertation/airbnb/signal x hofstede/lvmlm/us vs asia/201804 onward/zdata.RData')