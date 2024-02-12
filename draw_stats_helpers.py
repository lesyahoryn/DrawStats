
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