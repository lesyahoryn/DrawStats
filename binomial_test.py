import matplotlib.pyplot as plt
from scipy.stats import binomtest
from scipy.stats import norm
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import os
from draw_stats_helpers import *


np.set_printoptions(threshold=np.inf, linewidth=np.inf)

provider = 'AE'
filepath = 'Data/' + provider + '/'
filepath = 'Data/' + provider + '/Old_UECL_Algo/'
for file in os.listdir(filepath):
    
    if '.csv' not in file: continue

    competition = file.strip(".csv").split("-")[0]
    if competition not in ['UCL', 'UEL', 'UECL']: #one of the pseudodata samples
        competition = "UECL"

    clubs = set_club_countries_pots(competition)

    ##set up input/output paths
    inpName = filepath + file
    saveName = inpName.split("/")[-1].strip(".csv")
    savePath = 'plots/' + provider + "/" + saveName + "/"
    #savePath = 'plots/' + provider + "_oldalgo/" + saveName + "/"

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    data = getData(inpName, provider == 'Barbara' )

    dataT = data.T
    dataSum = data + dataT
    # indexLabels = df["Unnamed: 0"]
    # columnLabels = df.columns
    # print(columnLabels)
    indexLabels=list(clubs.keys())

    ## normalize data and dataT to parallelize the two probabilities
    normFactor = 1
    dataNorm = np.round(data / dataSum * normFactor)
    dataTNorm = np.round(dataT / dataSum * normFactor)
    dataNormSum = dataNorm + dataTNorm 

    ## get p values of binomal test
    ## one test per pairing 

    #output data structure
    workingData = data
    workingSum = dataSum
    nRows, nCols = workingData.shape
    pvalues = np.zeros((nRows, nCols))
    statistics = np.zeros((nRows, nCols))
    p = 0.5
    cl = 0.05

    for i in range(nRows):
        for j in range(nCols):
            if i >= j: continue #only work with cells above diagonal, also skip diagonal bc who cares
            if np.isnan( workingData[i][j] ) and np.isnan( workingData[j][i] ): continue #skip pairings that are illegal
            if workingData[i][j] == 0 and workingData[j][i] == 0 : continue #skip pairings that are illegal

            nHome = int(workingData[i][j])
            nAway = int(workingData[j][i])
            total = int(workingSum[i][j]) ## data sum is symmetric over the diagonal

            result = binomtest( nHome, total, p )
            #result = binomtest( 50-1, 100, 0.5 )
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
    plt.savefig(savePath+"pvalues.png")
    plt.clf()

    print("sum with < {} {}, out of {}".format(cl, np.sum(pvaluesNZ < 0.05), pvaluesNZ.size))
    #bin_range = (0,0.1)
    #overflow_range = (bin_range[0]. bin_range[1]+1)
    counts, bins, _ = plt.hist(pvaluesNZ, bins=40, range=[0,0.1],  label='data')
    plt.axvline(cl, color='black')
    plt.text(0.02,0.90, "number < {}: {}\ntotal: {}".format(cl, np.sum(pvaluesNZ < 0.05), pvaluesNZ.size), transform=plt.gca().transAxes)
    plt.ylim(0,9)
    plt.xlabel("pvalue")
    plt.ylabel("number of pairings")
    plt.savefig(savePath+"pvalues_zoom.png")
    plt.clf()
    
    statisticsNZ = statistics[statistics != 0]
    counts, bins, _ = plt.hist(statisticsNZ, bins=30, label='data')
    plt.axvline(0.5, color='black')
    plt.savefig(savePath+"statistics.png")
    plt.clf()

    ##count low p values per pot, and sum p values per team  
    
    pvalues_perteam = [0]*len(clubs.keys())
    low_pvalues_perteam = [0]*len(clubs.keys())

    npots, nteamsperpot = getNPots_TeamsPerPot(competition)
    
    # pvalues_perpot = {}
    # for pot in range ( 1, npots+1 ):
    #     print("\n pot", pot)
    #     pvalues_perpot[pot] = []

    for i in range(nRows):
        for j in range(nCols):
            if i >= j: continue
            if pvalues[i][j] !=0 : 
                
                pvalues_perteam[i] += pvalues[i][j]
                pvalues_perteam[j] += pvalues[i][j]
                
                if pvalues[i][j] < 0.05:
                    low_pvalues_perteam[i] += 1
                    low_pvalues_perteam[j] += 1

    #pvalues_perpot[pot] = elements_w_index

    ## plot p values per team 
    plt.barh(indexLabels, pvalues_perteam)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
    plt.yticks(np.arange(0,len(indexLabels),1), labels=indexLabels, fontsize=9)
    plt.xlabel("sum of p values per team")
    plt.savefig(savePath+"pvalues-perteam.png")
    plt.clf()

    plt.barh(indexLabels, low_pvalues_perteam)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
    plt.yticks(np.arange(0,len(indexLabels),1), labels=indexLabels, fontsize=9)
    plt.xlabel("number of p-value < 0.05 per team")
    plt.savefig(savePath+"pvalues-nlow-perteam.png")
    plt.close()


    ## do 2d array of p values per matchup

    make2DTeamPlot(pvalues, indexLabels, "workingData[i, j] < 0.05", savePath+"pvalues-2d.png", competition, redTxtPrec='0.2f', cbarLabel="p value")
    plt.close()




