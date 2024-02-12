import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
import os
import draw_stats_helpers
from matplotlib.transforms import Affine2D


##############
## some lil plotters and fitters
##############
def gaussian(x, a, mean, sigma):
    return a * np.exp(-((x - mean)**2 / (2 * sigma**2)))

def fit_data(data, range, nbins=20):
    #data = data[~np.isnan(data)] ## remove nan for plotting
    counts, bins, _ = plt.hist(data, bins=nbins, label='data')

    guess = (range[0] + range[1])/2
    sigma_guess = abs(range[0] - range[1])/2
    initial_guess = [1, guess, 1]
    params, covariance = curve_fit(gaussian, bins[:-1], counts, p0=initial_guess, maxfev=5000)

    return counts, bins, params

def plot(bins, params, savePath, xlineloc=-999, range=[]):

    x_values = np.linspace(min(bins), max(bins), 1000)

    plt.plot(x_values, gaussian(x_values, *params), color='red', linestyle='-', label='Fit')
    
    plt.text(0.02,0.90, "mean: {} \nsigma: {}".format(round(params[1], 6), round(params[2], 6)), transform=plt.gca().transAxes)

    if xlineloc != -999 : plt.axvline(x=xlineloc, color='black')

    if len(range) != 0: plt.xlim(range)
    plt.legend()
    plt.savefig(savePath)
    print("mean", params[1])
    print("sigma", params[2])

def splitDiagonalToList(data):
    nRows, nCols = data.shape
    output = []
    
    for i in range(nRows):
        for j in range(nCols):
            if i >= j: continue #only work with cells above diagonal, also skip diagonal bc who cares
            if np.isnan( data[i][j] ) and np.isnan( data[j][i] ): continue #skip pairings that are illegal
            if data[i][j] == 0 and data[j][i] == 0 : continue #skip pairings that are illegal

            output.append(data[i][j])

    return output

######################
### script
######################
if __name__ == '__main__':

    np.set_printoptions(threshold=np.inf, linewidth=np.inf)

    provider = 'Asolvo'
    filepath = 'Data/' + provider + '/'
    for file in os.listdir(filepath):
        if '.csv' not in file: continue


        inpName = filepath + file
        saveName = inpName.split("/")[-1].strip(".csv")
        savePath = 'plots/' + provider + "/" + saveName + "/"
        
        print(inpName)
        #if "Ba5000Sim050" not in inpName: continue

        if not os.path.exists(savePath):
            os.makedirs(savePath)

        #get info from competition, assume competition is what's before first - in name 
        competition = file.strip(".csv").split("-")[0]
        if competition not in ['UCL', 'UEL', 'UECL']: #one of the pseudodata samples
            competition = "UECL"

        print(file, competition)

        clubs, pots_indices = draw_stats_helpers.get_clubs_pots_indices(competition)

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

        ## normalize data and dataT to parallelize the two probabilities
        normFactor = 100
        dataNorm = data / dataSum * normFactor
        dataTNorm = dataT / dataSum * normFactor


        ## do some basic plotting, just see spread of values and fit histogram

        #############
        # plot and fit normalized distribution
        #############
        print("normalized")
        dataNormH = splitDiagonalToList(dataNorm)
        counts, bins, params = fit_data(dataNormH , [0.43*normFactor,0.57*normFactor], 20)
        #plot(bins, params, savePath + "HA_norm_zoom.png") #plot w default range
        plot(bins, params, savePath + "HA_norm.png", xlineloc=0.5*normFactor, range=[0.43*normFactor,0.57*normFactor])
        plt.clf()

        ###########
        # plot and fit difference between home and away
        ###########
        dataDiff = dataNorm - dataTNorm

        print("diff")
        dataDiffH = splitDiagonalToList(dataDiff)
        counts, bins, params = fit_data(dataDiffH , [-0.2*normFactor,0.2*normFactor], 20)
        #plot(bins, params, savePath + "HA_diff_zoom.png")
        plot(bins, params, savePath + "HA_diff.png", xlineloc=0.0*normFactor, range=[-0.2*normFactor,0.2*normFactor])
        plt.clf()


        ##Separate above curves into one per pot
        ## i want to know the probability of pot 1 playing at home vs pot1, pot2, pot3, pot4
        prob_pot_v_pot = {}
        mean_pot_v_pot = {}
        stdv_pot_v_pot = {}
        nRows, nCols = dataNorm.shape
        for potH in pots_indices:
            prob_pot_v_pot[potH] = {}
            mean_pot_v_pot[potH] = []
            stdv_pot_v_pot[potH] = []
            for potA in pots_indices:
                prob_pot_v_pot[potH][potA] = []
        
        for potH in pots_indices:
            for idxH in pots_indices[potH]:
                for potA in pots_indices:
                    for idxA in pots_indices[potA]:
                        if not np.isnan(dataNorm[idxH][idxA]):
                            prob_pot_v_pot[potH][potA].append( dataNorm[idxH][idxA] )

        for potH in pots_indices:
            for potA in pots_indices:
                print()
                print( prob_pot_v_pot[potH] )
                print( np.mean(prob_pot_v_pot[potH][potA]) )
                mean_pot_v_pot[potH].append( np.mean(prob_pot_v_pot[potH][potA]) )
                stdv_pot_v_pot[potH].append( np.nanstd(prob_pot_v_pot[potH][potA]) )
                #print(mean_pot_v_pot)
                #print(stdv_pot_v_pot)
                plt.hist( prob_pot_v_pot[potH][potA], label="vs pot {}".format(potA), histtype="step", range=[0.43*normFactor,0.57*normFactor], bins=30)
            plt.xlabel("times pot {} plays at home".format(potH))
            plt.legend()
            plt.savefig(savePath + "prob_pot{}.png".format(potH))
            plt.clf()

        #print(mean_pot_v_pot)
        #print(stdv_pot_v_pot)

        trans = {}
        fig, ax = plt.subplots()
        trans[1] = Affine2D().translate(-0.2, 0.0) + ax.transData
        trans[2] = Affine2D().translate(-0.1, 0.0) + ax.transData
        trans[3] = Affine2D().translate(+0.1, 0.0) + ax.transData
        trans[4] = Affine2D().translate(+0.2, 0.0) + ax.transData
        if competition == "UECL":
            trans[5] = Affine2D().translate(-0.3, 0.0) + ax.transData
            trans[6] = Affine2D().translate(+0.3, 0.0) + ax.transData
        for potH in pots_indices:
            #print( pots_indices.keys() )
            #print( mean_pot_v_pot[potH] )
            #print( stdv_pot_v_pot[potH] )
            ax.errorbar( pots_indices.keys(), mean_pot_v_pot[potH], yerr=stdv_pot_v_pot[potH], 
                        marker='o', linestyle='none', label='Pot {}'.format(potH), transform=trans[potH])

        plt.xlabel("Away pot")
        plt.ylabel("probability at home")
        plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc='lower left', mode='expand',ncol=len(pots_indices), title='home pot')
        plt.savefig(savePath + 'summary_prob_pots.png')
        plt.clf()

        plt.close()
    
    plt.close()

        

                
