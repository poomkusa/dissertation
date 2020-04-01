setwd("/home/poom/Desktop/thammasat/2y1s/DB864 Contemporary Empirical Research in Marketing II/term paper/airbnb/study2/airbnb_data/")
filename = list.files(pattern="*.csv")
library(dplyr)
readdata <- function(filename) {
  df <- select(read.csv(filename), id)
  return(df)
}
for (i in 1:length(filename)){
  assign(filename[i], readdata(filename[i]))
}
#rbind into 1 big df
result <- do.call(rbind, lapply(filenames, readdata))