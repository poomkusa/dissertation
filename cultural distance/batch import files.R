# library(dplyr)
# library("lavaan")
library(feather)
library(MASS)
library(car)
library(lmtest)
library(caret)
library(mctest)

dta <- read_feather("/home/poom/Desktop/dta.feather")
summary(dta)

#listing level
est <- lm(logit_perf ~ host_is_superhost + cult_dst_6 #+ host_is_superhost:cult_dst_6
          #+ gc_dst + sentiment_pl + sentiment_sj
          + host_listings_count + number_of_reviews + price + bathrooms + bedrooms + review_scores_location
          , data=dta)
summary(est)
#fix heteroskedasticity
library(sandwich)
coeftest(est, type="HC0")
#get F-test
waldtest(est, vcov=vcovHC)

#review level


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
var_col <- dta[,c('self_esteem','brand_love','social_compare','distance','se_x_sc','se_x_sd')]
corr <- round(cor(var_col),2)
findCorrelation(corr, cutoff = 0.7, names = TRUE)
vif(model) #>10 is not good (actually it depends on how much it inflates)
omcdiag(as.matrix(var_col), dta$brand_jealous)
imcdiag(var_col, dta$brand_jealous)
# The X variables and residuals are uncorrelated
cor.test(x$host_is_superhost, model$residuals) #sig=correlated
