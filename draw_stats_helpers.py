import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 

### import clubs, countries, pots from csv
## need to keep clubs in order
def set_club_countries_clubs(competition):
    metadataDir = './metadata/'
    
    clubs = OrderedDict()

    with open(metadataDir + competition+'.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0] == "Team": continue ## skip header row

            club = row[0]
            country = row[1]
            pot = row[2]

            clubs[club] = { 'country': country, 'pot': pot }
    return clubs
       
def getData(inpName, isPseudodata=False):
    ## import data and set up matrices, transpose used for adding/subtracting across the diagonal
    #from excel with labels
    if isPseudodata: #no team names in spreadsheet, and extra empty column at the end
        data = np.genfromtxt(inpName, delimiter=',')
        data = data[:, ~np.isnan(data).any(axis=0)]
    
    else: #it's from an excel sheet with the names
        df = pd.read_csv(inpName)
        data = df.iloc[:, 1:].values

    return data



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

def plot(bins, params, savePath, xlineloc=-999, range=[], xlabel=""):

    x_values = np.linspace(min(bins), max(bins), 1000)

    plt.plot(x_values, gaussian(x_values, *params), color='red', linestyle='-', label='Fit')
    
    plt.text(0.02,0.90, "mean: {} \nsigma: {}".format(round(params[1], 6), round(params[2], 6)), transform=plt.gca().transAxes)

    if xlineloc != -999 : plt.axvline(x=xlineloc, color='black')

    if len(range) != 0: plt.xlim(range)
    plt.xlabel(xlabel)
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


def make2DTeamPlot(workingData, names, redTxtCondition, outPath, redTxtPrec='.0f', cbarLabel=""):
    ## do 2d array of p values per matchup
    plt.figure(figsize=(20,20))
    plt.imshow(abs(workingData), cmap='Greens')
    warningVal = 400

    for i in range(workingData.shape[0]):
        for j in range(workingData.shape[1]):
            if i >= j: continue #only work with cells above diagonal, also skip diagonal bc who cares
            if np.isnan( workingData[i][j] ) and np.isnan( workingData[j][i] ): continue #skip pairings that are illegal
            if eval(redTxtCondition):
                plt.text(j, i, f'{workingData[i, j]: {redTxtPrec}}', ha='center', va='center', color='red')
            else:
                plt.text(j, i, f'{workingData[i, j]: {redTxtPrec}}', ha='center', va='center', color='black')

    # add team names as x and y ticks
    plt.xticks(np.arange(0,len(names),1), labels=names, fontsize=12, rotation=90)
    plt.yticks(np.arange(0,len(names),1), labels=names, fontsize=12)

    plt.tick_params(axis='x', labeltop=True, labelbottom=False, bottom=False, top=True)
    plt.tick_params(axis='y', labelright=False, labelleft=True, left=True, right=False)

    # Add color bar
    cbar = plt.colorbar(shrink=0.7, location='right', label=cbarLabel)

    plt.savefig(outPath)




##old/hardcoded version -- currently needed for binomial_test.py and probability_plots.py
### 
### dictionary of clubs
###
clubs = {}
##these are in the order of the data matrix
clubs["UCL"] = ['Liverpool FC', 'Manchester City FC',
       'Manchester United FC', 'FC Barcelona', 'Real Madrid CF', 'Sevilla FC',
       'Paris Saint Germain', 'FC Bayern München', 'FC Internazionale Milano',
       'FC Salzburg', 'Arsenal FC', 'Club Atlético de Madrid',
       'Borussia Dortmund', 'RB Leipzig', 'SSC Napoli', 'FC Porto',
       'SL Benfica', 'FC Shakhtar Donetsk', 'FC Copenhagen', 'AC Milan',
       'Atalanta BC', 'SS Lazio', 'Feyenoord', 'PSV Eindhoven', 'SC Braga',
       'FK Crvena Zvezda', 'BSC Young Boys', 'Qarabağ FK', 'Royal Antwerp FC',
       'Newcastle United FC', 'Real Sociedad de Fútbol',
       'Olympique de Marseille', 'RC Lens', '1. FC Union Berlin', 'Celtic FC',
       'Galatasaray A.Ş.']

clubs["UEL"] = ['GNK Dinamo', 'SK Slavia Praha',
       'West Ham United FC', 'Villarreal CF', 'Bayer 04 Leverkusen', 'AS Roma',
       'AFC Ajax', 'Sporting Clube de Portugal', 'Rangers FC', 'LASK',
       'Real Betis Balompié', 'LOSC Lille', 'Stade Rennais FC',
       'Olympiacos FC', 'Ferencvárosi TC', 'AZ Alkmaar', 'Molde FK',
       'FC Dynamo Kyiv', 'SK Rapid Wien', 'R. Union Saint-Gilloise',
       'AC Sparta Praha', 'Aston Villa FC', 'Brighton & Hove Albion FC',
       'SC Freiburg', 'Maccabi Haifa FC', 'ACF Fiorentina',
       'FC Sheriff Tirsapol', 'SK Strum Graz', 'Aris Limassol', 'Toulouse FC',
       'AEK Athens FC', 'Panathinaikos FC', 'Raków Czestochowa',
       'FK TSC Bačka Topola', 'Servette FC', 'BK Häcken ']

clubs["UECL"] = ['Club Brugge', 'KAA Gent', 'Tottenham Hotspur',
       'Eintracht Frankfurt', 'FC Basel 1893', 'Fenerbahce SK',
       'FC Midtjylland', 'AS Monaco', 'PAOK FC', 'Maccabi Tel-Aviv FC',
       'CFR 1907 Cluj', 'SK Slovan Bratislava', 'KRC Genk',
       'PFC Ludogorets 1945', 'FC Viktoria Plzen', 'CA Osasuna', 'FC Bologna',
       'FK Bodo/Glimt', 'HJK Helsinki', 'FC Astana', 'FK Zalgiris Vilnius',
       'Legia Warszawa', 'Besiktas JK', 'FC Zorya Luhansk', 'HSK Zrinjski',
       'FC Flora Tallinn', 'Ki Klaksvik', 'FC Spartak Trnava',
       'NK Olimpija Ljubljana', 'Dnipro-1', 'FC Nordsjaelland', 'Breidablik',
       'FC Ballkani', 'Aberdeen FC', 'FK Cukaricki', 'FC Lugano']


### 
### dictionary of clubs per pot
###

pots = {}
pots["UCL"] = {}
pots["UCL"][1] = ['Liverpool FC', 'Manchester City FC', 'Manchester United FC', 
                  'FC Barcelona', 'Real Madrid CF', 'Sevilla FC', 
                  'FC Bayern München', 'Paris Saint Germain', 'FC Internazionale Milano']
pots["UCL"][2] = ['Borussia Dortmund', 'RB Leipzig', 'SSC Napoli', 
                  'FC Porto', 'SL Benfica', 'FC Shakhtar Donetsk', 
                  'Club Atlético de Madrid', 'Arsenal FC', 'FC Salzburg' ]
pots["UCL"][3] = [ 'Atalanta BC', 'SS Lazio', 'Feyenoord', 
                   'SC Braga', 'AC Milan', 'FK Crvena Zvezda',
                   'PSV Eindhoven', 'FC Copenhagen', 'BSC Young Boys']
pots["UCL"][4] = ['Newcastle United FC', 'Real Sociedad de Fútbol', 'Olympique de Marseille',
                  'Galatasaray A.Ş.', 'Celtic FC',  'Qarabağ FK',
                  '1. FC Union Berlin', 'Royal Antwerp FC', 'RC Lens' ]

pots["UEL"] = {}
pots["UEL"][1] = [ 'GNK Dinamo', 'SK Slavia Praha','West Ham United FC',
                  'Villarreal CF', 'Bayer 04 Leverkusen', 'AS Roma',
                  'AFC Ajax', 'Sporting Clube de Portugal', 'Rangers FC' ]
pots['UEL'][2] = [ 'LASK', 'Real Betis Balompié', 'LOSC Lille', 
                  'Stade Rennais FC', 'Olympiacos FC', 'Ferencvárosi TC',
                  'AZ Alkmaar', 'Molde FK', 'FC Dynamo Kyiv']
pots['UEL'][3] = [ 'AC Sparta Praha', 'Aston Villa FC', 'Brighton & Hove Albion FC',
                  'SC Freiburg', 'Maccabi Haifa FC', 'ACF Fiorentina',
                  'FC Sheriff Tirsapol', 'R. Union Saint-Gilloise','SK Rapid Wien']
pots['UEL'][4] = [ 'SK Strum Graz', 'Aris Limassol', 'Toulouse FC',
                  'AEK Athens FC', 'Panathinaikos FC', 'Raków Czestochowa',
                   'FK TSC Bačka Topola', 'Servette FC', 'BK Häcken ' ]

pots['UECL'] = {}
pots['UECL'][1] = ['Club Brugge', 'KAA Gent', 'Tottenham Hotspur',
                   'Eintracht Frankfurt', 'FC Basel 1893', 'Fenerbahce SK']
pots['UECL'][2] = ['FC Midtjylland', 'AS Monaco', 'PAOK FC',
                    'Maccabi Tel-Aviv FC', 'CFR 1907 Cluj', 'SK Slovan Bratislava' ]
pots['UECL'][3] = [ 'FC Viktoria Plzen', 'CA Osasuna', 'FC Bologna',
                    'FK Bodo/Glimt','PFC Ludogorets 1945','KRC Genk']
pots['UECL'][4] = [ 'FC Zorya Luhansk', 'Legia Warszawa', 'Besiktas JK',
                    'HJK Helsinki', 'FC Astana', 'FK Zalgiris Vilnius']
pots['UECL'][5] = [ 'FC Flora Tallinn', 'Ki Klaksvik', 'FC Spartak Trnava',
                   'NK Olimpija Ljubljana', 'Dnipro-1','HSK Zrinjski']
pots['UECL'][6] = [ 'Aberdeen FC', 'FK Cukaricki', 'FC Lugano',
                   'FC Nordsjaelland', 'Breidablik','FC Ballkani']

countries = {}




colors=['blue','green','red','orange','purple','blue','yellow']




## get the list of clubs and 
def get_clubs_pots_indices(competition):
    pots_indices = {}

    if competition not in clubs.keys():
        print("ERROR: invalid competition: ", competition)
        return [], []

    pots_indices = {}

    for pot in pots[competition]:
        pots_indices[pot] = []
            
        for team in pots[competition][pot]:
            idx = clubs[competition].index(team)
            pots_indices[pot].append( idx )
    
    return clubs[competition], pots_indices