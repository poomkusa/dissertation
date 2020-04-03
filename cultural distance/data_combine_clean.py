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
data['country'] = np.where(data['country'].str.lower().isin(states.str.lower()), 'USA', data['country'])
#find countries with same name but diff capital letter
freq = data['country'].value_counts(dropna=False)
freq2 = data['country'].str.lower().value_counts(dropna=False)

#calculate cultural distance
data['cult_dst'] = np.nan
def cult_diff()
#retrieve a table of distance
hofstede = pd.read_csv('/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/hofstede.csv')




host = hofstede.iloc[hofstede.index[hofstede['country']=='Italy'], 1:8].values.flatten().tolist()
visitor = hofstede.iloc[hofstede.index[hofstede['country']=='Thailand'], 1:8].values.flatten().tolist()
sum = 0
variance = ?
for i, j in zip(host, visitor):
    print("======================================")
    print(i, j)
    sum += (pow((i/j), 2)/variance)/len(host)
    print(sum)







# found duplicate reviews, they are the same house but have different listing id
 




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