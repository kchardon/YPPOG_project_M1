import pandas as pd

def parseLeagueData(data : dict, puuid : str):
    """
    Parses raw API data for a specific player.

    This function takes as input the raw data from the API and the PUUID of the player being analyzed. It returns the player's parsed game data.

    Parameters
    ----------
    data : dict
        The raw data retrieved from the API for the player.
        
    puuid : str
        The PUUID of the player.

    Returns
    -------
    dict
        The parsed game data for the player.
    """

    # We flatten the whole dictionnary, keep the data of the player we are working on and delete data that is not useful

    data = data['info']
    participants = data['participants']
    data.pop('participants', None)

    for p in participants:
        if p['puuid'] == puuid:
            participants = p
            break
    
    challenges = participants['challenges']
    perks = participants['perks']
    participants.pop('challenges', None)
    participants.pop('perks', None)

    stats = perks['statPerks']

    primarySelections = perks['styles'][0]['selections']
    secondarySelections = perks['styles'][1]['selections']

    data.update(participants)
    data.update(challenges)
    data.update(stats)

    data['primaryStyle'] = perks['styles'][0]['style']
    data['secondaryStyle'] = perks['styles'][1]['style']

    data['primaryPerk0'] = primarySelections[0]['perk']
    data['primaryVar10'] = primarySelections[0]['var1']
    data['primaryVar20'] = primarySelections[0]['var2']
    data['primaryVar30'] = primarySelections[0]['var3']

    data['primaryPerk1'] = primarySelections[1]['perk']
    data['primaryVar11'] = primarySelections[1]['var1']
    data['primaryVar21'] = primarySelections[1]['var2']
    data['primaryVar31'] = primarySelections[1]['var3']

    data['primaryPerk2'] = primarySelections[2]['perk']
    data['primaryVar12'] = primarySelections[2]['var1']
    data['primaryVar22'] = primarySelections[2]['var2']
    data['primaryVar32'] = primarySelections[2]['var3']

    data['primaryPerk3'] = primarySelections[3]['perk']
    data['primaryVar13'] = primarySelections[3]['var1']
    data['primaryVar23'] = primarySelections[3]['var2']
    data['primaryVar33'] = primarySelections[3]['var3']

    data['secondaryPerk0'] = secondarySelections[0]['perk']
    data['secondaryVar10'] = secondarySelections[0]['var1']
    data['secondaryVar20'] = secondarySelections[0]['var2']
    data['secondaryVar30'] = secondarySelections[0]['var3']

    data['secondaryPerk1'] = secondarySelections[1]['perk']
    data['secondaryVar11'] = secondarySelections[1]['var1']
    data['secondaryVar21'] = secondarySelections[1]['var2']
    data['secondaryVar31'] = secondarySelections[1]['var3']

    # List of columns to remove
    columns_to_remove = [
    'teams', 'gameCreation', 'gameEndTimestamp', 'gameId', 'gameName', 'gameVersion', 
    'mapId', 'missions', 'endOfGameResult', 'platformId', 'queueId', 'tournamentCode', 
    'championName', 'individualPosition', 'participantId', 'profileIcon', 'riotIdGameName', 
    'riotIdTagline', 'summonerId', 'summonerName', 'teamId', 'timePlayed', 'gameType', 
    'gameDuration', 'championTransform', 'playerAugment1', 'playerAugment2', 'playerAugment3', 
    'playerAugment4', 'playerSubteamId', 'subteamPlacement', 'visionClearedPings', 'mythicItemUsed', 
    'legendaryItemUsed', 'PlayerScore0', 'PlayerScore1', 'PlayerScore10', 'PlayerScore11', 
    'PlayerScore2', 'PlayerScore3', 'PlayerScore4', 'PlayerScore5', 'PlayerScore6', 
    'PlayerScore7', 'PlayerScore8', 'PlayerScore9', 'playerAugment5', 'playerAugment6', 
    'retreatPings', 'HealFromMapSources', 'InfernalScalePickup', 'SWARM_DefeatAatrox', 
    'SWARM_DefeatBriar', 'SWARM_DefeatMiniBosses', 'SWARM_EvolveWeapon', 'SWARM_Have3Passives', 
    'SWARM_KillEnemy', 'SWARM_PickupGold', 'SWARM_ReachLevel50', 'SWARM_Survive15Min', 
    'SWARM_WinWith5EvolvedWeapons', 'fistBumpParticipation', 'voidMonsterKill'
    ]

    # Iterate through the list and pop the columns
    for column in columns_to_remove:
        data.pop(column, None)  

    return data

    