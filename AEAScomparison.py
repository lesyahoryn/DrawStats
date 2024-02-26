from draw_stats_helpers import *
import matplotlib.pyplot as plt
import os
from matplotlib.transforms import Affine2D
import argparse
from DataHandler import * 

competitions = ['UCL', 'UECL', 'UEL']

dataPath = 'Data/'

init()

parser = argparse.ArgumentParser()
parser.add_argument('--test100', action='store_true', help='Running test with 100 simulations (to account for different AE data that should not be summed across the diagonal)')

args = parser.parse_args()


for competition in competitions:
    #for db_num in range(1,6):

    savePath_main = 'plots/matchupComparison/{}/'.format(competition)
    savePath_extra = 'plots/matchupComparison/{}/extra/'.format(competition)
    #savePath_main = 'plots/matchupComparison/AE_DB_{}/{}/'.format(db_num, competition)
    #savePath_extra = 'plots/matchupComparison/AE_DB_{}/{}/extra/'.format(db_num, competition)

    if not os.path.exists(savePath_main):
        os.makedirs(savePath_main)
    if not os.path.exists(savePath_extra):
        os.makedirs(savePath_extra)

    data_AE = DataHandler("AE", competition)
    data_AS = DataHandler("Asolvo", competition)

    data_AE.setDataPath(dataPath+"AE/"+competition+"-50k.csv")
    data_AS.setDataPath(dataPath+"Asolvo/"+competition+"-50k.csv")


    if args.test100:
        dataSumAE = data_AE.data
    else:
        dataSumAE = data_AE.data + data_AE.data.T
    
    dataSumAS = data_AS.data + data_AS.data.T

    #I just want to plot the two total counts over each other
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 6))

    AEsplit = splitDiagonalToList(dataSumAE)
    ASsplit = splitDiagonalToList(dataSumAS)
    nbins = 20
    val_of_bins_x1, edges_of_bins_x1, patches_x1 = ax1.hist(AEsplit, bins=nbins, label='AE', alpha=0.4, color='green')
    val_of_bins_x2, edges_of_bins_x2, patches_x2 = ax1.hist(ASsplit, bins=nbins, label='Asolvo',  alpha=0.4, color='blue')
    
    ax1.legend()
    
    ratio = np.divide(val_of_bins_x1, val_of_bins_x2)
    bin_centers = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
    ax2.plot(bin_centers, ratio, marker='o', linestyle='-', color='green', alpha=0.4)
    ax2.set_ylabel('ratio AE/Asolvo')
    ax2.set_xlabel('number of matchups per pairing')
    ax2.axhline(1, color='black', linestyle='--')
    plt.savefig(savePath_extra+"matchups_per_pairing.png")
    plt.close()

    
    ## absolute difference
    dataDiff = dataSumAE - dataSumAS
    dataDiffSplit = splitDiagonalToList(dataDiff)
    plt.hist(dataDiffSplit, bins=30)
    plt.xlabel("difference in # matchups: AE - AS")
    plt.savefig(savePath_extra + "raw_difference.png")
    plt.clf()

    ## percent difference
    dataDiffFractional = dataDiff.astype(np.float64) / dataSumAE.astype(np.float64) * 100
    dataDiffFSplit = splitDiagonalToList(dataDiffFractional)
    plt.hist(dataDiffSplit, bins=20)
    plt.xlabel("percent difference in # matchups: (AE - AS)/AE")
    plt.savefig(savePath_main + "percent_difference.png")
    plt.clf()


    # counts, bins, params = fit_data(dataDiffFSplit , [-5, 5], 30)
    # plot(bins, params, savePath_main + "percent_difference.png", xlineloc=0., range=[-5, 5], xlabel="percent difference in # matchups: (AE - AS)/AE", ymax=80)
    # plt.clf()

    #############
    ## Make some plots per-pairing
    ############

    names = list(data_AE.clubs.keys())
    
    dataDiffZ = emptyBottomDiagonal(dataDiff)
    make2DTeamPlot(dataDiffZ, names, "abs(workingData[i, j]) > 400", savePath_main+"difference_per_matchup_2D.png", competition, cbarLabel="AE - AS", clim=[0,50])
    plt.close()

    dataSumAEZ = emptyBottomDiagonal(dataSumAE)
    make2DTeamPlot(dataSumAEZ, names, "False", savePath_extra+"allData_AE.png", competition, cbarLabel="number of matchups", clim=[np.min( dataSumAEZ[dataSumAEZ !=0] ) , np.max(dataSumAEZ)], fontsize=7)
    plt.close()

    dataSumASZ = emptyBottomDiagonal(dataSumAS)
    make2DTeamPlot(dataSumASZ, names, "False", savePath_extra+"allData_Asolvo.png", competition, cbarLabel="number of matchups", clim=[np.min( dataSumAEZ[dataSumASZ !=0] ) , np.max(dataSumASZ)], fontsize=8)
    plt.close()

    ## check permission matrices
    ## replace data with 1 to indicate an allowed pairing, 0 to indicate an disallowed pairing
    permission_AE = np.where( data_AE.data !=0, 1, 0)
    permission_AS = np.where( data_AS.data !=0, 1, 0)

    difference_permission = permission_AE - permission_AS

    make2DTeamPlot(difference_permission, names, "False", savePath_main+"difference_allowedPairings_2D.png", competition, cbarLabel="AE - AS", clim=[0,1])
    plt.close()


    ########################################
    ## do country comparison for UCL only
    ########################################
    if competition == 'UCL':

        country_comp = {}
        big_countries = ['ENG', 'ESP', 'GER', 'ITA', 'FRA']
        big_country_indices = {}

        ## identify indices in array that have the big countries 

        for club in data_AE.clubs.keys():
            if data_AE.clubs[club]['country'] in big_countries: 
                #big_country_indices[clubs[club]['country']].append( names.index(club) )
                big_country_indices[names.index(club)] = data_AE.clubs[club]['country']

        combinations = ['ENG-ESP', 'ENG-GER', 'ENG-ITA', 'ENG-FRA',
                                'ESP-GER', 'ESP-ITA', 'ESP-FRA',
                                            'GER-ITA', 'GER-FRA',
                                                        'ITA-FRA']
        
        for combination in combinations:
            country_comp[combination] = []

        dataDiffFractionalZ = emptyBottomDiagonal(dataDiffFractional)
        for i in range(dataDiffFractionalZ.shape[0]):
            for j in range(dataDiffFractionalZ.shape[1]):
                if i >= j: continue

                if i in big_country_indices.keys() and j in big_country_indices.keys():   ## only want big country - big country pairings                    
                    
                    if big_country_indices[i] == big_country_indices[j] : continue ## same country

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
        plt.savefig(savePath_extra+"big_country_matchups.png")
        plt.clf()

        ## lets just plot them all on top of each other, yolo
        for country in big_countries:
            for combination in combinations:
                if country in combination:
                    plt.hist( country_comp[combination], label=combination, linewidth=2, alpha=0.6)
            plt.legend()
            plt.xlabel("percent difference (AE - Asolvo)/AE")
            plt.savefig(savePath_extra+"big_country_matchups_{}.png".format(country))
            plt.clf()


plt.close()
