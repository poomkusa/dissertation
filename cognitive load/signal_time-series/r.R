setwd("/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/airbnb_data/")
filename = list.files(pattern="*.csv")
library(dplyr)
library(plyr)
readdata <- function(filename) {
  df <- read.csv(filename)
  df$date <- filename
  return(df)
}
# for (i in 1:length(filename)){
#   assign(filename[i], readdata(filename[i]))
# }
#rbind into 1 big df
result <- do.call(rbind.fill, lapply(filename, readdata))
rm(filename, readdata)
save(result, file="/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/raw_combined.Rda")
load("/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/raw_combined.Rda")

sort(colnames(result))
#loop through each column and return a column name with NA > 30000
result <- select(result, availability_30, host_is_superhost, id, host_id, date,
                 host_response_rate, host_since, host_identity_verified, host_listings_count, 
                 review_scores_rating, review_scores_location,
                 number_of_reviews, price, bathrooms, bedrooms, neighbourhood_cleansed
                 #, everything()
)

#transform occupancy into logit(percentage)
which(is.na(result$availability_30))
which(result$availability_30 == "")
summary(result$availability_30)
epsilon <- 0.0000001
percent_perf <- (30-result$availability_30)/30
result$perf <- ifelse(percent_perf == 0, percent_perf+epsilon, percent_perf)
result$perf <- ifelse(percent_perf == 1, percent_perf-epsilon, result$perf)
result$logit_perf <- log(result$perf/(1-result$perf))
rm(epsilon, percent_perf)
summary(result$perf30)

#create time var
result$t <- as.integer(substr(result$date,1,8))
result <- result[with(result, order(id, t)), ]

save(result, file="/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/final.Rda")
load("/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/final.Rda")

#transform host_is_superhost from t,f to boolean
summary(result$host_is_superhost)
which(result$host_is_superhost != 't' & result$host_is_superhost != 'f')
which(result$host_is_superhost == "")
which(is.na(result$host_is_superhost))
result <- result[-which(result$host_is_superhost == ""), ]
result$host_is_superhost <- result$host_is_superhost == "t"
#result$host_is_superhost <- as.numeric(result$host_is_superhost)

