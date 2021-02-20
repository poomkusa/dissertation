* Conditional Logit Model in Stata
* Copyright 2013 by Ani Katchova

clear all
set more off

use "D:\PhD\Dissertation\airbnb\cultural distance\choice model\Lido\data.dta"

* Dependent variable is 1 or 0 whether the alternative is selected or not
* xlist is case-specific regressors and zlist is alternative-specific regressors
global ylist listing_id
global zlist sh sh_x_dst

global id chid
global alternative alt

describe $id $alternative $ylist $zlist 
summarize $id $alternative $ylist $zlist

* Conditional logit model with base outcome set as basealternative1
asclogit $ylist $zlist, case($id) alternatives($alternative)

===================================================================================
* Conditional logit marginal effects
estat mfx, varlist($xlist $zlist)

* Conditional logit predicted probabilities
predict pasclogit, pr
summarize pasclogit
tabulate $ylist

* Multinomial logit is conditional logit with no alternative-specific variables
asclogit $ylist, case($id) alternatives($alternative) casevar($xlist)

===================================================================================
global ylist listing_id
global xlist sh_x_dst
global rand sh 
 
global id reviewer_id
global group chid

describe $id $ylist $xlist  
summarize $id $ylist $xlist

* Mixed logit or random-parameters logit model
mixlogit $ylist $xlist, group ($group) id($id) rand($rand) 

=================================================================================== 
cmset chid alt
cmclogit listing_id sh sh_x_dst



list reviewer_id period alt listing_id in 1/12, sepby(period ) noobs

gen t = real(period)
cmset reviewer_id t alt
cmxtmixlogit listing_id, random(sh sh_x_dst) nolog











