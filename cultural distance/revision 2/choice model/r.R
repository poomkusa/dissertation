setwd("D:/PhD/Dissertation/airbnb/cultural distance/raw data/venice_listings_long/")
filename = list.files(pattern="*.csv")
library(plyr)
library(dplyr)
readdata <- function(filename) {
  df <- read.csv(filename)
  df$neighbourhood_cleansed <- as.character(df$neighbourhood_cleansed)
  df <- select(df, id, neighbourhood_cleansed)
  df$date <- filename
  return(df)
}
result <- do.call(rbind.fill, lapply(filename, readdata))
library(feather)
path <- "C:/Users/ThisPC/Desktop/nbh.feather"
write_feather(result, path)

#mixed logit
library("mlogit")
library(feather)

df <- read_feather("D:/PhD/Dissertation/airbnb/cultural distance/choice model/murano/data1.feather")
df$choiceid  <- 1:nrow(df)
Tr <- dfidx(df, choice = "listing_id", varying = 12:55, sep = "_", idx = list(c("choiceid", "reviewer_id")), 
            idnames = c("chid", "alt"))


Train.mxlu <- mlogit(listing_id ~ sh + sh:cult_dst_6 | - 1, Tr,
                     panel = TRUE, rpar = c(sh = "u"), R = 100,
                     correlation = FALSE, halton = NA, method = "bhhh")
summary(Train.mxlu)

ml.MC1 <- mlogit(listing_id ~ sh + sh:cult_dst_6, Tr)
summary(ml.MC1)


