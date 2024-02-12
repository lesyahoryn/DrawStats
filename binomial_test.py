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
for file in os.listdir(filepath):
    if '.csv' not in file: continue

    ##set up input/output paths
    inpName = filepath + file
    saveName = inpName.split("/")[-1].strip(".csv")
    savePath = 'plots/' + provider + "/" + saveName + "/"

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    #get info from competition, assume competition is what's before first - in name 
    competition = file.strip(".csv").split("-")[0]
    if competition not in ['UCL', 'UEL', 'UECL']: #one of the pseudodata samples
        competition = "UECL"

    print(file, competition)

    clubs, pots_indices = get_clubs_pots_indices(competition)


    ## import data and set up matrices, transpose used for adding/subtracting across the diagonal
    #from excel with labels
    if provider == 'Barbara': #no team names in spreadsheet, and extra empty column at the end
        data = np.genfromtxt(inpName, delimiter=',')
        data = data[:, ~np.isnan(data).any(axis=0)]
    
    else: #it's from an excel sheet with the names
        df = pd.read_csv(inpName)
        data = df.iloc[:, 1:].values


    dataT = data.T
    dataSum = data + dataT
    # indexLabels = df["Unnamed: 0"]
    # columnLabels = df.columns
    # print(columnLabels)
    indexLabels=clubs

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
    pvalues_perpot = {}
    pvalues_perteam = [0]*len(clubs)
    low_pvalues_perteam = [0]*len(clubs)
    for pot in pots_indices:
        print("\n pot", pot)
        elements_w_index = []
        n_low_p = 0

        for index in pots_indices[pot]:

            for i in range(nRows):
                for j in range(nCols):
                    if i == index or j == index:
                        if pvalues[i][j] !=0 : 
                            
                            pvalues_perteam[index] += pvalues[i][j]
                            elements_w_index.append(pvalues[i][j])
                            
                            if pvalues[i][j] < 0.05:
                                low_pvalues_perteam[index] += 1
                                n_low_p += 1 

        pvalues_perpot[pot] = elements_w_index
        print("elements w index", len(elements_w_index))
        print("with low p value", n_low_p)
        print("fraction with low p", n_low_p*1.0/len(elements_w_index))

    ## plot p values per team 
    plt.barh(clubs, pvalues_perteam)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
    plt.yticks(np.arange(0,len(clubs),1), labels=indexLabels, fontsize=9)
    plt.xlabel("sum of p values per team")
    plt.savefig(savePath+"pvalues-perteam.png")
    plt.clf()

    plt.barh(clubs, low_pvalues_perteam)
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)
    plt.yticks(np.arange(0,len(clubs),1), labels=indexLabels, fontsize=9)
    plt.xlabel("number of p-value < 0.05 per team")
    plt.savefig(savePath+"pvalues-nlow-perteam.png")
    plt.close()


    ## do 2d array of p values per matchup

    make2DTeamPlot(pvalues, indexLabels, "workingData[i, j] < 0.05", savePath+"pvalues-2d.png", redTxtPrec='0.2f', cbarLabel="p value")
    plt.close()




