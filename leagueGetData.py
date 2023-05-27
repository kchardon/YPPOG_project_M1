from riotwatcher import LolWatcher, ApiError
from riot_api import key

from leagueDataParser import parseLeagueData
from leagueDataCleaner import cleanLeagueData

import pandas as pd


def getLeagueDataOne(pseudo : str, region : str):

    lol = LolWatcher(key)
    
    player = lol.summoner.by_name(region,pseudo)
    puuid = player['puuid']

    matchs = lol.match.matchlist_by_puuid(region, puuid, count = 100)
    i = 100

    while (lol.match.matchlist_by_puuid(region, puuid, count = 100, start = i) != []):
        matchs.extend(lol.match.matchlist_by_puuid(region, puuid, count = 100, start = i))
        i = i + 100
    
    matchData = None

    for j,i in enumerate(matchs):
        p = lol.match.by_id(region, i)
        p = parseLeagueData(p, puuid)
        if j == 0:
            matchData = pd.DataFrame(columns = list(p.keys()))
        matchData.loc[j,:] = p
    
    return cleanLeagueData(matchData)
