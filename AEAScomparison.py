from draw_stats_helpers import *
import matplotlib.pyplot as plt
import os
from matplotlib.transforms import Affine2D

competitions = ['UCL', 'UECL', 'UEL']

clubs = {}

dataPath = 'Data/'

data = {}
dataSum = {}

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

for competition in competitions:
    clubs = set_club_countries_pots(competition)

    outDir = 'plots/matchupComparison/' + competition + "/"
    #outDir = 'plots/matchupComparison/AEoldvAENew_' + competition + "/"
    #outDir = 'plots/matchupComparison/ASvAENew_' + competition + "/"
    #outDir = 'plots/matchupComparison/ASvAEold_' + competition + "/"

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    data["AE"] = getData(dataPath+"AE/"+competition+"-50k.csv")
    #data["AE"] = getData(dataPath+"AE/Old_UECL_algo/"+competition+"-50k.csv")
    data["AS"] = getData(dataPath+"Asolvo/"+competition+"-50k.csv")
    #data["AE"] = getData(dataPath+"AE/Old_UECL_algo/"+competition+"-50k.csv")


    dataSum["AE"] = data["AE"] + data["AE"].T
    dataSum["AS"] = data["AS"] + data["AS"].T

    #I just want to plot the two total counts over each other
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 6))

    AEsplit = splitDiagonalToList(dataSum['AE'])
    ASsplit = splitDiagonalToList(dataSum['AS'])
    nbins = 20
    val_of_bins_x1, edges_of_bins_x1, patches_x1 = ax1.hist(AEsplit, bins=nbins, label='AE', alpha=0.4, color='green')
    val_of_bins_x2, edges_of_bins_x2, patches_x2 = ax1.hist(ASsplit, bins=nbins, label='Asolvo',  alpha=0.4, color='blue')
    
    ax1.legend()
    
    ratio = np.divide(val_of_bins_x1, val_of_bins_x2)
    print(ratio)
    bin_centers = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
    ax2.plot(bin_centers, ratio, marker='o', linestyle='-', color='green', alpha=0.4)
    ax2.set_ylabel('ratio AE/Asolvo')
    ax2.set_xlabel('number of matchups per pairing')
    ax2.axhline(1, color='black', linestyle='--')
    plt.savefig(outDir+"all_matchups.png")
    plt.close()

    
    ## absolute difference
    dataDiff = dataSum["AE"] - dataSum["AS"]
    dataDiffSplit = splitDiagonalToList(dataDiff)
    plt.hist(dataDiffSplit, bins=30)
    plt.xlabel("difference in # matchups: AE - AS")
    plt.savefig(outDir + "diff.png")
    plt.clf()

    ## percent difference
    dataDiffFractional = dataDiff.astype(np.float64) / dataSum["AE"].astype(np.float64) * 100
    dataDiffFSplit = splitDiagonalToList(dataDiffFractional)
    counts, bins, params = fit_data(dataDiffFSplit , [-5, 5], 30)
    plot(bins, params, outDir + "diffFraction.png", xlineloc=0., range=[-5, 5], xlabel="percent difference in # matchups: (AE - AS)/AE", ymax=80)
    #plot(bins, params, outDir + "diffFraction.png", xlineloc=0., range=[-5, 5], xlabel="percent difference in # matchups: (AE new - AE old)/AE new", ymax=80)
    plt.clf()

    ## difference per pairing

    ## this is cheating so that the plot looks better
    dataDiffZ = emptyBottomDiagonal(dataDiff)
    dataDiffFractionalZ = emptyBottomDiagonal(dataDiffFractional)
    #dataSumAEZ = emptyBottomDiagonal(dataSum['AE'])
    #dataSumASZ = emptyBottomDiagonal(dataSum['AS'])
    dataSumAEZ = dataSum['AE']
    dataSumASZ = dataSum['AS']
    
    names = list(clubs.keys())

    make2DTeamPlot(dataDiffZ, names, "abs(workingData[i, j]) > 400", outDir+"diff-2d.png", cbarLabel="AE - AS", clim=[0,500])
    plt.close()

    make2DTeamPlot(dataSumAEZ, names, "False", outDir+"allData_AE.png", cbarLabel="number of matchups", clim=[np.min( dataSumAEZ[dataSumAEZ !=0] ) , np.max(dataSumAEZ)], fontsize=8)
    plt.close()

    make2DTeamPlot(dataSumASZ, names, "False", outDir+"allData_AS.png", cbarLabel="number of matchups", clim=[np.min( dataSumAEZ[dataSumASZ !=0] ) , np.max(dataSumASZ)], fontsize=8)
    plt.close()
    


    ########################################
    ## do country comparison for UCL only
    if competition == 'UCL':

        country_comp = {}
        big_countries = ['ENG', 'ESP', 'GER', 'ITA', 'FRA']
        big_country_indices = {}

        ## identify indices in array that have the big countries 

        for club in clubs.keys():
            if clubs[club]['country'] in big_countries: 
                #big_country_indices[clubs[club]['country']].append( names.index(club) )
                big_country_indices[names.index(club)] = clubs[club]['country']
        print(big_country_indices)

        combinations = ['ENG-ESP', 'ENG-GER', 'ENG-ITA', 'ENG-FRA',
                                   'ESP-GER', 'ESP-ITA', 'ESP-FRA',
                                              'GER-ITA', 'GER-FRA',
                                                         'ITA-FRA']
        
        for combination in combinations:
            country_comp[combination] = []

        
        for i in range(dataDiffFractionalZ.shape[0]):
            for j in range(dataDiffFractionalZ.shape[1]):
                if i >= j: continue

                if i in big_country_indices.keys() and j in big_country_indices.keys():   ## only want big country - big country pairings                    
                    
                    if big_country_indices[i] == big_country_indices[j] : continue ## if same country

                    flag = bigCountryFillString( big_country_indices[i], big_country_indices[j], combinations)
                    country_comp[ flag ].append(dataDiffFractionalZ[i][j])
        
        means = []  ## these should stay in order with the combinations bc everything is a list
        stds = []
        for combination in combinations:
            means.append( np.mean( country_comp[combination] ) )
            stds.append( np.std( country_comp[combination] ) )
        
        plt.errorbar( combinations, means, yerr=stds, marker='o', linestyle='none' )
        plt.axhline(0, color='black', linestyle='--')
        plt.ylabel( "percent difference (AE - Asolvo)/AE" )
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(outDir+"bigCountryComp.png")
        plt.clf()

        ## lets just plot them all on top of each other, yolo
        for country in big_countries:
            for combination in combinations:
                if country in combination:
                    plt.hist( country_comp[combination], label=combination, histtype='barstacked')
            plt.legend()
            plt.xlabel("percent difference (AE - Asolvo)/AE")
            plt.savefig(outDir+"bigCountryComp_{}.png".format(country))
            plt.clf()



