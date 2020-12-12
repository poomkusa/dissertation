library(dplyr)
library(feather)
library("lme4")

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

review_dta$vader_sent <- ifelse(review_dta$compound>=0.05, 1, NA)
review_dta$vader_sent <- ifelse(review_dta$compound<=-0.05, 0, review_dta$vader_sent)
review_dta$bayes_dummy <- review_dta$bayes_class == "pos"
review_dta$bayes_dummy <- as.numeric(review_dta$bayes_dummy)

#warning explanation: https://rstudio-pubs-static.s3.amazonaws.com/33653_57fc7b8e5d484c909b615d8633c01d51.html
m1 <- glmer(vader_sent ~ individualism*review_scores_accuracy
            + power_distance + masculinity + uncertainty_avoidance + LT_orientation + indulgence
            + (1| listing_id)
            , data = review_dta, family = binomial)
summary(m1)
saveRDS(m1, "D:/PhD/Dissertation/airbnb/cultural distance/mixed effect logistic reg/m1.rds")
my_model <- readRDS("D:/PhD/Dissertation/airbnb/cultural distance/mixed effect logistic reg/m1.rds")

#################################################################################
# multi-level modeling sample
#################################################################################
library(mlmRev)
#standLRT - individual level
#schavg  - group level

#null model
lmer(normexam ~ 1 + (1 | school), data=Exam)

#random intercept, fixed predictor in individual level
lmer(normexam ~ standLRT + (1 | school), data=Exam)

#random intercept, random slope
lmer(normexam ~ standLRT + (standLRT | school), data=Exam, method='ML')

#random intercept, individual and group level predictor
lmer(normexam ~ standLRT + schavg + (1 + standLRT | school), data=Exam)

#random intercept, cross-level interaction
lmer(normexam ~ standLRT * schavg + (1 + standLRT | school), data=Exam)
