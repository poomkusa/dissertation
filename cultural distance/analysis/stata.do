*create gender dummy
label define gender 1 "TRUE" 2 "FALSE"
encode gender, label(gender) gen(gender_c)
replace gender_c = . if !inlist(gender_c, 1, 2)

*conidtional fixed effect logit
clogit vader_sent power_distance individualism masculinity uncertainty_avoidance LT_orientation indulgence dst gc_dst age i.gender_c, group(listing_id)

*unconidtional fixed effect logit
logit vader_sent power_distance individualism masculinity uncertainty_avoidance LT_orientation indulgence dst gc_dst age i.gender_c i.host_is_superhost host_listings_count number_of_reviews price bathrooms bedrooms review_scores_location review_scores_rating review_scores_value i.listing_id