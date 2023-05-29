from leagueGetData import getLeagueDataOne

import pandas as pd


def getLeagueData(targets : pd.DataFrame):

    finalData = None
    
    # For each player
    for i in range(targets.shape[0]) :
        
        # Get the features
        data = getLeagueDataOne(targets.loc[i, 'pseudo'], targets.loc[i, 'region'])

        # Add it to the final dataFrame
        if i == 0:
            finalData = pd.DataFrame(columns = list(data.keys()))
        finalData.loc[i,:] = data.loc[0,:]
    
    # Keep the id in the target dataFrame
    targets['puuid'] = finalData['puuid']
    
    return finalData