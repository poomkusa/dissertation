# library(dplyr)
# library("lavaan")
library(feather)
library(MASS)
library(car)
library(lmtest)
library(caret)
library(mctest)

listing_dta <- read_feather("D:/PhD/Dissertation/airbnb/cultural distance/listing.feather")
review_dta <- read_feather("D:/PhD/Dissertation/airbnb/cultural distance/review.feather")
summary(review_dta)
#replace null with nan
sapply(review_dta, is.null)
#replace "" with nan
which(review_dta == "")
review_dta[listing_dta == ""] <- NA

#################################################################################
# listing level
#################################################################################
#cultural value
# listing_dta$host_x_idv <- listing_dta$host_is_superhost*listing_dta$individualism
# listing_dta$host_x_uai <- listing_dta$host_is_superhost*listing_dta$uncertainty_avoidance
#cultural distance
# mean <- mean(listing_dta$cult_dst_6)
# sd <- sd(listing_dta$cult_dst_6)
# listing_dta$dst <- NA
# listing_dta$dst <- ifelse(listing_dta$cult_dst_6<(mean-(0.25*sd)) | listing_dta$cult_dst_6 > (mean+(0.25*sd)),
#                           listing_dta$cult_dst_6, listing_dta$dst)
# listing_dta$dstH <- NA
# listing_dta$dstH <- ifelse(listing_dta$cult_dst_6 > (mean+(0.25*sd)), TRUE, listing_dta$dstH)
# listing_dta$dstH <- ifelse(listing_dta$cult_dst_6 < (mean-(0.25*sd)), FALSE, listing_dta$dstH)
# listing_dta$host_x_dst <- listing_dta$host_is_superhost*listing_dta$dst
# listing_dta$host_x_dst_x_age <- listing_dta$host_is_superhost*listing_dta$cult_dst_6*listing_dta$age
listing_dta$dst <- abs(listing_dta$uncertainty_avoidance-75)
listing_dta$dst <- ifelse(listing_dta$dst < 0, TRUE, FALSE)
listing_dta$host_x_dst <- listing_dta$host_is_superhost*listing_dta$dst
#reg
est <- lm(logit_perf ~ host_is_superhost + dst + host_x_dst
          + gc_dst
          + age
          + host_listings_count + number_of_reviews + price + bathrooms + bedrooms + review_scores_location
          , data=listing_dta, na.action=na.omit)
summary(est)
# est <- lm(logit_perf ~ host_is_superhost + individualism + host_x_idv
#           #+ uncertainty_avoidance + host_x_uai
#           + gc_dst
#           + age
#           + host_listings_count + number_of_reviews + price + bathrooms + bedrooms + review_scores_location
#           , data=listing_dta, na.action=na.omit)
# summary(est)

#fix heteroskedasticity
library(sandwich)
coeftest(est, type="HC0")
#get F-test
waldtest(est, vcov=vcovHC)

#################################################################################
# review level
#################################################################################
est <- lm(sentiment_pl ~ host_is_superhost + cult_dst_6 #+ host_is_superhost:cult_dst_6
          + gc_dst + age + gender
          + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
          + review_scores_location
          , data=review_dta, na.action=na.omit)
summary(est)
review_dta$bayes_dummy <- review_dta$bayes_class == "pos"
review_dta$bayes_dummy <- as.numeric(review_dta$bayes_dummy)
est <- glm(bayes_dummy ~ host_is_superhost + cult_dst_6 #+ host_is_superhost:cult_dst_6
          + gc_dst + age + gender
          + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
          + review_scores_location
          , data=review_dta, na.action=na.omit, family='binomial')
summary(est)

#reg assumption test
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
car::vif(model)
var_col <- dta[,c('self_esteem','brand_love','social_compare','distance','se_x_sc','se_x_sd')]
corr <- round(cor(var_col),2)
findCorrelation(corr, cutoff = 0.7, names = TRUE)
vif(model) #>10 is not good (actually it depends on how much it inflates)
omcdiag(as.matrix(var_col), dta$brand_jealous)
imcdiag(var_col, dta$brand_jealous)
# The X variables and residuals are uncorrelated
cor.test(x$host_is_superhost, model$residuals) #sig=correlated
