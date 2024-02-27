import matplotlib.pyplot as plt
from scipy.stats import binomtest
import pandas as pd
import numpy as np
import os
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

        ##set up output paths
        savePath = 'plots/{}/'.format(competition)
        savePath_main = savePath + '{}_'.format(provider)
        savePath_extra = savePath + 'extras/HA_binomial/{}_'.format(provider)
        #savePath = 'plots/' + provider + "_oldalgo/" + saveName + "/"

        if not os.path.exists(savePath):
            os.makedirs(savePath)
        if not os.path.exists(savePath + 'extras/HA_binomial/'):
            os.makedirs(savePath + 'extras/HA_binomial/')

        data = DataHandler(provider, competition)
        data.setDataPath(data_config.data_config[provider][competition])

        dataSum = data.data + data.data.T

        indexLabels=list(data.clubs.keys())

        ## normalize data and dataT to parallelize the two probabilities
        normFactor = 1
        dataNorm = np.round(data.data / dataSum * normFactor)
        dataTNorm = np.round(data.data.T / dataSum * normFactor)
        dataNormSum = dataNorm + dataTNorm  

        
        #############
        # perform binomial test per pairing
        #    -- one result per pairing
        #############

        #output data structure
        workingData = data.data
        workingSum = dataSum
        pvalues = np.zeros((data.nteams, data.nteams))
        statistics = np.zeros((data.nteams, data.nteams))
        p = 0.5
        cl = 0.05

        for i in range(data.nteams):
            for j in range(data.nteams):
                if i >= j: continue #only work with cells above diagonal, also skip diagonal bc who cares
                if np.isnan( workingData[i][j] ) and np.isnan( workingData[j][i] ): continue #skip pairings that are illegal
                if workingData[i][j] == 0 and workingData[j][i] == 0 : continue #skip pairings that are illegal

                nHome = int(workingData[i][j])
                nAway = int(workingData[j][i])
                total = int(workingSum[i][j]) ## data sum is symmetric over the diagonal

                result = binomtest( nHome, total, p )
                pvalues[i][j] = result.pvalue
                statistics[i][j] = result.statistic
                #print(i, j, nHome, nAway, total, result.pvalue, result.statistic, result.proportion_ci(confidence_level=0.95))


        plt.clf()
        plt.figure(figsize=(7,6))
        pvaluesNZ = pvalues[pvalues != 0]
        counts, bins, _ = plt.hist(pvaluesNZ, bins=30, label='data')
        #plt.xscale('log')
        plt.xlabel("pvalue")
        plt.ylabel("number of pairings")
        plt.savefig(savePath_extra+"pvalues_0to1.png")
        plt.clf()

        print("sum with < {} {}, out of {}".format(cl, np.sum(pvaluesNZ < 0.05), pvaluesNZ.size))
        #bin_range = (0,0.1)
        #overflow_range = (bin_range[0]. bin_range[1]+1)
        counts, bins, _ = plt.hist(pvaluesNZ, bins=40, range=[0,0.1],  label='data')
        plt.axvline(cl, color='black')
        plt.text(0.02,0.90, "number < {}: {}\ntotal: {}".format(cl, np.sum(pvaluesNZ < 0.05), pvaluesNZ.size), transform=plt.gca().transAxes)
        plt.text(0.02,0.70, "compare to 31 \n(5% of total number of pairings)", transform=plt.gca().transAxes, color='red')
        plt.ylim(0,9)
        plt.xlabel("pvalue")
        plt.ylabel("number of pairings")
        plt.savefig(savePath_main+"pvalues_0to0p1.png")
        plt.clf()
        
        statisticsNZ = statistics[statistics != 0]
        counts, bins, _ = plt.hist(statisticsNZ, bins=30, label='data')
        plt.axvline(0.5, color='black')
        plt.savefig(savePath_extra+"estimated_statistic.png")
        plt.clf()

        ##count low p values per pot, and sum p values per team  
        
        pvalues_perteam = [0]*data.nteams
        low_pvalues_perteam = [0]*data.nteams
        
        for i in range(data.nteams):
            for j in range(data.nteams):
                if i >= j: continue
                if pvalues[i][j] !=0 : 
                    
                    pvalues_perteam[i] += pvalues[i][j]
                    pvalues_perteam[j] += pvalues[i][j]
                    
                    if pvalues[i][j] < 0.05:
                        low_pvalues_perteam[i] += 1
                        low_pvalues_perteam[j] += 1

        ## plot p values per team 
        plt.barh(indexLabels, pvalues_perteam)
        plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
        plt.yticks(np.arange(0,len(indexLabels),1), labels=indexLabels, fontsize=9)
        plt.xlabel("sum of p values per team")
        plt.savefig(savePath_extra+"pvalues_perteam.png")
        plt.clf()

        plt.barh(indexLabels, low_pvalues_perteam)
        plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
        plt.yticks(np.arange(0,len(indexLabels),1), labels=indexLabels, fontsize=9)
        plt.xlabel("number of p-value < 0.05 per team")
        plt.savefig(savePath_extra+"n_low_pvalues_per_team.png")
        plt.close()


        ## do 2d array of p values per matchup
        make2DTeamPlot(pvalues, indexLabels, "workingData[i, j] < 0.05", savePath_extra+"pvalue_per_matchup_2D.png", data.npots, data.nteamsperpot, redTxtPrec='0.2f', cbarLabel="p value")
        plt.close()




