library(dplyr)

result <- select(read.csv("/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/raw data/venice_listings.csv"), 
               id, last_review, availability_30, host_is_superhost, host_response_rate, host_since,
               host_identity_verified, host_listings_count, review_scores_rating, number_of_reviews,
               price, bathrooms, bedrooms, review_scores_location)

#remove listing with no review         
length(which(result$last_review == ""))
length(which(result$number_of_reviews == 0))
result <- result[-which(result$number_of_reviews == 0), ]
result$last_review <- as.Date(result$last_review)
#remove listings with last review > 6m old
#NA means no review for that listing, dont know if inactive for 6m or noone gives a review
library(lubridate)
last_6m <- as.Date('2019/09/16') %m-% months(6)
length(which(result$last_review < last_6m))
result <- result[-which(result$last_review < last_6m), ]
############################################################################
### perf, availability_30
############################################################################
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
summary(result$logit_perf)
############################################################################
### host_is_superhost
############################################################################
#transform host_is_superhost from t,f to boolean
summary(result$host_is_superhost)
which(result$host_is_superhost != 't' & result$host_is_superhost != 'f')
which(result$host_is_superhost == "")
which(is.na(result$host_is_superhost))
result <- result[-which(result$host_is_superhost == ""), ]
result$host_is_superhost <- result$host_is_superhost == "t"
#result$host_is_superhost <- as.numeric(result$host_is_superhost)
############################################################################
### host_listings_count
############################################################################
#outlier because business exploiting airbnb
#effect should be u-shape, both ends have better performance
summary(result$host_listings_count)
hist(result$host_listings_count)
length(which(result$host_listings_count==0))
############################################################################
### review_scores_location
############################################################################
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

#drop unused columns
result <- result[ , !(names(result) %in% c("last_review","availability_30","host_response_rate","host_since",
                             "host_identity_verified","review_scores_rating"))]
library(feather)
write_feather(result, "/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/listing_clean.feather")
#df <- read_feather("path/to/file")

