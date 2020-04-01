library(dplyr)
scraped_date <- as.Date('2019/09/19')
data <- select(read.csv("/home/poom/Desktop/airbnb_data/austin_tx.csv"), id, listing_url, last_review, 
               availability_30, host_location, host_is_superhost, host_response_rate, host_since, 
               host_identity_verified, host_listings_count, review_scores_rating, number_of_reviews, price, 
               bathrooms, bedrooms, beds, amenities, accommodates, review_scores_location, 
               neighbourhood_cleansed, city, state)
data$last_review <- as.Date(data$last_review)
dta <- select(data, id, listing_url)
#remove listings with last review > 6m old
#NA means no review for that listing, dont know if inactive for 6m or noone gives a review
length(which(is.na(data$last_review)))
length(which(data$number_of_reviews == 0))
length(which(data$last_review < as.Date('2019/03/19')))
dta <- dta[-which(data$last_review < as.Date('2019/03/19')), ]
data <- data[-which(data$last_review < as.Date('2019/03/19')), ]
############################################################################
### perf, availability_30
############################################################################
#transform occupancy into logit(percentage)
which(is.na(data$availability_30))
which(data$availability_30 == "")
summary(data$availability_30)
epsilon <- 0.0000001
percent_perf <- (30-data$availability_30)/30
dta$percent_perf <- percent_perf
library(car)
dta$pkg_logit_perf <- logit(percent_perf, adjust=epsilon)
for (i in 1:nrow(dta)){
  if(dta$percent_perf[i] == 0) {dta$perf_[i] = dta$percent_perf[i]+epsilon
  }else if(dta$percent_perf[i] == 1) {dta$perf_[i] = dta$percent_perf[i]-epsilon
  }else {dta$perf_[i] = dta$percent_perf[i]}
}
# dta$perf <- ifelse(percent_perf == 0, percent_perf+epsilon, percent_perf)
# dta$perf <- ifelse(percent_perf == 1, percent_perf-epsilon, dta$perf)
dta$logit_perf <- log(dta$perf_/(1-dta$perf_))
rm(epsilon, percent_perf)
############################################################################
### local_host, host_location
############################################################################
#some people only say US or tx, cant tell if local or not
x=grep("austin", data$host_location, ignore.case=TRUE, value=TRUE)
unique(x)
x=grep("austin", data$host_location, ignore.case=TRUE, value=TRUE, invert=TRUE)
unique(x)
dta$local_host[grep("austin", data$host_location, ignore.case=TRUE, value=FALSE)]=1
dta$local_host[grep("austin", data$host_location, ignore.case=TRUE, value=FALSE, invert=TRUE)]=0
rm(x)
############################################################################
### host_is_superhost
############################################################################
#transform host_is_superhost from t,f to boolean
summary(data$host_is_superhost)
which(data$host_is_superhost != 't' & data$host_is_superhost != 'f')
which(data$host_is_superhost == "")
which(is.na(data$host_is_superhost))
dta <- dta[-which(data$host_is_superhost == ""), ]
data <- data[-which(data$host_is_superhost == ""), ]
dta$host_is_superhost <- data$host_is_superhost == "t"
dta$host_is_superhost <- as.numeric(dta$host_is_superhost)
############################################################################
### host_response_rate
############################################################################
#r1779 missing value, dont know if missing value or noone asks a question
#transform host_response_rate
summary(data$host_response_rate)
which(data$host_response_rate == "N/A")
dta <- dta[-which(data$host_response_rate == "N/A"), ]
data <- data[-which(data$host_response_rate == "N/A"), ]
dta$host_response_rate = as.character(data$host_response_rate)
dta$host_response_rate = gsub("%", "", dta$host_response_rate)
dta$host_response_rate <- as.double(dta$host_response_rate)
############################################################################
### membership, host_since
############################################################################
data$host_since <- as.Date(data$host_since)
which(is.na(data$host_since))
summary(data$host_since)
dta$membership <- (scraped_date - data$host_since)/365
dta$membership <- as.numeric(dta$membership)
summary(dta$membership)
which(is.na(dta$membership))
############################################################################
### host_identity_verified
############################################################################
summary(data$host_identity_verified)
which(data$host_identity_verified != 't' & data$host_identity_verified != 'f')
which(data$host_identity_verified == "")
which(is.na(data$host_identity_verified))
# dta <- dta[-which(data$host_identity_verified == ""), ]
# data <- data[-which(data$host_identity_verified == ""), ]
dta$host_identity_verified <- data$host_identity_verified == "t"
dta$host_identity_verified <- as.numeric(dta$host_identity_verified)
############################################################################
### host_listings_count
############################################################################
#outlier because business exploiting airbnb
summary(data$host_listings_count)
hist(data$host_listings_count)
length(which(data$host_listings_count>100))
which(data$host_listings_count==1799)
data$listing_url[2736]
dta$host_listings_count <- data$host_listings_count
############################################################################
### review_scores_rating
############################################################################
#42 missing data or someone reviews without rating, the rest are because theres no review
summary(data$review_scores_rating)
length(which(is.na(data$review_scores_rating)))
length(which(data$number_of_reviews == 0))
which(is.na(data$review_scores_rating))
data$listing_url[18]
dta <- dta[-which(is.na(data$review_scores_rating)), ]
data <- data[-which(is.na(data$review_scores_rating)), ]
dta$review_scores_rating <- data$review_scores_rating
############################################################################
### review_scores_location
############################################################################
#same issue as rating
summary(data$review_scores_location)
length(which(is.na(data$review_scores_location)))
length(which(data$number_of_reviews == 0))
which(is.na(data$review_scores_location))
data$listing_url[18]
# dta <- dta[-which(is.na(data$review_scores_location)), ]
# data <- data[-which(is.na(data$review_scores_location)), ]
dta$review_scores_location <- data$review_scores_location
############################################################################
### number_of_reviews
############################################################################
summary(data$number_of_reviews)
hist(data$number_of_reviews)
length(which(is.na(data$number_of_reviews)))
which(is.na(data$number_of_reviews))
data$listing_url[18]
# dta <- data[-which(is.na(data$number_of_reviews)), ]
# data <- data[-which(is.na(data$number_of_reviews)), ]
dta$number_of_reviews <- data$number_of_reviews
############################################################################
### price
############################################################################
#transform price ($1,000.00 -> 1000.00)
which(is.na(data$price))
which(data$price == "")
dta$price = gsub("[\\$,]", "", data$price)
dta$price <- as.numeric(dta$price)
summary(dta$price)
############################################################################
### bathrooms
############################################################################
summary(data$bathrooms)
which(is.na(data$bathrooms))
data$listing_url[1]
data$bathrooms[1] <- 1
# dta <- dta[-which(is.na(data$bathrooms)), ]
# data <- data[-which(is.na(data$bathrooms)), ]
dta$bathrooms <- data$bathrooms
############################################################################
### bedrooms
############################################################################
summary(data$bedrooms)
which(is.na(data$bedrooms))
# dta <- dta[-which(is.na(data$bedrooms)), ]
# data <- data[-which(is.na(data$bedrooms)), ]
dta$bedrooms <- data$bedrooms
############################################################################
### beds
############################################################################
summary(data$beds)
which(is.na(data$beds))
# dta <- dta[-which(is.na(data$beds)), ]
# data <- data[-which(is.na(data$beds)), ]
dta$beds <- data$beds
############################################################################
### amenities_num, amenities
############################################################################
which(data$amenities == "")
which(is.na(data$amenities))
which(data$amenities == "N/A")
data$amenities = as.character(data$amenities)
#check whether a listing has toiletry (Towels, soap, Shampoo), TV, , Wifi, Air conditioning, Refrigerator
dta$tv <- grepl("TV", data$amenities, ignore.case=TRUE)
dta$wifi <- grepl("Wifi", data$amenities, ignore.case=TRUE)
dta$ac <- grepl("Air conditioning", data$amenities, ignore.case=TRUE)
dta$fridge <- grepl("Refrigerator", data$amenities, ignore.case=TRUE)
towel <- grepl("Towel", data$amenities, ignore.case=TRUE)
soap <- grepl("soap", data$amenities, ignore.case=TRUE)
shampoo <- grepl("Shampoo", data$amenities, ignore.case=TRUE)
dta$toiletry <- towel & soap & shampoo
rm(towel, soap, shampoo)
#count number of amenities
library(stringr)
dta$amenities_num <- str_count(data$amenities, ",") + 1
############################################################################
### accommodates
############################################################################
summary(data$accommodates)
which(is.na(data$accommodates))
# dta <- dta[-which(is.na(data$accommodates)), ]
# data <- data[-which(is.na(data$accommodates)), ]
dta$accommodates <- data$accommodates
############################################################################
### density, avg_price, neighbourhood_cleansed
############################################################################
which(data$neighbourhood_cleansed == "")
summary(data$neighbourhood_cleansed)
dta$neighborhood <- data$neighbourhood_cleansed
freq_neighborhood <- as.data.frame(table(data$neighbourhood_cleansed))
avg_price_neighborhood <- aggregate(dta$price, list(dta$neighborhood), mean)
freq_price <- merge(x=freq_neighborhood, y=avg_price_neighborhood, by.x="Var1", by.y="Group.1")
temp <- merge(x=dta, y=freq_price, by.x="neighborhood", by.y="Var1", all.x = TRUE)
temp <- temp[order(temp$id),]
dta$density <- temp$Freq
dta$avg_price <- temp$x
dta$neighborhood <- NULL
rm(freq_neighborhood, avg_price_neighborhood, freq_price, temp)
############################################################################
### city
############################################################################
summary(data$city)
which(data$city == "")
which(is.na(data$city))
which(data$city == "N/A")
dta$city <- "austin"
############################################################################
### state
############################################################################
summary(data$state)
which(data$state == "")
which(is.na(data$state))
which(data$state == "N/A")
dta$state <- "texas"
############################################################################
dta$moderator1 <- dta$host_is_superhost * dta$density
est <- lm(percent_perf ~ local_host + host_response_rate + membership + host_identity_verified +
            host_listings_count + review_scores_rating + number_of_reviews + price + bathrooms + bedrooms +
            beds + amenities_num + accommodates + review_scores_location + 
            avg_price + host_is_superhost + density + moderator1, data=dta)
summary(est)

est <- lm(percent_perf ~  host_is_superhost + density + moderator1 + price + avg_price, data=dta)
est <- lm(percent_perf ~  host_is_superhost + density + moderator1 + price + avg_price +
            review_scores_rating, data=dta)
dta$moderator2 <- dta$host_is_superhost * dta$review_scores_rating
est <- lm(percent_perf ~  host_is_superhost + density + moderator1 + price + avg_price +
            review_scores_rating + moderator2, data=dta)
