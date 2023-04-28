import pandas as pd

def parseLeagueData(data : dict, puuid):
    data = data['info']
    participants = data['participants']
    data.pop('participants', None)
    data.pop('teams', None)

    for p in participants:
        if p['puuid'] == puuid:
            participants = p
    
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

    return data

    