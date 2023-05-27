from leagueGetData import getLeagueDataOne

import pandas as pd


def getLeagueData(targets : pd.DataFrame):

    finalData = None

    for i in range(targets.shape[0]) :
        
        data = getLeagueDataOne(targets.loc[i, 'pseudo'], targets.loc[i, 'region'])

        if i == 0:
            finalData = pd.DataFrame(columns = list(data.keys()))
        
        finalData.loc[i,:] = data
    
    return data