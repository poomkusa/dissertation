setwd("D:/PhD/Dissertation/airbnb/cultural distance/raw data/venice_listings_long/")
filename = list.files(pattern="*.csv")
library(plyr)
library(dplyr)
readdata <- function(filename) {
  df <- read.csv(filename)
  df$date <- filename
  return(df)
}
result <- do.call(rbind.fill, lapply(filename, readdata))
rm(filename, readdata)

result <- select(result, 
               id, last_review, availability_30, host_is_superhost, host_response_rate, host_since,
               host_identity_verified, host_listings_count, review_scores_rating, review_scores_accuracy,
               review_scores_value, number_of_reviews, date,
               price, bathrooms, bedrooms, review_scores_location)
result$id_date <- paste(result$id, substr(result$date,1,6), sep="-")


############################################################################
### review_scores_rating
############################################################################
summary(result$review_scores_location)
length(which(result$review_scores_location == 0))
which(is.na(result$review_scores_location))
result <- result[-which(is.na(result$review_scores_location)), ]
############################################################################
### review_scores_accuracy
############################################################################
summary(result$review_scores_accuracy)
length(which(result$review_scores_accuracy == 0))
which(is.na(result$review_scores_accuracy))
result <- result[-which(is.na(result$review_scores_accuracy)), ]
############################################################################
### review_scores_value
############################################################################
summary(result$review_scores_value)
length(which(result$review_scores_value == 0))
which(is.na(result$review_scores_value))
result <- result[-which(is.na(result$review_scores_value)), ]
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

#drop unused columns
# result <- result[ , !(names(result) %in% c("last_review","availability_30","host_response_rate","host_since",
#                              "host_identity_verified","review_scores_rating"))]
library(feather)
write_feather(result, "C:/Users/ThisPC/Desktop/listing_long_clean.feather")
#df <- read_feather("path/to/file")

