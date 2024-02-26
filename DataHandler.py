import numpy as np
import pandas as pd
from collections import OrderedDict
import csv

class DataHandler:

    def __init__(self, provider, competition):
        self.setProvider(provider)
        self.setCompetition(competition)
        
        self.dataPath = ""
        self.metadataPath = ""

        self.clubs = OrderedDict()

        self.data = np.zeros(self.nteams, self.nteams )
    
    def setProvider(self, provider):
        self.provider = provider

    def setCompetition(self, competition):
        self.competition = competition
        self.setPotInfo()  ##pots are a function of competition
    
    def setDataPath(self, dataPath):
        self.dataPath = dataPath
        if self.provider == "AE":
            self.metadataPath = self.dataPath
        if self.provider == "Asolvo":
            self.metadataPath = self.dataPath #TODO change string

        self.getData()

    ## actually extract data from files
    def getData(self):
        if self.provider == "Pseudodata": #no team names in spreadsheet, and extra empty column at the end
            data = np.genfromtxt(self.dataPath, delimiter=',')
            data = data[:, ~np.isnan(data).any(axis=0)]
    
        else: #it's from an excel sheet with the names
            df = pd.read_csv(self.dataPath)
            if self.provider == "Asolvo":
                data = df.iloc[:, 1:].values
            elif self.provider == "AE":
                data = df.iloc[:, 4:].values
                data = df.iloc[:, 1:].values
        
        self.data = data
    
    ## get number of teams per pot and number of pots
    def setPotInfo(self):
        ## setup pots and teams per pot
        self.npots = 4
        self.nteamsperpot = 9
        if self.competition == 'UECL':
            self.npots = 6
            self.nteamsperpot = 6

        self.nteams = self.npots * self.nteamsperpot
    
    ## get club and pot info from metadata from providers
    def set_club_countries_pots(self):

        with open(self.metadataPath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None) # skip header

            for row in reader:
                club = row[0]
                country = row[1]
                pot = row[2]

                self.clubs[club] = { 'country': country, 'pot': int(pot) }

        
       