#dont forget to include var like room type (check in previous paper)
#########################################################################################
############################################################################
### host_response_rate (didnt use)
############################################################################
#lost 621345
#transform host_response_rate
summary(result$host_response_rate)
result <- result[-which(result$host_response_rate == "N/A"), ]
result$host_response_rate = as.character(result$host_response_rate)
result$host_response_rate = gsub("%", "", result$host_response_rate)
result$host_response_rate <- as.double(result$host_response_rate)
############################################################################
### membership, host_since (didnt use)
############################################################################
result$host_since <- as.Date(result$host_since)
which(is.na(result$host_since))
summary(result$host_since)
scraped_date <- as.Date(as.character(result$t), format='%Y%m%d')
result$membership <- (scraped_date - result$host_since)/365
result$membership <- as.numeric(result$membership)
summary(result$membership)
rm(scraped_date)
############################################################################
### host_identity_verified (didnt use)
############################################################################
#some listing show 0 host_listings_count
summary(result$host_identity_verified)
which(result$host_identity_verified != 't' & result$host_identity_verified != 'f')
which(result$host_identity_verified == "")
which(is.na(result$host_identity_verified))
result$host_identity_verified <- result$host_identity_verified == "t"
result$host_identity_verified <- as.numeric(result$host_identity_verified)
############################################################################
### host_listings_count
############################################################################
#outlier because business exploiting airbnb
#effect should be u-shape, both ends have better performance
summary(result$host_listings_count)
hist(result$host_listings_count)
length(which(result$host_listings_count==0))
############################################################################
### review_scores_rating (didnt use)
############################################################################
#lost 192404
#some listing doesnt have rating but the scraped data has! 
#A host needs to receive star ratings from at least 3 guests before their aggregate score appears.
summary(result$review_scores_rating)
length(which(result$number_of_reviews == 0))
which(is.na(result$review_scores_rating))
result <- result[-which(is.na(result$review_scores_rating)), ]
############################################################################
### review_scores_location
############################################################################
#lost 453064 
#same issue as rating
summary(result$review_scores_location)
length(which(result$review_scores_location == 0))
which(is.na(result$review_scores_location))
result <- result[-which(is.na(result$review_scores_location)), ]
############################################################################
### number_of_reviews
############################################################################
summary(result$number_of_reviews)
hist(result$number_of_reviews)
length(which(is.na(result$number_of_reviews)))
which(is.na(result$number_of_reviews))
which(result$number_of_reviews==0)
############################################################################
### price
############################################################################
#some prices are too low
#transform price ($1,000.00 -> 1000.00)
#some price is 0
summary(result$price)
unique(result$price)
which(is.na(result$price))
which(result$price == "")
which(grepl("n", result$price, ignore.case=TRUE) == TRUE)
result$price = gsub("[\\$,]", "", result$price)
result$price <- as.numeric(result$price)
summary(result$price)
length(which(result$price==0))
which(result$price==0)
result$listing_url[which(result$price==0)]
############################################################################
### bathrooms
############################################################################
#lost 4437
#there are 0 bathrooms and bedrooms
summary(result$bathrooms)
which(is.na(result$bathrooms))
result$listing_url[is.na(result$bathrooms)]
result <- result[-which(is.na(result$bathrooms)), ]
############################################################################
### bedrooms
############################################################################
#lost 2023
summary(result$bedrooms)
which(is.na(result$bedrooms))
result$listing_url[is.na(result$bedrooms)]
result <- result[-which(is.na(result$bedrooms)), ]
############################################################################
### beds (didnt use)
############################################################################
summary(result$beds)
which(is.na(result$beds))
result$listing_url[is.na(result$beds)]
# dta <- dta[-which(is.na(data$beds)), ]
# data <- data[-which(is.na(data$beds)), ]
# ############################################################################
# ### amenities_num, amenities (didnt use)
# ############################################################################
# which(data$amenities == "")
# which(is.na(data$amenities))
# which(data$amenities == "N/A")
# which(grepl("na", data$amenities, ignore.case=TRUE) == TRUE)
# which(grepl("n/a", data$amenities, ignore.case=TRUE) == TRUE)
# data$amenities = as.character(data$amenities)
# #check whether a listing has toiletry (Towels, soap, Shampoo), TV, , Wifi, Air conditioning, Refrigerator
# dta$tv <- grepl("TV", data$amenities, ignore.case=TRUE)
# dta$wifi <- grepl("Wifi", data$amenities, ignore.case=TRUE)
# dta$ac <- grepl("Air conditioning", data$amenities, ignore.case=TRUE)
# dta$fridge <- grepl("Refrigerator", data$amenities, ignore.case=TRUE)
# dta$towel <- grepl("Towel", data$amenities, ignore.case=TRUE)
# dta$soap <- grepl("soap", data$amenities, ignore.case=TRUE)
# dta$shampoo <- grepl("Shampoo", data$amenities, ignore.case=TRUE)
# dta$toiletry <- dta$towel & dta$soap & dta$shampoo
# dta$tv <- as.numeric(dta$tv)
# dta$wifi <- as.numeric(dta$wifi)
# dta$ac <- as.numeric(dta$ac)
# dta$fridge <- as.numeric(dta$fridge)
# dta$toiletry <- as.numeric(dta$toiletry)
############################################################################
### accommodates (didnt use)
############################################################################
summary(result$accommodates)
which(is.na(result$accommodates))
# dta <- dta[-which(is.na(data$accommodates)), ]
# data <- data[-which(is.na(data$accommodates)), ]
############################################################################
### density, avg_price, neighbourhood_cleansed
############################################################################
which(result$neighbourhood_cleansed == "")
summary(result$neighbourhood_cleansed)
#calculate density and avg_price based on neigborhood
result$neighborhood <- result$neighbourhood_cleansed
freq_neighborhood <- as.data.frame(table(result$neighbourhood_cleansed))
avg_price_neighborhood <- aggregate(result$price, list(result$neighborhood), mean)
freq_price <- merge(x=freq_neighborhood, y=avg_price_neighborhood, by.x="Var1", by.y="Group.1")
temp <- merge(x=result, y=freq_price, by.x="neighborhood", by.y="Var1", all.x = TRUE)
temp <- temp[order(temp$id),]
result$density_nbh <- temp$Freq
result$avg_price_nbh <- temp$x
result$neighborhood <- NULL
rm(freq_neighborhood, avg_price_neighborhood, freq_price, temp)

save(result, file="/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/final_more_var.Rda")
load("/media/poom/Backup/PhD/Dissertation/airbnb/cognitive load/2-time_series/final_more_var.Rda")
#########################################################################################

#balance panel data
library(plm)
is.pbalanced(result, index = c("id","t"))
x <- make.pbalanced(result, balance.type = c("shared.individuals"), index = c("id","t"))
is.pbalanced(x, index = c("id","t"))

#fixed effect model (across individual and time)
#panel var should be factor
library(plm)
result$superhostxnum_reviews <- result$host_is_superhost*result$number_of_reviews
result$superhostxdensity <- result$host_is_superhost*result$density_nbh
fe <- plm(logit_perf ~ host_is_superhost + superhostxnum_reviews + host_listings_count + review_scores_location + number_of_reviews + price + bathrooms + bedrooms,
          data = result,
          index = c("id", "t"),
          model = "within",
          effect = "twoways")
summary(fe)
fixef(fe) # Display the fixed effects (constants for each country)
pcdtest(fe, test = c("lm")) # Testing for cross-sectional dependence, sig -> there is
library(lmtest) # Testing for heteroskedasticity, sig -> hetero
bptest(perf30 ~ host_is_superhost + factor(id) + factor(t), data = result, studentize=F)
pbgtest(fe) # Testing for serial correlation, sig -> there is
library(tseries) # test for stationarity, sig -> stationary
adf.test(result$perf30, k=2)
library(car)
scatterplot(perf30~t|id, boxplots=FALSE, smooth=TRUE, reg.line=FALSE, data=result)

library(lmtest)
coeftest(fe, vcov = vcovHC, type = "HC1")