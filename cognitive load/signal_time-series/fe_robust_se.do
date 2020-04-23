*set cross-section and ts variable
xtset id timevar
xtdescribe

*run two-way fe
xtreg logit_perf host_is_superhost superhostxnum_reviews host_listings_count review_scores_location number_of_reviews price bathrooms bedrooms i.timevar, fe
*check for heteroskedasticity (sig=hetero)
xttest3
*check for cross-sectional dependence (sig=dependence)
xttest2
xtcsd, pesaran abs
xtcsd, frees
xtcsd, friedman
*check for serial correlation (sig=there is)
xtserial logit_perf host_is_superhost superhostxnum_reviews host_listings_count review_scores_location number_of_reviews price bathrooms bedrooms, output

*Driscoll-Kraay SE
xtscc logit_perf host_is_superhost superhostxnum_reviews host_listings_count review_scores_location number_of_reviews price bathrooms bedrooms i.timevar, fe
*Rogers or clustered SE
xtreg logit_perf host_is_superhost superhostxnum_reviews host_listings_count review_scores_location number_of_reviews price bathrooms bedrooms i.timevar, fe cluster()