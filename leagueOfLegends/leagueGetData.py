import pandas as pd
import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from riot_api import key

from leagueDataParser import parseLeagueData


def getLeagueData(targets : pd.DataFrame, dataFolder : str = None):
    """
    Processes a pandas DataFrame containing player information and saves relevant match and parsed data.

    This function takes as input a pandas DataFrame containing the `Pseudo`, `TagLine`, and `Region` for one or more players. 
    It saves the match list and parsed data to `data/matchLists/puuid.txt` and `data/parsedData/puuid.csv` for each player.
    It returns a DataFrame with information necessary to retrieve each player's data.

    Parameters
    ----------
    targets : pd.DataFrame
        A pandas DataFrame containing at least the following columns: [`pseudo`, `tagline`, `region`].
    
    dataFolder : str
        A path to store the players' data. Default is `'data'`.

    Returns
    -------
    targetID : pd.DataFrame
        A pandas DataFrame with the `Pseudo`, `TagLine`, `Region` and `PUUID` for each player.
    """

    # Create the folder where we will store data
    if dataFolder is None:
        dataFolder = "data"
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
    
    # For each player
    for i in range(targets.shape[0]) :
        
        # Get the features
        puuid = getLeagueDataOne(targets.loc[i, 'pseudo'], targets.loc[i, 'tagline'], targets.loc[i, 'region'], dataFolder)

        # Add it to the final DataFrames
        if i == 0:
            targetID = pd.DataFrame(columns = ['puuid', 'pseudo', 'tagline', 'region'])
    
        # Keep the id with the player information
        targetID.loc[i, 'puuid'] = puuid
        targetID.loc[i, ['pseudo', 'tagline', 'region']] = targets.loc[i, ['pseudo', 'tagline', 'region']]
    
    return targetID



def getLeagueDataOne(pseudo : str, tag_line : str, region : str, dataFolder : str):
    """
    Retrieves a player's PUUID based on their Pseudo, TagLine, and Region, and saves their raw parsed game data.

    This function takes as input the `Pseudo`, `TagLine`, and `Region` of a player, saves their match list and parsed data to 
    `data/matchLists/puuid.txt` and `data/parsedData/puuid.csv`, and returns the player's PUUID.

    Parameters
    ----------
    pseudo : str
        The Pseudo of the player.
        
    tag_line : str
        The TagLine of the player.
        
    region : str
        The Region of the player.
    
    dataFolder : str
        A path to store the players' data.

    Returns
    -------
    str
        The player's PUUID.
    """
    # Create the folders where we will store data
    matchFolder = os.path.join(dataFolder,"matchLists")
    parsedDataFolder = os.path.join(dataFolder, "parsedData")
    if not os.path.exists(matchFolder):
        os.makedirs(matchFolder)
    if not os.path.exists(parsedDataFolder):
        os.makedirs(parsedDataFolder)

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

        print("Got parsed data from os for " + pseudo + "#" + tag_line)

        # Verify whether it's up to date
        new_matches = update_match_list(lol, region, puuid, matchFolder)

        if new_matches:
            print("Added new matches :", new_matches)
            
            deleted = 0
            size = matchData.shape[0]
            # For each match
            for j,i in enumerate(new_matches):
                # Get the data
                try:
                    p = lol.match.by_id(region, i)

                    # If the match is not a Classic or Aram game or has been played before the 10th of February 2022 : deleted
                    if (p['info']['gameMode'] != 'CLASSIC' and p['info']['gameMode'] != 'ARAM') or (p['info']['gameStartTimestamp'] <= 1644533999000) :
                        deleted += 1
                    
                    # Else we parse the data and keep it
                    else :
                        p = parseLeagueData(p, puuid)
                        matchData.loc[j + size - deleted,:] = p

                except ApiError as err:
                    print('Error', err.response.status_code, 'for match', i, 'for', pseudo + "#" + tag_line)
            
            # We save the dataFrame
            matchData.to_csv(os.path.join(parsedDataFolder, file_name_parsed))


        else :
            print("List of matchs up to date.")
    
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
            
            print("Got matchs list from os for " + pseudo + "#" + tag_line)

            # Verify whether it's up to date
            new_matches = update_match_list(lol, region, puuid, matchFolder)

            if new_matches:
                print("Added new matches :", new_matches)
            else :
                print("List of matchs up to date.")

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
            
            print("Saved matchs list for " + pseudo + "#" + tag_line)

        deleted = 0

        # For each match
        for j,i in enumerate(matchs):
            # Get the data
            try:
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

            except ApiError as err:
                print('Error', err.response.status_code, 'for match', i, 'for', pseudo + "#" + tag_line)
        
        # We save the dataFrame
        matchData.to_csv(os.path.join(parsedDataFolder, file_name_parsed))

        print("Saved parsed data for " + pseudo + "#" + tag_line)

    # When the data is saved, we return the puuid
    return puuid


def update_match_list(lol: LolWatcher, region: str, puuid: str, match_folder: str):
    """
    Checks if the saved match list is up to date with the API.
    Updates the list if new matches are found and returns the new matches.

    New matches are placed at the beginning of the list, preserving order.

    Parameters
    ----------
    lol : LolWatcher
        LolWatcher instance for API requests.
        
    region : str
        Region code.
        
    puuid : str
        Player unique identifier.
    
    match_folder : str
        Path to the folder storing match lists.

    Returns
    -------
    list
        List of new match IDs.
    """
    file_path = os.path.join(match_folder, puuid + ".txt")
    saved_matches = []

    # Get stored matchs list
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            saved_matches = f.read().split(',')

    all_new_matches = []
    start = 0

    while True:
        new_matches = lol.match.matchlist_by_puuid(region, puuid, count=100, start=start)
        if not new_matches:
            break
        
        # Identify new matches not in saved list
        unique_new = [m for m in new_matches if m not in saved_matches]
        if not unique_new:
            break

        all_new_matches.extend(unique_new)
        start += 100

    if all_new_matches:
        all_matches = all_new_matches + saved_matches # New matches first
        with open(file_path, 'w') as f:
            f.write(','.join(all_matches))
        return all_new_matches

    return []