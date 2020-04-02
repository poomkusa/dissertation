library(dplyr)
library(cld2)

data <- select(read.csv(file="/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/raw data/venice_reviews.csv"), 
               comments)
data$comments <- as.character(data$comments)
data$cld2 <- detect_language(data$comments, plain_text = TRUE, lang_code = TRUE)
write.csv(data, "/home/poom/Desktop/PhD/Dissertation/airbnb/cultural distance/ML/nlp/cld2.csv", row.names = FALSE)

# detect_language("This is a test.", plain_text = TRUE, lang_code = TRUE)
# test = head(data)
# test$cld2 <- detect_language(test$comments, plain_text = TRUE, lang_code = TRUE)
