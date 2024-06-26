from scipy.stats import norm
import os
from matplotlib.transforms import Affine2D
import argparse
import sys

from draw_stats_helpers import *
from DataHandler import DataHandler
import data_config

init()

parser = argparse.ArgumentParser()
parser.add_argument('--provider', type=str, help='choices: AE, Asolvo, all. All runs both. Default = all', default='all')
parser.add_argument('--competition', type=str, help='choices: UCL, UECL, UEL, all. All runs all 3, otherwise provide comma separated list. Default = all', default='all' )

args = parser.parse_args()

providers=[]
if args.provider == 'all':
    providers = data_config.providers
else:
    for prov in args.provider.split(','):
        if prov.strip(" ") not in data_config.providers:
            print("INVALID PROVIDER")
            sys.exit()
        else:
            providers.append(prov.strip(" "))

competitions=[]
if args.competition == 'all':
    competitions = data_config.competitions
else:
    for prov in args.competition.split(','):
        if prov.strip(" ") not in data_config.competitions:
            print("INVALID COMPETITION")
            sys.exit()
        else:
            competitions.append(prov.strip(" "))

print(providers, competitions)


for provider in providers:

    for competition in competitions:

        print("TESTING", competition, provider)

        savePath = '{}/{}/'.format(data_config.plotDir, competition)
        savePath_main = savePath + '{}_'.format(provider)
        savePath_extra = savePath + 'extras/HA_probability/{}_'.format(provider)
        #savePath = 'plots/' + provider + "_oldalgo/" + saveName + "/"

        if not os.path.exists(savePath):
            os.makedirs(savePath)
        if not os.path.exists( savePath + 'extras/HA_probability/'):
            os.makedirs( savePath + 'extras/HA_probability/')

        data = DataHandler(provider, competition)
        data.setDataPath(data_config.data_config[provider][competition])

        dataSum = data.data + data.data.T

        ## normalize data and dataT to parallelize the two probabilities
        normFactor = 100
        dataNorm = data.data / dataSum * normFactor
        dataTNorm = data.data.T / dataSum * normFactor

        #############
        # basic plotting of population
        #############

        ## normalized distribution
        dataNormH = splitDiagonalToList(dataNorm)
        counts, bins, params = fit_data(dataNormH , [0.43*normFactor,0.57*normFactor], 20)
        plot(bins, params, savePath_main + "HA_prob_normalized.png", xlineloc=0.5*normFactor, range=[0.43*normFactor,0.57*normFactor], ymax=110, extratext= "COMPARE TO: \nmean: {} \nsigma: {}".format(50.,0.5))
        plt.clf()

        ## difference between home and away
        dataDiff = dataNorm - dataTNorm

        dataDiffH = splitDiagonalToList(dataDiff)
        counts, bins, params = fit_data(dataDiffH , [-0.2*normFactor,0.2*normFactor], 20)
        plot(bins, params, savePath_extra + "HA_difference.png", xlineloc=0.0*normFactor, range=[-0.2*normFactor,0.2*normFactor])
        plt.clf()

        #############
        # separate above into curve per pot - also summary plots per pot
        #############

        ## i want to know the probability of pot 1 playing at home vs pot1, pot2, pot3, pot4
        prob_pot_v_pot = {}
        mean_pot_v_pot = {}
        stdv_pot_v_pot = {}

        ## set up data structures to save the data per pot 
        for potH in range( 1, data.npots+1 ):
            prob_pot_v_pot[potH] = {}
            mean_pot_v_pot[potH] = []
            stdv_pot_v_pot[potH] = []
            for potA in range( 1, data.npots+1 ):
                prob_pot_v_pot[potH][potA] = []

        # for each team to play each other team, but smeared into pots
        clubList = list(data.clubs.keys())
        for teamH in data.clubs:
            for teamA in data.clubs:
                potH = data.clubs[teamH]['pot']
                idxH = clubList.index(teamH)

                potA = data.clubs[teamA]['pot']
                idxA = clubList.index(teamA)

                if not np.isnan(dataNorm[idxH][idxA]):
                    prob_pot_v_pot[potH][potA].append( dataNorm[idxH][idxA] )

        ## make one plot for each home plot and make the data list for the summary plot
        for potH in range( 1, data.npots+1 ):
            for potA in range( 1, data.npots+1 ):
                mean_pot_v_pot[potH].append( np.mean(prob_pot_v_pot[potH][potA]) )
                stdv_pot_v_pot[potH].append( np.nanstd(prob_pot_v_pot[potH][potA]) )

                plt.hist( prob_pot_v_pot[potH][potA], label="vs pot {}".format(potA), histtype="step", range=[0.43*normFactor,0.57*normFactor], bins=30)

            plt.xlabel("times pot {} plays at home".format(potH))
            plt.legend()
            plt.savefig(savePath_extra + "probability_for_pot{}.png".format(potH))
            plt.clf()

        ## summary plot -- mostly some python magic to make the dots not on top of each other
        trans = {}
        fig, ax = plt.subplots()
        trans[1] = Affine2D().translate(-0.3, 0.0) + ax.transData
        trans[2] = Affine2D().translate(-0.2, 0.0) + ax.transData
        trans[3] = Affine2D().translate(-0.1, 0.0) + ax.transData
        trans[4] = Affine2D().translate(0.0, 0.0) + ax.transData
        if competition == "UECL":
            trans[5] = Affine2D().translate(0.1, 0.0) + ax.transData
            trans[6] = Affine2D().translate(0.2, 0.0) + ax.transData
        for potH in range( 1, data.npots+1 ):
            ax.errorbar( range( 1, data.npots+1 ), mean_pot_v_pot[potH], yerr=stdv_pot_v_pot[potH], 
                        marker='o', linestyle='none', label='Pot {}'.format(potH), transform=trans[potH])

        plt.xlabel("Away pot")
        plt.ylabel("probability at home")
        plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc='lower left', mode='expand',ncol=len(range( 1, data.npots+1 )), title='home pot')
        plt.savefig(savePath_extra + 'summary_probability_per_pot.png')
        plt.clf()

        plt.close()

    plt.close()

            

                    

