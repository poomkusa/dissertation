import numpy as np
import pandas as pd
import feather
import pickle
import progressbar

df = feather.read_dataframe("D:/PhD/Dissertation/airbnb/cultural distance/listing_long_clean.feather")
#df = feather.read_dataframe("/home/poom/Desktop/phd/Dissertation/airbnb/cultural distance/listing_long_clean.feather")
df = df[['id', 'date', 'host_is_superhost', 'host_listings_count', 'number_of_reviews', 'price', 'id_date']]
df['yyyymm'] = df['date'].str[0:6]
data = pd.read_pickle("D:/PhD/Dissertation/airbnb/cultural distance/data_mini.pkl")
#data = pd.read_pickle("/home/poom/Desktop/phd/Dissertation/airbnb/cultural distance/data_mini.pkl")
data = data[['listing_id', 'id', 'date', 'reviewer_id', 'country', 'cult_dst_6']].copy()
data['id_date'] = data['listing_id'].apply(str) + "-" + data['date'].str[0:4] + data['date'].str[5:7]
data['yyyymm'] = data['date'].str[0:4] + data['date'].str[5:7]
data = data.rename(columns = {'id':'review_id'})
#check for missing data in data
data.isna().sum()
data = data.dropna()

#optional filter for each neighborhood
nbh = feather.read_dataframe("D:/PhD/Dissertation/airbnb/cultural distance/choice model/nbh.feather")
nbh = nbh[['id', 'neighbourhood_cleansed']]
freq = nbh['id'].value_counts(dropna=False)
nbh = nbh.drop_duplicates(subset=['id'])
df = pd.merge(left=df, right=nbh, left_on='id', right_on='id', how='left')
df = df[df.neighbourhood_cleansed == "Cannaregio"]
data = pd.merge(left=data, right=nbh, left_on='listing_id', right_on='id', how='left')
data = data[data.neighbourhood_cleansed == "Cannaregio"]
df.reset_index(drop=True, inplace=True)
data.reset_index(drop=True, inplace=True)

#check how many reviews in each year, how many houses are available for every period in each year
freq = data['date'].str[0:7].value_counts(dropna=False) #periods where at least 1 review exist
freq = df['id_date'].str[:-2].value_counts(dropna=False) #count of number of months the data is available for each house in each year
#create a table
summary = pd.DataFrame(columns=['period','num_house','num_review','cum_house','cum_review'])
#fill period column
summary.period = df['date'].str[0:6].unique()
summary = summary.sort_values(by=['period'], ascending=False)
summary.reset_index(drop=True, inplace=True)
#loop throught each period column
house_list = None
for i in range(len(summary)):
    #create a list of id from period i
    temp1 = df[df['yyyymm'].str.contains(summary.period[i])].id.unique()
    temp2 = data[data['yyyymm'].str.contains(summary.period[i])].review_id.unique()
    #check how many house in listing data has no review (dont need to check because if it exist in other period, removing it in this period would be wrong)
    #print(str(len(np.in1d(temp2, temp1)))) #not sure if the code is correct yet
    #number of houses and reviews in current period
    summary.num_house[i] = len(temp1)
    summary.num_review[i] = len(temp2)
    #another loop from period 0 to i-1
    for j in range(i):
        #keep only common id for temp1
        temp1 = np.intersect1d(temp1, df[df['yyyymm'].str.contains(summary.period[j])].id.unique())
        temp2 = np.concatenate([temp2, data[data['yyyymm'].str.contains(summary.period[j])].review_id.unique()])
    #cumulative number of house and review
    #####select wanted period
    if summary.period[i] == "201804":
        house_list = temp1
    summary.cum_house[i] = len(temp1)
    summary.cum_review[i] = len(temp2)
#export to excel
summary.to_csv("C:/Users/ThisPC/Desktop/output.csv")

#from summary table, remove houses that are not used in house data
house_list = pd.Series(house_list)
house_list = house_list.astype(str)
df['id'] = df['id'].astype(str)
df['id'] = np.where(df['id'].str.lower().isin(house_list.str.lower()), df['id'], np.nan)
df.isna().sum()
df = df[df['id'].notna()]
len(df['id'].unique())
#period (y-axis) and superhost (x-axis). superhost is one-hot encoding format
lookup = pd.DataFrame([house_list])
temp = pd.DataFrame({'period': np.append(['period'],summary['period'])})
lookup = pd.concat([temp, lookup], axis=1)
df = df[df.host_is_superhost != ""]
df['host_is_superhost'] = np.where(df['host_is_superhost']=="t", 1, 0)
df.reset_index(drop=True, inplace=True)
# with progressbar.ProgressBar(max_value=len(df)) as bar:
#     for i in range(1, len(lookup.columns)):
#         for j in range(1, len(lookup)):
#             for k in range(len(df)):
#                 if lookup.iloc[0, i] + "-" + lookup.iloc[j, 0] == df.id_date[k]:
#                     lookup.iloc[j, i] = df.host_is_superhost[k]
temp = house_list.tolist()
temp.insert(0, "period")
lookup.columns = temp
lookup.set_index('period', inplace=True)
with progressbar.ProgressBar(max_value=len(df)) as bar:
    for i in range(len(df)):
        bar.update(i)
        try:
            lookup.loc[[df.yyyymm[i]], [df.id[i]]] = df.host_is_superhost[i]
        except Exception as e:
            print(str(e))
#####select wanted period            
lookup.drop(lookup.tail(2).index, inplace = True) 
x=lookup.isna().sum()
x[x == 1].index
len(x[x == 1].index)
lookup[x[x == 1].index]
lookup.drop(x[x == 1].index, axis=1, inplace=True)
#feather.write_dataframe(lookup, "C:/Users/ThisPC/Desktop/lookup.feather")
lookup.to_csv(r"C:/Users/ThisPC/Desktop/lookup.csv")

#rename column name, remove first row, merge
temp = 'sh_' + lookup.iloc[0]
temp = temp.tolist()
lookup.columns = temp
lookup['period'] = lookup.index
lookup.reset_index(drop=True, inplace=True)
lookup = lookup.iloc[1:]
#merge above into review data
data['period'] = data['id_date'].str[-6:]
#####select wanted period
keep_list = lookup['period'].tolist()[:18]
data = data[data['period'].isin(keep_list)]
data = data[data['listing_id'].isin(house_list)]
reg_dta = pd.merge(left=data, right=lookup, left_on='period', right_on='period', how='left')
feather.write_dataframe(reg_dta, "C:/Users/ThisPC/Desktop/data1.feather")



