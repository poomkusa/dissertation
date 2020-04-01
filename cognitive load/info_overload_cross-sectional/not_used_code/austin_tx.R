library(dplyr)
#library(tidy)
#library(purrr)
# library("ggmap")
# register_google(key = "AIzaSyC5cMXiO0IakLyaF6VYcYuMlhAK-B_wxU8")

#check missing value, outlier

data <- select(read.csv("/home/poom/Desktop/listings.csv"), id, listing_url, description, house_rules, 
               host_since, host_location, host_response_time, host_response_rate, host_is_superhost,
               host_listings_count, host_identity_verified, city, zipcode, country, latitude, longitude, 
               is_location_exact, accommodates, bathrooms, bedrooms, beds, amenities, price, weekly_price, 
               monthly_price, extra_people, minimum_nights, availability_30, number_of_reviews, 
               review_scores_rating, review_scores_location, cancellation_policy, neighbourhood, 
               neighbourhood_cleansed, last_review)
data$last_review <- as.Date(data$last_review)
dta <- select(data, id, listing_url)

#remove listings with last review > 6m old
length(which(data$last_review < as.Date('2019/01/12')))
dta <- dta[-which(data$last_review < as.Date('2019/01/12')), ]
data <- data[-which(data$last_review < as.Date('2019/01/12')), ]

#transform host_is_superhost from t,f to boolean
which(data$host_is_superhost != 't' & data$host_is_superhost != 'f')
which(data$host_is_superhost == "") #should remove because we cant check the status in the past
dta <- dta[-which(data$host_is_superhost == ""), ]
data <- data[-which(data$host_is_superhost == ""), ]
dta$host_is_superhost <- data$host_is_superhost == "t"
#dta$host_is_superhost <- as.numeric(dta$host_is_superhost)

#transform price ($1,000.00 -> 1000.00)
dta$price = gsub("[\\$,]", "", data$price)
dta$price <- as.numeric(dta$price)

#reverse geocode from long/lat
# res <- revgeocode(c(long, lat), output="address")
#count number of listings in a zipcode, create new variable - avg price in a zipcode
# dta$num_competitors <- NA
# for(i in 1:nrow(dta)) {
#   dta$num_competitors[i] = length(which(data$zipcode == data$zipcode[i]))
#   dta$avg_price_zip[i] = mean(data$price[which(data$zipcode == data$zipcode[i])])
# }
# dta <- dta[-which(data$zipcode == ""), ]
# data <- data[-which(data$zipcode == ""), ]
# data$zipcode <- toupper(data$zipcode)
# dta$zipcode <- data$zipcode
# freq_zipcode <- as.data.frame(table(data$zipcode))
# avg_price_zipcode <- aggregate(dta$price, list(dta$zipcode), mean)
# freq_price <- merge(x=freq_zipcode, y=avg_price_zipcode, by.x="Var1", by.y="Group.1")
# temp <- merge(x=dta, y=freq_price, by.x="zipcode", by.y="Var1", all.x = TRUE)
# temp <- temp[order(temp$id),]
# dta$num_competitors_zip <- temp$Freq
# dta$price_area_zip <- temp$x
# dta$zipcode <- NULL
# rm(freq_zipcode, avg_price_zipcode, freq_price, temp)
#count number of listings in a neighborhood, create new variable - avg price in a neighborhood
which(data$neighbourhood_cleansed == "")
dta$neighborhood <- data$neighbourhood_cleansed
freq_neighborhood <- as.data.frame(table(data$neighbourhood_cleansed))
avg_price_neighborhood <- aggregate(dta$price, list(dta$neighborhood), mean)
freq_price <- merge(x=freq_neighborhood, y=avg_price_neighborhood, by.x="Var1", by.y="Group.1")
temp <- merge(x=dta, y=freq_price, by.x="neighborhood", by.y="Var1", all.x = TRUE)
temp <- temp[order(temp$id),]
dta$num_competitors <- temp$Freq
dta$price_area <- temp$x
dta$neighborhood <- NULL
rm(freq_neighborhood, avg_price_neighborhood, freq_price, temp)

#transform host_response_rate
# dta$host_response_rate = as.character(data$host_response_rate)
# dta$host_response_rate = gsub("%", "", dta$host_response_rate)
# dta$host_response_rate <- as.double(dta$host_response_rate)

#transform occupancy into logit(percentage)
epsilon <- 0.0000001
percent_perf1m <- (30-data$availability_30)/30
dta$dv_quasibino <- percent_perf1m
percent_perf1m <- ifelse(percent_perf1m == 0, percent_perf1m+epsilon, percent_perf1m)
percent_perf1m <- ifelse(percent_perf1m == 1, percent_perf1m-epsilon, percent_perf1m)
dta$logit_percent_perf1m <- log(percent_perf1m/(1-percent_perf1m))
rm(epsilon, percent_perf1m)

#other control var
#bathrooms, bedrooms, beds, review_scores_rating-NA
dta$host_listings_count <- data$host_listings_count
dta$host_identity_verified <- data$host_identity_verified == "t"
dta$accommodates <- data$accommodates
dta$number_of_reviews <- data$number_of_reviews


dta$moderator <- dta$host_is_superhost * dta$num_competitors
est <- lm(logit_percent_perf1m ~ host_is_superhost + num_competitors + moderator +
            price + price_area + host_listings_count + host_identity_verified + accommodates + 
            number_of_reviews, data=dta)
summary(est)

#quasibinomial
m = glm(dv_quasibino ~ host_is_superhost + num_competitors + moderator + price + 
          price_area + host_listings_count + host_identity_verified + accommodates + 
          number_of_reviews, dta,family=quasibinomial())
summary(m)
