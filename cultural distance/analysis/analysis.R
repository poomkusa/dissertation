library(dplyr)
library(feather)
# library(MASS)
# library(car)
# library(lmtest)
# library(caret)
# library(mctest)

listing_dta <- read_feather("D:/PhD/Dissertation/airbnb/cultural distance/listing.feather")
review_dta <- read_feather("D:/PhD/Dissertation/airbnb/cultural distance/review_long.feather")
#remove rows with translated comments
# review_dta <- review_dta[(review_dta$comments==review_dta$translation),]
# review_dta$gender <- ifelse(review_dta$gender=='Male', TRUE, review_dta$gender)
# review_dta$gender <- ifelse(review_dta$gender=='Female', FALSE, review_dta$gender)
# library(foreign)
# review_dta <- subset(review_dta, select=-c(comments,translation,pic))
# write.dta(review_dta, "C:/Users/ThisPC/Desktop/mydata.dta")
summary(review_dta)
#replace null with nan
sapply(review_dta, is.null)
#replace "" with nan
which(review_dta == "")
review_dta[listing_dta == ""] <- NA

#################################################################################
# listing level
#################################################################################
#remove middle distance
# mean <- mean(listing_dta$cult_dst_6)
# sd <- sd(listing_dta$cult_dst_6)
# listing_dta$dst <- NA
# listing_dta$dst <- ifelse(listing_dta$cult_dst_6<(mean-(0.25*sd)) | listing_dta$cult_dst_6 > (mean+(0.25*sd)),
#                           listing_dta$cult_dst_6, listing_dta$dst)
#transform distance to dummy
# listing_dta$dstH <- NA
# listing_dta$dstH <- ifelse(listing_dta$cult_dst_6 > (mean+(0.25*sd)), TRUE, listing_dta$dstH)
# listing_dta$dstH <- ifelse(listing_dta$cult_dst_6 < (mean-(0.25*sd)), FALSE, listing_dta$dstH)
# listing_dta$host_x_dst <- listing_dta$host_is_superhost*listing_dta$cult_dst_6
# listing_dta$host_x_dst_x_age <- listing_dta$host_is_superhost*listing_dta$cult_dst_6*listing_dta$age
listing_dta$dst <- abs(listing_dta$uncertainty_avoidance-75) #italy UAI=75
listing_dta$host_x_dst <- listing_dta$host_is_superhost*listing_dta$dst
#reg (can remove age if also remove dst)
est <- lm(logit_perf ~ host_is_superhost + dst + host_x_dst
          # + gc_dst
          + age
          + host_listings_count + number_of_reviews + price + bathrooms + bedrooms + review_scores_location
          , data=listing_dta, na.action=na.omit)
summary(est)

#fix heteroskedasticity
library(sandwich)
coeftest(est, type="HC0")
#get F-test
waldtest(est, vcov=vcovHC)

#################################################################################
# review level
#################################################################################
#dv = rating distance
temp <- aggregate(select(review_dta, compound), list(review_dta$listing_id), mean, na.rm=TRUE)
temp <- rename(temp, avg_sentiment=compound)
review_dta <- merge(x=review_dta, y=temp, by.x="listing_id", by.y="Group.1", all.x = TRUE)
review_dta$rating_dst <- abs(review_dta$compound.x - review_dta$compound.y)
est <- lm(rating_dst ~ power_distance + individualism + masculinity + uncertainty_avoidance
          + LT_orientation + indulgence
          + dst + gc_dst + age + gender
          + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
          + review_scores_location + review_scores_rating + review_scores_value
          + individualism:number_of_reviews
          , data=review_dta, na.action=na.omit)
summary(est)

#dv = subjectivity
review_dta$vader_subj <- ifelse( (review_dta$compound>=0.05) | (review_dta$compound<=-0.05), 1, NA)
review_dta$vader_subj <- ifelse( (review_dta$compound>-0.05) & (review_dta$compound<0.05)
                                 , 0, review_dta$vader_subj)
library("bife")
mod_1 <- bife(vader_subj ~ power_distance + individualism + masculinity + uncertainty_avoidance
              + LT_orientation + indulgence
              + gc_dst + age + gender
              | listing_id, data=review_dta, bias_corr="no")
summary(mod_1)
#use logistic regression
# est <- glm(vader_subj ~ power_distance + individualism + masculinity + uncertainty_avoidance
#            + LT_orientation + indulgence
#            + dst + gc_dst + age + gender
#            + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#            + review_scores_location + review_scores_rating + review_scores_value
#            , data=review_dta, na.action=na.omit, family='binomial')
# summary(est)
#use linear regression
# review_dta$vader_subj2 <- abs(review_dta$compound)
# est <- lm(vader_subj2 ~ power_distance + individualism + masculinity + uncertainty_avoidance
#           + LT_orientation + indulgence
#           + dst + gc_dst + age + gender
#           + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#           + review_scores_location + review_scores_rating + review_scores_value
#           , data=review_dta, na.action=na.omit)
# summary(est)

