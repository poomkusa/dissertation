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
indexNames = data[ (data['cult_dst_4'].isnull()) & (data['cult_dst_4'].isnull()) ].index
data.drop(indexNames , inplace=True)
data.isna().any()
# data.to_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/w_age_20200402.pkl")
            
# =============================================================================
# combine listing level and review level data
# =============================================================================
# import listing level data
import feather
# feather.write_dataframe(df, "path/to/file")
df = feather.read_dataframe("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/listing_clean.feather")
# check datatype of all columns
for (columnName, columnData) in df.iteritems():
    print('Colunm Name : ', columnName, 'Type: ', type(columnData.values[0]))

##review level merge
data=data.rename(columns = {'id':'review_id'})
reg_dta = pd.merge(left=data, right=df, left_on='listing_id', right_on='id')
# found duplicate reviews, they are the same house but have different listing id
# temp.to_pickle("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/data_final.pkl")

#listing level merge
temp = data[['listing_id', 'cult_dst_4', 'cult_dst_6']]
temp = temp.groupby('listing_id', as_index=False).mean()
reg_dta = pd.merge(left=df, right=temp, left_on='id', right_on='listing_id')

# =============================================================================
# regression
# ============================================================================= 
import statsmodels.formula.api as sm
reg = sm.ols("logit_perf ~ host_is_superhost + cult_dst_6 + host_is_superhost*cult_dst_6+ host_listings_count \
             + number_of_reviews + price + bathrooms + bedrooms + review_scores_location", 
             data=reg_dta, missing='drop').fit()
result = reg.summary()
result

