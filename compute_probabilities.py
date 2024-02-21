import numpy as np
import argparse
import sys
import os
from draw_stats_helpers import * 

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

competition = 'UEL'
n_simulations = 50 #in thousands, bc of my naming convention

data = getData('Data/AE/{}-{}k.csv'.format(competition, n_simulations))


clubs = set_club_countries_pots(competition)
npots, nteamsperpot = getNPots_TeamsPerPot(competition)


savePath_main = 'plots/matchupComparison/{}/'.format(competition)
savePath_extra = 'plots/matchupComparison/{}/extra/'.format(competition)

if not os.path.exists(savePath_main):
    os.makedirs(savePath_main)
if not os.path.exists(savePath_extra):
    os.makedirs(savePath_extra)


## I need to do this per pot because there is 100% chance to play at home per pot
## Really there is a 200% chance to play against any team, but I don't care about home vs away, so I am only looking at home
## I guess I should compare what happens if i compute this for the rows or for the columns.. but i think I don't care
## I then want to fill in the overall array so that i can plot it, but that is step two 

pot_probs = {}
probability_matrix = np.zeros(( data.shape[0], data.shape[1] )) # where we will store the output 
prob_scaling_factor = n_simulations*1000 #total number that each row/col should sum up to 
#prob_scaling_factor = 100

for pot1 in range( 1, npots+1 ):

    for pot2 in range( 1, npots+1 ):


        ## start and end index of my pot in matrix
        start1 = (pot1-1) * nteamsperpot
        end1 =    pot1    * nteamsperpot
        start2 = (pot2-1) * nteamsperpot
        end2 =    pot2    * nteamsperpot

        # grab the data from only the pot i am working with , for now symmetric but we will come back to that
        sub_matrix = data[start1:end1, start2:end2]

        ##replace all nonzero elements with 1 because I want to be computing the probability, not just taking what is there
        sub_matrix = np.where( sub_matrix !=0, 1, sub_matrix)

        print("\n\nworking with pot", pot1, pot2)
        
        #compute sums per row and per col, as we know that these are our 100%
        row_sums = np.sum(sub_matrix, axis=1)
        col_sums = np.sum(sub_matrix, axis=0)  

        # Normalize the probabilities
        #normalized_matrix = sub_matrix / row_sums
        probabilities_normalized = (sub_matrix * prob_scaling_factor / col_sums) * (sub_matrix * prob_scaling_factor / row_sums[:, np.newaxis])

        ## store in full data struct
        probability_matrix[ start1:end1, start2:end2  ] = probabilities_normalized

make2DTeamPlot(probability_matrix, list(clubs.keys()), "False", savePath_main+"apriori_probs.png", competition, cbarLabel="probability", clim=[np.min( probability_matrix[probability_matrix !=0] ) , np.max(probability_matrix)], redTxtPrec='.1f', fontsize=8)
plt.close()



