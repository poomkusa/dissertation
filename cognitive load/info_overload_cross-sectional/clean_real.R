filename <- "hawaii_hi"
scraped_date <- as.Date('2019/09/12')

library(dplyr)
data <- select(read.csv(paste(
  "/home/poom/Desktop/thammasat/2y1s/DB864 Contemporary Empirical Research in Marketing II/term paper/airbnb/study2/airbnb_data/",
  filename, ".csv", sep="")), id, listing_url, last_review, availability_30, host_is_superhost, 
  host_response_rate, host_since, host_identity_verified, host_listings_count, review_scores_rating, 
  number_of_reviews, price, bathrooms, bedrooms, beds, amenities, accommodates, review_scores_location, 
  neighbourhood_cleansed, zipcode, latitude, longitude, is_location_exact, city, last_scraped)
length(which(data$last_review == ""))
length(which(data$number_of_reviews == 0))
data <- data[-which(data$number_of_reviews == 0), ]
data$last_review <- as.Date(data$last_review)
dta <- select(data, id, listing_url)
#remove listings with last review > 6m old
#NA means no review for that listing, dont know if inactive for 6m or noone gives a review
library(lubridate)
last_6m <- scraped_date %m-% months(6)
length(which(data$last_review < last_6m))
dta <- dta[-which(data$last_review < last_6m), ]
data <- data[-which(data$last_review < last_6m), ]
############################################################################
### perf, availability_30
############################################################################
#transform occupancy into logit(percentage)
which(is.na(data$availability_30))
which(data$availability_30 == "")
summary(data$availability_30)
epsilon <- 0.0000001
percent_perf <- (30-data$availability_30)/30
dta$perf <- ifelse(percent_perf == 0, percent_perf+epsilon, percent_perf)
dta$perf <- ifelse(percent_perf == 1, percent_perf-epsilon, dta$perf)
dta$logit_perf <- log(dta$perf/(1-dta$perf))
rm(epsilon, percent_perf)
############################################################################
### host_is_superhost
############################################################################
#transform host_is_superhost from t,f to boolean
summary(data$host_is_superhost)
which(data$host_is_superhost != 't' & data$host_is_superhost != 'f')
which(data$host_is_superhost == "")
which(is.na(data$host_is_superhost))
# dta <- dta[-which(data$host_is_superhost == ""), ]
# data <- data[-which(data$host_is_superhost == ""), ]
dta$host_is_superhost <- data$host_is_superhost == "t"
dta$host_is_superhost <- as.numeric(dta$host_is_superhost)
############################################################################
### host_response_rate
############################################################################
#1779 missing value, dont know if missing value or noone asks a question
#transform host_response_rate
summary(data$host_response_rate)
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
# dta <- dta[-which(is.na(data$host_since)), ]
# data <- data[-which(is.na(data$host_since)), ]
dta$membership <- (scraped_date - data$host_since)/365
dta$membership <- as.numeric(dta$membership)
summary(dta$membership)
############################################################################
### host_identity_verified
############################################################################
#some listing show 0 host_listings_count
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
#effect should be u-shape, both ends have better performance
summary(data$host_listings_count)
hist(data$host_listings_count)
length(which(data$host_listings_count==0))
dta$host_listings_count <- data$host_listings_count
############################################################################
### review_scores_rating
############################################################################
#36 missing data or someone reviews without rating, the rest are because theres no review
#some listing doesnt have rating but the scraped data has! 
#A host needs to receive star ratings from at least 3 guests before their aggregate score appears.
summary(data$review_scores_rating)
length(which(data$number_of_reviews == 0))
which(is.na(data$review_scores_rating))
dta <- dta[-which(is.na(data$review_scores_rating)), ]
data <- data[-which(is.na(data$review_scores_rating)), ]
dta$review_scores_rating <- data$review_scores_rating
############################################################################
### review_scores_location
############################################################################
#same issue as rating
summary(data$review_scores_location)
length(which(data$number_of_reviews == 0))
which(is.na(data$review_scores_location))
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
which(data$number_of_reviews==0)
# dta <- dta[-which(is.na(data$number_of_reviews)), ]
# data <- data[-which(is.na(data$number_of_reviews)), ]
dta$number_of_reviews <- data$number_of_reviews
############################################################################
### price
############################################################################
#some prices are too low
#transform price ($1,000.00 -> 1000.00)
#some price is 0
summary(data$price)
unique(data$price)
which(is.na(data$price))
which(data$price == "")
which(grepl("n", data$price, ignore.case=TRUE) == TRUE)
dta$price = gsub("[\\$,]", "", data$price)
dta$price <- as.numeric(dta$price)
summary(dta$price)
length(which(dta$price==0))
which(dta$price==0)
dta$listing_url[which(dta$price==0)]
############################################################################
### bathrooms
############################################################################
#there are 0 bathrooms and bedrooms
summary(data$bathrooms)
which(is.na(data$bathrooms))
data$listing_url[is.na(data$bathrooms)]
# data$bathrooms[which(is.na(data$bathrooms))] <- 1
# dta <- dta[-which(is.na(data$bathrooms)), ]
# data <- data[-which(is.na(data$bathrooms)), ]
# dta <- dta[-c(12725), ]
# data <- data[-c(12725), ]
dta$bathrooms <- data$bathrooms
############################################################################
### bedrooms
############################################################################
summary(data$bedrooms)
which(is.na(data$bedrooms))
data$listing_url[is.na(data$bedrooms)]
# dta <- dta[-which(is.na(data$bedrooms)), ]
# data <- data[-which(is.na(data$bedrooms)), ]
dta$bedrooms <- data$bedrooms
############################################################################
### beds
############################################################################
summary(data$beds)
which(is.na(data$beds))
data$listing_url[is.na(data$beds)]
# dta <- dta[-which(is.na(data$beds)), ]
# data <- data[-which(is.na(data$beds)), ]
dta$beds <- data$beds
############################################################################
### amenities_num, amenities
############################################################################
which(data$amenities == "")
which(is.na(data$amenities))
which(data$amenities == "N/A")
which(grepl("na", data$amenities, ignore.case=TRUE) == TRUE)
which(grepl("n/a", data$amenities, ignore.case=TRUE) == TRUE)
data$amenities = as.character(data$amenities)
#check whether a listing has toiletry (Towels, soap, Shampoo), TV, , Wifi, Air conditioning, Refrigerator
dta$tv <- grepl("TV", data$amenities, ignore.case=TRUE)
dta$wifi <- grepl("Wifi", data$amenities, ignore.case=TRUE)
dta$ac <- grepl("Air conditioning", data$amenities, ignore.case=TRUE)
dta$fridge <- grepl("Refrigerator", data$amenities, ignore.case=TRUE)
dta$towel <- grepl("Towel", data$amenities, ignore.case=TRUE)
dta$soap <- grepl("soap", data$amenities, ignore.case=TRUE)
dta$shampoo <- grepl("Shampoo", data$amenities, ignore.case=TRUE)
dta$toiletry <- dta$towel & dta$soap & dta$shampoo
dta$tv <- as.numeric(dta$tv)
dta$wifi <- as.numeric(dta$wifi)
dta$ac <- as.numeric(dta$ac)
dta$fridge <- as.numeric(dta$fridge)
dta$toiletry <- as.numeric(dta$toiletry)
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
x <- data
x$zip_precise <- TRUE
x$zipcode <- as.character(x$zipcode)
unique(x$zipcode)
a <- data.frame("zip"=unique(x$zipcode))
#remove state name (e.g. "IL") from the begining of zipcode
x$zipcode <- ifelse(grepl(toupper(substr(filename, nchar(filename)-1, nchar(filename))), x$zipcode, ignore.case=FALSE), substr(x$zipcode, 4, 8), x$zipcode)
#add 0 in at the beginning of zipcode
x$zipcode <- ifelse(grepl("2", substr(x$zipcode,1,1), ignore.case=FALSE), paste("0",x$zipcode, sep=""), x$zipcode)
#substring only the first 5 characters of zipcode
x$zipcode <- ifelse(grepl("-", x$zipcode, ignore.case=FALSE), substr(x$zipcode,1,5), x$zipcode)
#reverse geocode from long/lat
library("ggmap")
register_google(key = "AIzaSyC5cMXiO0IakLyaF6VYcYuMlhAK-B_wxU8")
state <- paste(toupper(substr(filename, nchar(filename)-1, nchar(filename))), " ", sep="")
count <- 1
for(i in which(x$zipcode=="")){
#for(i in which(is.na(x$zipcode))){
  cat(paste("count:", count, "\tindex:", i, "\turl:", x$listing_url[i], "\tis_location_exact:", x$is_location_exact[i], "\n"))
  count <- count + 1
  if(x$is_location_exact[i]=="f"){x$zip_precise[i] <- FALSE}
  long <- x$longitude[i]
  lat <- x$latitude[i]
  cat(paste("long:", long, " lat:", lat, "\n"))
  res <- revgeocode(c(long, lat), output="address")
  zipcode <- substr(res,gregexpr(pattern =state,res)[[1]][1]+3,gregexpr(pattern =state,res)[[1]][1]+7)
  cat(paste("zipcode:", zipcode, "\n=======================================================\n"))
  x$zipcode[i] <- zipcode
}
dta$zip_precise <- x$zip_precise
#calculate density and avg_price based on neigborhood
dta$neighborhood <- data$neighbourhood_cleansed
freq_neighborhood <- as.data.frame(table(data$neighbourhood_cleansed))
avg_price_neighborhood <- aggregate(dta$price, list(dta$neighborhood), mean)
freq_price <- merge(x=freq_neighborhood, y=avg_price_neighborhood, by.x="Var1", by.y="Group.1")
temp <- merge(x=dta, y=freq_price, by.x="neighborhood", by.y="Var1", all.x = TRUE)
temp <- temp[order(temp$id),]
dta$density_nbh <- temp$Freq
dta$avg_price_nbh <- temp$x
dta$neighborhood <- NULL
rm(freq_neighborhood, avg_price_neighborhood, freq_price, temp)
#calculate density and avg_price based on zipcode
data$neighbourhood_cleansed <- x$zipcode
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
rm(a,x,count,i,lat,long,res,zipcode,state)
############################################################################
### city
############################################################################
dta$city <- filename
which(is.na(dta))
result <- rbind(result, dta)
save(result,file="/home/poom/Desktop/airbnb/final_data.Rda")
load("C:/Users/ThisPC/Desktop/dissertation/cognitive load/info_overload_cross-sectional/final_data.Rda")
############################################################################
############################################################################

