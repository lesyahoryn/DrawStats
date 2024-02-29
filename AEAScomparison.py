from draw_stats_helpers import *
import matplotlib.pyplot as plt
import os
import argparse
from DataHandler import DataHandler
import data_config
import sys

competitions = ['UCL', 'UECL', 'UEL']

RED = '\033[91m'
RESET = '\033[0m'


dataPath = 'Data/'

init()

parser = argparse.ArgumentParser()
parser.add_argument('--competition', type=str,            help='choices: UCL, UECL, UEL, all. All runs all 3, otherwise provide comma separated list. Default = all', default='all' )
parser.add_argument('--test100',     action='store_true', help='Running test with 100 simulations (to account for different AE data that should not be summed across the diagonal)')

args = parser.parse_args()

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

print(competitions)


for competition in competitions:

    #savePath_main = 'plots/matchupComparison/{}/'.format(competition)
    #savePath_extra = 'plots/matchupComparison/{}/extra/'.format(competition)
    savePath = '{}/{}/'.format(data_config.plotDir, competition)
    savePath_main = savePath + '{}_'.format('comparison')
    savePath_extra = savePath + 'extras/AE_Asolvo_Comparison/{}_'.format('comparison')

    if not os.path.exists(savePath):
        os.makedirs(savePath)
    if not os.path.exists(savePath + 'extras/AE_Asolvo_Comparison/'):
        os.makedirs(savePath + 'extras/AE_Asolvo_Comparison/')

    data_AE = DataHandler("AE", competition)
    data_AS = DataHandler("Asolvo", competition)

    data_AE.setDataPath(data_config.data_config['AE'][competition])
    data_AS.setDataPath(data_config.data_config['Asolvo'][competition])


    if args.test100:
        dataSumAE = data_AE.data
    else:
        dataSumAE = data_AE.data + data_AE.data.T
    
    dataSumAS = data_AS.data + data_AS.data.T


    results = []
    result_strings = []

    result_strings.append("same teams")
    if set(list(data_AE.clubs.keys())) == set(list(data_AS.clubs.keys())):
        results.append(1) 
    else:
        results.append(0)

    result_strings.append("same order")
    if list(data_AE.clubs.keys()) == list(data_AS.clubs.keys()):
        results.append(1)
    else:
        results.append(0)

    if 0 in results: # if any of the above failed

        with open(savePath_main+"_teamListWithProblems.txt", "w", encoding='utf-8') as f:
            listAE = list(data_AE.clubs.keys())
            listAS = list(data_AS.clubs.keys())
            width = max(len(word) for word in listAE + listAS)

            for iclub in range(len(listAE)):
                txt = "{:<{width}} {:<{width}}".format(listAE[iclub], listAS[iclub], width=width)
                if listAE[iclub] != listAS[iclub]:
                    print(RED + txt + RESET)
                    f.write(txt + "!!!!!!!! \n")
                else:
                    print(txt)
                    f.write(txt + "\n")


    plt.bar( result_strings, results, color="green")
    plt.ylim(0,1)
    plt.savefig(savePath_main+"teamCheck.png")    
    plt.close()



    ##############
    ## just counts per provider and ratio
    ##############
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

    ###################
    ## overall difference 
    ###################
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
    make2DTeamPlot(dataDiffZ, names, "abs(workingData[i, j]) > 400", savePath_main+"difference_per_matchup_2D.png", data_AE.nteamsperpot, data_AE.npots, cbarLabel="AE - AS", clim=[0,50])
    plt.close()

    dataSumAEZ = emptyBottomDiagonal(dataSumAE)
    make2DTeamPlot(dataSumAEZ, names, "False", savePath_extra+"allData_AE.png", data_AE.nteamsperpot, data_AE.npots, cbarLabel="number of matchups", clim=[np.min( dataSumAEZ[dataSumAEZ !=0] ) , np.max(dataSumAEZ)], fontsize=7)
    plt.close()

    dataSumASZ = emptyBottomDiagonal(dataSumAS)
    make2DTeamPlot(dataSumASZ, names, "False", savePath_extra+"allData_Asolvo.png", data_AS.nteamsperpot, data_AS.npots, cbarLabel="number of matchups", clim=[np.min( dataSumAEZ[dataSumASZ !=0] ) , np.max(dataSumASZ)], fontsize=8)
    plt.close()

    ## check permission matrices
    ## replace data with 1 to indicate an allowed pairing, 0 to indicate an disallowed pairing
    permission_AE = np.where( data_AE.data !=0, 1, 0)
    permission_AS = np.where( data_AS.data !=0, 1, 0)

    difference_permission = permission_AE - permission_AS

    make2DTeamPlot(difference_permission, names, "False", savePath_main+"difference_allowedPairings_2D.png", data_AE.nteamsperpot, data_AE.npots, cbarLabel="AE - AS", clim=[0,1])
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