#dv = sentiment
review_dta$dst <- abs(review_dta$uncertainty_avoidance-75)
#-----
review_dta$vader_sent <- ifelse(review_dta$compound>=0.05, 1, NA)
review_dta$vader_sent <- ifelse(review_dta$compound<=-0.05, 0, review_dta$vader_sent)
#-----
# review_dta$sent_sign <- ifelse(review_dta$rating_dst > 0, 'pos', NA)
# review_dta$sent_sign <- ifelse(review_dta$rating_dst < 0, 'neg', review_dta$rating_dst_sign)
#-----
# review_dta$bayes_dummy <- review_dta$bayes_class == "pos"
# review_dta$bayes_dummy <- as.numeric(review_dta$bayes_dummy)
#-----
# temp <- aggregate(select(review_dta, compound), list(review_dta$listing_id), sd, na.rm=TRUE) #abiguity
# temp <- rename(temp, sd_sentiment=compound)
# review_dta <- merge(x=review_dta, y=temp, by.x="listing_id", by.y="Group.1", all.x = TRUE)
#-----
# review_dta$word_count <- sapply(review_dta$translation, function(x) wordcount(x))
#-----
library("bife") #https://cran.r-project.org/web/packages/bife/vignettes/howto.html
mod_1 <- bife(vader_sent ~ power_distance + individualism + masculinity + uncertainty_avoidance
              + LT_orientation + indulgence
              # + gc_dst
              # + gender
              # + review_scores_rating + individualism:review_scores_rating
              + review_scores_accuracy + individualism:review_scores_accuracy
              # + sd_sentiment + individualism:sd_sentiment
              # + LT_orientation:gc_dst
              # + age + power_distance:age
              # + price + power_distance:price
              | listing_id, data=review_dta)
              # | listing_id, data=review_dta, bias_corr="no")
summary(mod_1)

#use glmm
# library("lme4")
# m1 <- glmer(vader_sent ~ power_distance + individualism + masculinity + uncertainty_avoidance
#             + LT_orientation + indulgence
#             + dst + gc_dst + age + gender
#             + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#             + review_scores_location
#             # + review_scores_rating + individualism:review_scores_rating
#             # + review_scores_accuracy + individualism:review_scores_accuracy
#             # + LT_orientation:gc_dst
#             # + power_distance:age
#             # + power_distance:price
#             + (1 | listing_id)
#             + (1 | country)
#             , data = review_dta, family = binomial, nAGQ = 1)
# summary(m1)
#use ordinal logistic regression
# review_dta$vader_ordered <- ifelse(review_dta$compound>=0.05, 'pos', NA)
# review_dta$vader_ordered <- ifelse(review_dta$compound<=-0.05, 'neg', review_dta$vader_ordered)
# review_dta$vader_ordered <- ifelse( (review_dta$compound>-0.05) & (review_dta$compound<0.05), 'neu',
#                                     review_dta$vader_ordered)
# review_dta$vader_ordered <- ordered(review_dta$vader_ordered, levels = c("pos", "neu", "neg"))
# review_dta = as.matrix(review_dta)
# m <- polr(vader_ordered ~ power_distance + individualism + masculinity + uncertainty_avoidance
#           + LT_orientation + indulgence
#           + dst + gc_dst + age + gender
#           + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#           + review_scores_location + review_scores_rating + review_scores_value
#           + individualism:review_scores_rating
#           #+ individualism:review_scores_accuracy
#           # + LT_orientation:gc_dst
#           # + power_distance:age
#           , data = review_dta, Hess=TRUE)
# summary(m)
#use logistic regression
# est <- glm(vader_sent ~ power_distance + individualism + masculinity + uncertainty_avoidance
#            + LT_orientation + indulgence
#            + dst + gc_dst + age + gender
#            + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#            + review_scores_location + review_scores_rating + review_scores_value
#            + individualism:review_scores_rating
#            + LT_orientation:gc_dst
#            + power_distance:age
#           , data=review_dta, na.action=na.omit, family='binomial')
# summary(est)
#use linear regression
# est <- lm(compound ~ power_distance + individualism + masculinity + uncertainty_avoidance
#           + LT_orientation + indulgence
#           + dst + gc_dst + age + gender
#           + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#           + review_scores_location + review_scores_rating + review_scores_value
#           + power_distance:price
#           , data=review_dta, na.action=na.omit)
# summary(est)
#use fixed effect logistic regression
# library(survival)
# fe <- clogit(vader_sent ~ power_distance + individualism + masculinity + uncertainty_avoidance
#              + LT_orientation + indulgence
#              + dst + gc_dst + age + gender
#              + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#              + review_scores_location
#              + strata(listing_id)
#              + individualism:number_of_reviews + power_distance:price
#              , data=review_dta, na.action=na.omit)
# library(plm)
# fixed <-plm(compound ~ power_distance + individualism + masculinity + uncertainty_avoidance
#             + LT_orientation + indulgence
#             + dst + gc_dst + age + gender
#             + host_is_superhost + host_listings_count + number_of_reviews + price + bathrooms + bedrooms
#             + review_scores_location
#             + strata(listing_id)
#             + individualism:number_of_reviews + power_distance:price 
#             , data=review_dta, na.action=na.omit, index=c("listing_id"), model="within")

#################################################################################
# test sentiment prediction performance
#################################################################################
pos <- review_dta[review_dta$vader_sent == 1, ]
neg <- review_dta[review_dta$vader_sent == 0, ]
t.test(pos$review_scores_rating, neg$review_scores_rating)

#################################################################################
# reg assumption test
#################################################################################
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