dta <- result
library(varhandle)
binary_city <- to.dummy(dta$city, "city")
dta <- cbind(dta, binary_city)

#some listing show 0 host_listings_count (effect should be u-shape, both ends have better performance)
#there are 0 bathrooms, bedrooms, beds 
#x <- dta[-which(dta$host_listings_count==0 | dta$bathrooms==0 | dta$bedrooms==0 | dta$beds==0), ]
x <- dta[-which(dta$host_listings_count==0), ]
est <- lm(logit_perf ~  host_is_superhost + density_nbh + host_is_superhost*density_nbh, data=x)
est <- lm(logit_perf ~ host_is_superhost + density_nbh + host_is_superhost*density_nbh
          
          +host_listings_count
          
          #number_of_reviews becomes insig if interact with review_scores_rating
          +review_scores_location+number_of_reviews
          
          +price+bathrooms+bedrooms
          +beds+tv+wifi+ac+fridge+toiletry+accommodates
          
          
          # #if include, superhost will not be sig (cor=0.18,0.11,0.1,0.33)
          # #1) Host a minimum of 10 stays in a year
          # #2) Respond to guests quickly and maintain a 90% response rate or higher
          # #3) Have at least 80% 5-star reviews
          # #4) Honor confirmed reservations (meaning hosts should rarely cancel)
          # +host_response_rate+membership+host_identity_verified+review_scores_rating
          # 
          # #if control for city, density becomes positive
          # +city.asheville_nc+city.austin_tx+city.boston_ma+city.browardcounty_fl+city.cambridge_ma+
          # city.chicago_il+city.clarkcounty_nv+city.columbus_oh+city.denver_co+city.hawaii_hi+city.jerseycity_nj+
          # city.losangeles_ca+city.nashville_tn+city.neworleans_la+city.newyorkcity_ny+city.oakland_ca+
          # city.pacificgrove_ca+city.portland_or+city.rhodeisland_ri+city.salem_or+city.sandiego_ca+
          # city.sanfrancisco_ca+city.santaclaracounty_ca+city.santacruzcounty_ca+city.seattle_wa+
          # city.twincitiesmsa_mn+city.washington_dc
          
          , data=x)
