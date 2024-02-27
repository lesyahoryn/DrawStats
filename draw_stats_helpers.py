import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 


##set some common stuff
def init():
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    np.seterr(divide='ignore', invalid='ignore')

##################
## Some data formatting helpers
##################
    
## get string that corresponds to big country pairing
def bigCountryFillString( country1, country2, combinations):
    for combination in combinations:
        if country1 in combination and country2 in combination: 
            return combination
    
    print("INVALID COMBINATION", country1, country2)
    return ""

## silly little cheating to make the 2d plots look better by removing the data from below the diagonal
def emptyBottomDiagonal(data):
    dataZ = np.zeros((data.shape[0], data.shape[1]))
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if i >= j: continue
            
            if np.isnan( data[i][j] ): dataZ[i][j] = 0
            else: dataZ[i][j] = data[i][j]
    
    return dataZ

## take only top half of the diagonal and make a list to dump into plt.hist()
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


##############
## Plot and fit helpers
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

def plot(bins, params, savePath, xlineloc=-999, range=[], xlabel="", ymax=-999, extratext = ""):

    x_values = np.linspace(min(bins), max(bins), 1000)

    plt.plot(x_values, gaussian(x_values, *params), color='red', linestyle='-', label='Fit')
    
    plt.text(0.02,0.90, "mean: {} \nsigma: {}".format(round(params[1], 6), round(params[2], 6)), transform=plt.gca().transAxes)
    if extratext != "":
        plt.text(0.02,0.70, extratext, transform=plt.gca().transAxes, color='red')

    if xlineloc != -999 : plt.axvline(x=xlineloc, color='black')

    if len(range) != 0: plt.xlim(range)
    if ymax != -999: plt.ylim(0, ymax)
    
    plt.xlabel(xlabel)
    plt.legend()
    plt.savefig(savePath)



def make2DTeamPlot(workingData, names, redTxtCondition, outPath, nteamsperpot, npots, redTxtPrec='.0f', cbarLabel="", clim=[], fontsize=12):
    ## do 2d array of p values per matchup
    plt.figure(figsize=(20,20))
    if clim != []:
        plt.imshow(abs(workingData), cmap='Greens', vmin = clim[0], vmax = clim[1])
    else:
        plt.imshow(abs(workingData), cmap='Greens')

    for i in range(workingData.shape[0]):
        for j in range(workingData.shape[1]):
            if i >= j: continue #only work with cells above diagonal, also skip diagonal bc who cares
            if np.isnan( workingData[i][j] ) and np.isnan( workingData[j][i] ): continue #skip pairings that are illegal
            if eval(redTxtCondition):
                plt.text(j, i, f'{workingData[i, j]: {redTxtPrec}}', ha='center', va='center', color='red', fontsize=fontsize)
            else:
                plt.text(j, i, f'{workingData[i, j]: {redTxtPrec}}', ha='center', va='center', color='black', fontsize=fontsize)

    # add team names as x and y ticks
    plt.xticks(np.arange(0,len(names),1), labels=names, fontsize=12, rotation=90)
    plt.yticks(np.arange(0,len(names),1), labels=names, fontsize=12)

    for i in range(1, npots):
        plt.axvline(i * nteamsperpot - 0.5, color='black', linestyle='-', linewidth=1)
        plt.axhline(i * nteamsperpot - 0.5, color='black', linestyle='-', linewidth=1)


    plt.tick_params(axis='x', labeltop=True, labelbottom=False, bottom=False, top=True)
    plt.tick_params(axis='y', labelright=False, labelleft=True, left=True, right=False)

    # Add color bar
    cbar = plt.colorbar(shrink=0.7, location='right', label=cbarLabel)

    plt.savefig(outPath)
