library(dplyr)
data <- select(read.csv(file="/media/poom/Backup/PhD/Dissertation/airbnb/cultural distance/venice_reviews.csv"), 
               reviewer_id)
write.csv(dta, "/home/poom/Desktop/reviewer_id.csv", row.names = FALSE)