summary(est)
#fix heteroskedasticity
library(sandwich)
coeftest(est, type="HC3")
#get F-test
waldtest(est, vcov=vcovHC)

temp=x[,5:27]
temp$city <- NULL
cor(temp)
install.packages("corrplot")
library(corrplot)
corrplot(cor(temp))

library(psych)
describe(x)
library(sjPlot)
library(sjmisc)
library(sjlabelled)
tab_model(
  est, show.se = TRUE, show.std = TRUE, show.stat = TRUE,
  col.order = c("p", "stat", "est", "std.se", "se", "std.est")
)

############################################################################
### export to spss for multi-level
############################################################################
setwd("D:/PhD/Dissertation/airbnb/cognitive load/1-cross_section/airbnb_data/")
filename = list.files(pattern="*.csv")
library(dplyr)
library(plyr)
readdata <- function(filename) {
  df <- read.csv(filename)
  df$neighbourhood_cleansed <- as.character(df$neighbourhood_cleansed)
  df <- select(df, id, neighbourhood_cleansed)
  df$city <- filename
  return(df)
}
nhb <- do.call(rbind.fill, lapply(filename, readdata))
nhb$city <- gsub("\\..*", "", nhb$city)

nhb$key <- paste(nhb$id, nhb$city)
result$key <- paste(result$id, result$city)
temp <- merge(result, nhb, by.x ="key", by.y="key", all.x=TRUE)

