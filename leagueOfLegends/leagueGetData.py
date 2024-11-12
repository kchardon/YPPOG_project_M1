from riotwatcher import LolWatcher, RiotWatcher, ApiError
from riot_api import key

from leagueDataParser import parseLeagueData
from leagueDataCleaner import cleanLeagueData

import pandas as pd
import os

dataFolder = "data"
matchFolder = os.path.join(dataFolder,"matchLists")
parsedDataFolder = os.path.join(dataFolder, "parsedData")


def getLeagueDataOne(pseudo : str, tag_line : str, region : str):

    # API connection
    lol = LolWatcher(key)
    riot = RiotWatcher(key)
    
    # Get the data of the player
    player = riot.account.by_riot_id(region, pseudo, tag_line)
    puuid = player['puuid']

    # Look if the parsed data is already saved
    file_name_parsed = puuid + ".csv"
    matchData = None

    if os.path.exists(os.path.join(parsedDataFolder, file_name_parsed)):
        # If it exists, we get it and return it
        matchData = pd.read_csv(os.path.join(parsedDataFolder, file_name_parsed), index_col=0)

        print("Got parsed data from os for " + pseudo)
    
    else:
        # Else we retrieve it and save it

        # Look if the matchs list is already saved
        file_name = puuid + ".txt"
        matchs = []

        if os.path.exists(os.path.join(matchFolder, file_name)):
            # If it exists, we get it
            with open(os.path.join(matchFolder, file_name), 'r') as f:
                for line in f:
                    matchs.extend(line.split(','))
            
            print("Got matchs list from os for " + pseudo)

        else :
            # Else we retrieve it and save it

            # Get all the matchs played by the player
            matchs = lol.match.matchlist_by_puuid(region, puuid, count = 100)
            i = 100

            while (lol.match.matchlist_by_puuid(region, puuid, count = 100, start = i) != []):
                matchs.extend(lol.match.matchlist_by_puuid(region, puuid, count = 100, start = i))
                i = i + 100
            
            # Save matchs list
            with open(os.path.join(matchFolder, file_name), 'w') as f:
                f.write(','.join(matchs))
            
            print("Saved matchs list for " + pseudo)

        deleted = 0

        # For each match
        for j,i in enumerate(matchs):
            # Get the data
            p = lol.match.by_id(region, i)
            
            # If the match is not a Classic or Aram game or has been played before the 10th of February 2022 : deleted
            if (p['info']['gameMode'] != 'CLASSIC' and p['info']['gameMode'] != 'ARAM') or (p['info']['gameStartTimestamp'] <= 1644533999000) :
                deleted += 1
            
            # Else we parse the data and keep it
            else :
                p = parseLeagueData(p, puuid)
                if j - deleted == 0:
                    matchData = pd.DataFrame(columns = list(p.keys()))
                matchData.loc[j - deleted,:] = p
        
        # We save the dataFrame
        matchData.to_csv(os.path.join(parsedDataFolder, file_name_parsed))

        print("Saved parsed data for " + pseudo)

    print(matchData)
    # When all the matchs have been parsed, we clean them and return the dataFrame
    return cleanLeagueData(matchData)
