# DrawStats
A collection of scripts that do some analysis and make some plots showing the results

From each script, the output plots go into the folder `plots`. The main plots will stay in the appropriate top level folder, and other plots you might find helpful go into `extras`
The main plots include important indicators, as well as the values they should be compared to.

All scripts process data from all three competitions by default


## Quick Start Guide

1. If you do not have a python environment manager already installed, [install Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) on your personal computer. 

2. Launch Miniconda by searching for Miniconda in the Windows search bar, and select the item "Ananaconda Prompt (Miniconda 3)" which will give you a terminal. Navigate to the folder you want to work in.

3. In a folder on your computer, clone this git repository: `git clone https://github.com/lesyahoryn/DrawStats.git`

4. Set up the DrawStats conda environment by running `conda env create --name DrawStats -f environment.yml`. `environment.yml` comes from this git repository. You can replace `DrawStats` with any name you'd like to call your environment.

5. Activate the environment by running `conda activate DrawStats`. You will need to do this every time you open a new terminal (as in step 2). Where it previously said `(base)` should now say `(DrawStats)`. 

6. Run any of the scripts in the git repo. 

If you want edit code in a nice environment, I recommend [installing VSCode](https://code.visualstudio.com/download)

## Run Everything
To run all the scripts for each provider, simply run `runAll.bat` in your conda terminal.

It will make an output folder called `plots`. Inside of `plots` there is a folder for each competition, which contains the main results, as well as a folder called `extras` that contains auxiliary plots from each script that might be helpful if you see an issue in one of the main results, or are curious about things like country/pot correlations.


## Code details

### Home/Away Analysis
The first set of scripts studies if the home/away assignment is consistent with a fair draw. 

#### probability_plots.py
Usage: `python probability_plots.py --provider [AE, Asolvo, or Pseudodata]` 
Main output: 
  * `HA_prob_normalized.png` which shows the number of times team A plays at home, normalized to 100. 

#### binomial_test.py
Usage: `python probability_plots.py --provider [AE, Asolvo, or Pseudodata]` 
Main output: 
  * `pvalues_0to0p1.png` which shows us the number of pairings with pvalue from the binomial test less than 0.05. We expect this number to be about 5% of the total number of pairings.

### Team Pairing Analysis

#### ASAEcomparison.py
Usage `python ASAEcomparison.py` 
Main output:
  *  `percent_difference.png` shows the percent difference between AE and Asolvo dataset per pairing
  *  `difference_per_matchup_2D.png` shows the absolute difference between AE and Asolvo per pairing. Any large differences are highlighted with red text
  * `difference_allowedPairings_2D.png` shows a comparison of which pairings are/are not allowed in each dataset
  * `teamCheck.png` shows the result of a check between the teams and their order between the two datasets

#### compute_probabilities.py
Usage `python compute_probabilities.py `
Main output:
  *  `percent_difference_prob-AE.png` and `percent_difference_prob-AS.png` show the percent difference between draw results and computed probability on the population of team pairings.
  * `2D_percent_difference_prob-AE.png` and `2D_percent_difference_prob-AS.png` shows the percent difference between draw results and computed probability per team pairing.
