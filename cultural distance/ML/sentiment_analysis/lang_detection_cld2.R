library(dplyr)
library(cld2)

data <- select(read.csv(file="D:/PhD/Dissertation/airbnb/cultural distance/raw data/venice_reviews.csv"), 
               comments)
data$comments <- as.character(data$comments)
data$cld2 <- detect_language(data$comments)

#det?ct_language("??????????????????????????????", plain_text = TRUE, lang_code = TRUE)
#test = head(data)
#test$cld2 <- detect_language(test$comments)