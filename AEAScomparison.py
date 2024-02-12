from draw_stats_helpers import *
import matplotlib.pyplot as plt
import os

competitions = ['UCL', 'UECL', 'UEL']
clubs = {}

dataPath = 'Data/'

data = {}
dataSum = {}

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

for competition in competitions:
    clubs[competition] = set_club_countries_clubs(competition)

    outDir = 'plots/matchupComparison/' + competition + "/"

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    data["AE"] = getData(dataPath+"AE/"+competition+"-50k.csv")
    data["AS"] = getData(dataPath+"Asolvo/"+competition+"-50k.csv")

    dataSum["AE"] = data["AE"] + data["AE"].T
    dataSum["AS"] = data["AS"] + data["AS"].T


    dataDiff = dataSum["AE"] - dataSum["AS"]
    print( "competition ", competition)
    print( dataDiff[ abs(dataDiff) > 400])
    
    dataDiffSplit = splitDiagonalToList(dataDiff)
    plt.hist(dataDiffSplit, bins=30)
    plt.xlabel("difference in # matchups: AE - AS")
    plt.savefig(outDir + "diff.png")
    #counts, bins, params = fit_data(dataDiffSplit , [0.43*normFactor,0.57*normFactor], 20)
    #plot(bins, params, savePath + "HA_norm_zoom.png") #plot w default range
    #plot(bins, params, savePath + "HA_norm.png", xlineloc=0.5*normFactor, range=[0.43*normFactor,0.57*normFactor])
    plt.clf()


    dataDiffFractional = dataDiff.astype(np.float64) / dataSum["AS"].astype(np.float64) * 100

    dataDiffFSplit = splitDiagonalToList(dataDiffFractional)
    counts, bins, params = fit_data(dataDiffFSplit , [-5, 5], 30)
    #plot(bins, params, savePath + "HA_norm_zoom.png") #plot w default range
    plot(bins, params, outDir + "diffFraction.png", xlineloc=0., range=[-5, 5], xlabel="percent difference in # matchups: (AE - AS)/AE")
    plt.clf()


    dataDiffZ = np.zeros((dataDiff.shape[0], dataDiff.shape[1]))
    for i in range(dataDiff.shape[0]):
        for j in range(dataDiff.shape[1]):
            if i >= j: continue
            dataDiffZ[i][j] = dataDiff[i][j]
    
    names = list(clubs[competition].keys())

    ## do 2d array of p values per matchup
    plt.figure(figsize=(20,20))
    plt.imshow(abs(dataDiffZ), cmap='Greens')
    warningVal = 400

    for i in range(dataDiffZ.shape[0]):
        for j in range(dataDiffZ.shape[1]):
            if i >= j: continue #only work with cells above diagonal, also skip diagonal bc who cares
            if np.isnan( dataDiffZ[i][j] ) and np.isnan( dataDiffZ[j][i] ): continue #skip pairings that are illegal
            if abs(dataDiffZ[i, j]) > 400 :
                plt.text(j, i, f'{dataDiffZ[i, j]: .0f}', ha='center', va='center', color='red')
            else:
                plt.text(j, i, f'{dataDiffZ[i, j]: .0f}', ha='center', va='center', color='black')

    # add team names as x and y ticks
    

    plt.xticks(np.arange(0,len(names),1), labels=names, fontsize=12, rotation=90)
    plt.yticks(np.arange(0,len(names),1), labels=names, fontsize=12)

    plt.tick_params(axis='x', labeltop=True, labelbottom=False, bottom=False, top=True)
    plt.tick_params(axis='y', labelright=False, labelleft=True, left=True, right=False)

    # Add color bar
    cbar = plt.colorbar(shrink=0.7, location='right', label="AE-Asolvo")

    plt.savefig(outDir+"diff-2d.png")
    plt.close()






