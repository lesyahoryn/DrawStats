# DrawStats
A collection of scripts that do some analysis and make some plots showing the results

From each script, the output plots go into the folder `plots`. The main plots will stay in the appropriate top level folder, and other plots you might find helpful go into `extras`
The main plots include important indicators, as well as the values they should be compared to.

## Home/Away Analysis
The first set of scripts studies if the home/away assignment is consistent with a fair draw. 

### probability_plots.py
Usage: `python probability_plots.py --provider [AE, Asolvo, or Pseudodata]` 
Main output: 
  * `HA_prob_normalized.png` which shows the number of times team A plays at home, normalized to 100. 

### binomial_test.py
Usage: `python probability_plots.py --provider [AE, Asolvo, or Pseudodata]` 
Main output: 
  * `pvalues_0to0p1.png` which shows us the number of pairings with pvalue from the binomial test less than 0.05. We expect this number to be about 5% of the total number of pairings.

## Team Pairing Analysis

### ASAEcomparison.py
Usage `python ASAEcomparison.py` 
Main output:
  *  `percent_difference.png` shows the percent difference between AE and Asolvo dataset per pairing
  *  `difference_per_matchup_2D.png` shows the absolute difference between AE and Asolvo per pairing. Any large differences are highlighted with red text