temp$cities <- gsub("_.*$", "", temp$city.x)
temp$states <- gsub(".*_", "", temp$city.x)
keeps <- c("id.x", "logit_perf", "host_is_superhost", "density_nbh", "host_listings_count", "number_of_reviews",
           "price", "bathrooms", "bedrooms", "beds", "tv", "wifi", "ac", "fridge", "toiletry", "accommodates",
           "cities", "states", "neighbourhood_cleansed")
temp <- temp[keeps]
library(haven)
write_sav(temp, "C:/Users/ThisPC/Desktop/spss_dat.sav")

#neighbourhood
library(haven)
dta = read_sav("D:/PhD/Dissertation/airbnb/cognitive load/1-cross_section/spss_dat.sav")

dta[which(dta$states=="ca"), 'neighbourhood_cleansed']
t.first <- dta[match(unique(dta$cities), dta$cities),]
dta <- within(dta, { count <- ave(neighbourhood_cleansed, cities, FUN=function(x) length(unique(x)))})
freq <- dta[match(unique(dta$cities), dta$cities),]

###########################################################################################
# check regression assumption
###########################################################################################
# library(dplyr)
# library("lavaan")
library(MASS)
library(car)
library(lmtest)
library(caret)
library(mctest)

model <- est
# Linearity of the data
plot(model, which=1) #The red line should straight and horizontal, not curved
crPlots(model) #Both red & green lines should be nice and linear
# Outliers
plot(model, 5) #data shouldnt cross Cook’s distance line
plot(model, 4) #red line should be flat and horizontal with equally and randomly spread data points
outlierTest(model) #sig=outlier exists
# The mean of residuals is zero
mean(model$residuals) #should be zero (or very close)
# Normality of residuals
plot(model, 2) #observations should lie well along the 45-degree line
sresid <- studres(model) 
hist(sresid, freq=FALSE)
xfit <- seq(min(sresid),max(sresid),length=40) 
yfit <- dnorm(xfit) 
lines(xfit, yfit)
shapiro.test(sresid) #sig=non-normal
# Homoscedasticity
plot(model, 3) #red line should be flat and horizontal with equally and randomly spread data points
ncvTest(model) #sig=hetero
bptest(model) #sig=hetero
# Independence (Autocorrelation)
durbinWatsonTest(model) #sig=auto
# Multicollinearity 
var_col <- dta[,c('self_esteem','brand_love','social_compare','distance','se_x_sc','se_x_sd')]
corr <- round(cor(var_col),2)
findCorrelation(corr, cutoff = 0.7, names = TRUE)
vif(model) #>10 is not good (actually it depends on how much it inflates)
omcdiag(as.matrix(var_col), dta$brand_jealous)
imcdiag(var_col, dta$brand_jealous)
# The X variables and residuals are uncorrelated
cor.test(x$host_is_superhost, model$residuals) #sig=correlated

###########################################################################################
# prediction
###########################################################################################
library(caret)
library(LaplacesDemon)
library("ggplot2")
transform_to_num_booked_days <- function(logit) {
  percent <- invlogit(logit)
  num_booked_days <- percent*30
  return(num_booked_days)
}

sampling <- x
sampling$sampling <- "a"
trainIndex <- createDataPartition(sampling$sampling, p=2/3, list=FALSE)
train <- sampling[trainIndex,]
test <- sampling[-trainIndex,]
est <- lm(logit_perf ~ host_is_superhost + density_nbh + host_is_superhost*density_nbh
          +host_listings_count
          +review_scores_location+number_of_reviews
          +price+bathrooms+bedrooms
          , data=train)
summary(est)
yhat <- predict(est, newdata=test, interval="prediction")
yhat <- as.data.frame(yhat)
yhat$actual <- test$logit_perf
# yhat$fit = transform_to_num_booked_days(yhat$fit)
# yhat$lwr = transform_to_num_booked_days(yhat$lwr)
# yhat$upr = transform_to_num_booked_days(yhat$upr)
# yhat$actual = transform_to_num_booked_days(yhat$actual)
yhat <- yhat[order(yhat$actual), ]
rownames(yhat)=NULL
yhat$idu <- as.numeric(row.names(yhat))
p <- ggplot(yhat, aes(x=idu, y=actual)) +
  geom_point() +
  geom_line(aes(y=fit), color="blue") +
  geom_line(aes(y=lwr), color="red", linetype="dashed") +
  geom_line(aes(y=upr), color="red", linetype="dashed")
p
sum((yhat$actual<yhat$upr & yhat$actual>yhat$lwr), na.rm = TRUE)/nrow(yhat)

temp = yhat
yhat = temp[4500:5000,]
