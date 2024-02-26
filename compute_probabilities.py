import numpy as np
import argparse
import sys
import os
from draw_stats_helpers import * 

init()

competition = 'UEL'
competitions = ['UCL', 'UEL', 'UECL']
#competitions = ['UECL']
n_simulations = 50 #in thousands, bc of my naming convention

## Compute, per pot, the probability of playing other teams
## I need to do this per pot, because there is a 100% chance of playing at home and 100% chance of playing away per pot
## Here, I take the data from AE, just to get the constraints, and replace all the values with 1 (and disallowed pairings still have 0)
## Each team has a 1/N chance of playing the other teams in the pots at home -- if there are no constraints, N=9 (the number of teams in the pot)
## if there are constraints, each team has a 1/M chance, where M=9 - number of constraints
## to get the correct number of pairings, we need to multiply the row probability by the column probability
## this results in something normalized relatively randomly, so that will need to be taken care of in order to compare to the real simulations

for competition in competitions: 
    dataPath = 'Data/'
    data = getData('{}/AE/{}-{}k.csv'.format(dataPath, competition, n_simulations))


    clubs = set_club_countries_pots(competition)
    npots, nteamsperpot = getNPots_TeamsPerPot(competition)


    savePath_main = 'plots/matchupComparison/{}/'.format(competition)
    savePath_extra = 'plots/matchupComparison/{}/extra/'.format(competition)

    if not os.path.exists(savePath_main):
        os.makedirs(savePath_main)
    if not os.path.exists(savePath_extra):
        os.makedirs(savePath_extra)

    pot_probs = {}
    probability_matrix = np.zeros(( data.shape[0], data.shape[1] )) # where we will store the output 

    ## For UCL and UEL, the number of events per square is number of teams per pot x 2 (bc draw two pairs from each pot) x number of simulations
    if competition == "UCL" or competition == "UEL":
        normFactor = n_simulations * 1000 * nteamsperpot * 2 / 2
    
    ## For UECL, draw only one pair per pot 
    if competition == "UECL":
        normFactor = n_simulations * 1000 * nteamsperpot / 2 
    

    for pot1 in range( 1, npots+1 ):

        for pot2 in range( 1, npots+1 ):

            #if pot1 > pot2: continue # don't need to bother filling the bottom of the diagonal


            ## start and end index of my pot in matrix
            start1 = (pot1-1) * nteamsperpot
            end1 =    pot1    * nteamsperpot
            start2 = (pot2-1) * nteamsperpot
            end2 =    pot2    * nteamsperpot

            # grab the data from only the pot i am working with , for now symmetric but we will come back to that
            sub_matrix = data[start1:end1, start2:end2]


            ##replace all nonzero elements with 1 because I want to be computing the probability, not just taking what is there
            ## now i have a matrix that shows me allowed (1) and not allowed (0) pairings 
            ## n.b. doing this un-normalizes the matrix 
            sub_matrix = np.where( sub_matrix !=0, 1, sub_matrix)
            
            #compute sums per row and per col, as we know that these are our 100%
            row_sums = np.sum(sub_matrix, axis=1)
            col_sums = np.sum(sub_matrix, axis=0)

            print(row_sums)
            print(col_sums)
            print(np.sum(row_sums))
            print(np.sum(col_sums))

            ## normalize the sums to the fact that we should have nteams * nteams total 
            row_sums = nteamsperpot*nteamsperpot / np.sum(row_sums) * row_sums
            col_sums = nteamsperpot*nteamsperpot / np.sum(col_sums) * col_sums
            sub_matrix = nteamsperpot*nteamsperpot / np.sum(sub_matrix) * sub_matrix ## move this up and remove row/col scaling

            print(row_sums)
            print(col_sums)
            print(np.sum(row_sums))
            print(np.sum(col_sums))
            print(np.sum(sub_matrix))


            ## Now make the probabilites by multiplying row probabilities by column probabilities  
            probabilities = (sub_matrix / col_sums) * (sub_matrix / row_sums[:, np.newaxis])

            ## normalize matrix to match draw data
            normalized_matrix = probabilities * normFactor

            ## store in full data struct
            probability_matrix[ start1:end1, start2:end2  ] = normalized_matrix

            ### print debug info
            print(pot1, pot2)
            print(sub_matrix)
            print("rows", row_sums)
            print("cols", col_sums)
            print('pot sum', np.sum(normalized_matrix))
            print(probabilities)
            print(normFactor)
            print(normalized_matrix)
            print()


    ## now let's compare our draw providers with the computed probabilities 
    
    providers = ['prob', 'AE', 'AS']

    all_data = {}
    all_data['prob'] = probability_matrix
    all_data['AE']= getData('{}/AE/{}-{}k.csv'.format(dataPath, competition, n_simulations))
    all_data['AS']= getData('{}/Asolvo/{}-{}k.csv'.format(dataPath, competition, n_simulations))

    #all_data['AE'] = all_data['AE'] + all_data['AE'].T
    #all_data['AS'] = all_data['AS'] + all_data['AS'].T



    for prov in providers:
        nz = emptyBottomDiagonal(all_data[prov])
        nz=all_data[prov]
        make2DTeamPlot(nz, list(clubs.keys()), "False", savePath_extra+"2D_normalized_{}.png".format(prov), competition, cbarLabel="probability", clim=[np.min( nz[nz !=0] ) , np.max(nz)], fontsize=8)
        plt.close()
        np.savetxt(f'{savePath_extra}/data_{prov}.csv', all_data[prov], delimiter=',', fmt='%d')

    for prov in ['AE', 'AS']:

        ## absolute difference
        diff = all_data['prob'] - all_data[prov]
        diffSplit = splitDiagonalToList(diff)
        diffSplitDiag = emptyBottomDiagonal(diff)
        diffSplitDiag = diff

        plt.figure(figsize=(7,6))
        plt.hist(diffSplit, bins=30)
        plt.xlabel("difference in # matchups: probability - {}".format(prov))
        plt.savefig(savePath_extra + "raw_difference_prob-{}.png".format(prov))
        plt.close()

        make2DTeamPlot(diffSplitDiag, list(clubs.keys()), "False", savePath_extra+"2D_raw_difference_prob-{}.png".format(prov), competition, cbarLabel="difference", clim=[ 0 , np.max(abs(diffSplitDiag))], fontsize=8, redTxtPrec='0.2f')
        plt.close()

        ## percent difference 
        pctDiff = (all_data['prob'] - all_data[prov]) * 100 / all_data['prob']
        pctDiffSplit = splitDiagonalToList(pctDiff)
        pctDiffSplitDiag = emptyBottomDiagonal(pctDiff)
        pctDiffSplitDiag = pctDiff

        plt.figure(figsize=(7,6))
        plt.hist(pctDiffSplit, bins=30)
        plt.xlabel("percent difference in # matchups: probability - {}/probability".format(prov))
        plt.savefig(savePath_main + "percent_difference_prob-{}.png".format(prov))
        plt.close()

        make2DTeamPlot(pctDiffSplitDiag, list(clubs.keys()), "abs(workingData[i][j]) > 5", savePath_main+"2D_percent_difference_prob-{}.png".format(prov), competition, cbarLabel="percent difference", clim=[ 0 , 20], fontsize=8, redTxtPrec='0.2f')
        plt.close()
        make2DTeamPlot(pctDiffSplitDiag, list(clubs.keys()), "abs(workingData[i][j]) > 5", savePath_extra+"2D_percent_difference_prob-{}_dynamicAxis.png".format(prov), competition, cbarLabel="percent difference", clim=[ 0 , np.max(pctDiffSplitDiag)], fontsize=8, redTxtPrec='0.2f')
        plt.close()


    plt.close()



