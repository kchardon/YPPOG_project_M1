import pandas as pd
import os
from datetime import datetime

def cleanLeagueData(players : pd.DataFrame, path : str = None):
    """
    Processes and cleans game data for multiple players, combining it with personal information.

    This function takes as input a DataFrame containing player information and retrieves, processes, and cleans game data for each player. 
    It then returns a DataFrame that concatenates the cleaned game data with the personal information for each player.

    Parameters
    ----------
    players : pd.DataFrame
        A pandas DataFrame containing at least the following columns: [`puuid`, `pseudo`, `tagline`, `region`, `birthDate`].
        
    path : str
        The file path where each player's game data is saved as `puuid.csv`. Default is `'data/parsedData'`.

    Returns
    -------
    finalData : pd.DataFrame
        A pandas DataFrame containing the cleaned game data combined with the personal information for each player.
    """

    if path is None:
        path = "data/parsedData"
    
    finalData = players.copy()

    # For each player
    for puuid, birth_date in zip(players['puuid'], players['birthDate']):
        data = pd.read_csv(os.path.join(path, puuid + ".csv"), index_col=0)
        cleanData = cleanLeagueDataOne(data, birth_date)
        finalData = pd.merge(finalData, cleanData, on=['puuid'])
    return finalData


def getHourCat(data : pd.DataFrame, i : int):
    """
    Categorizes the hour into a time period (morning, afternoon, evening, or night) for a specific row in the DataFrame.

    This function updates the passed DataFrame by categorizing the value in the `'startHour'` column of the specified row in the `'startHourCat'` column.

    Parameters
    ----------
    data : pd.DataFrame
        A pandas DataFrame containing a column `'startHour'`, where the hour is stored.
        
    i : int
        The index of the row to process.

    Returns
    -------
    None
        The function modifies the DataFrame in place and does not return a value.
    """

    h = data.loc[i,'startHour']
    if h >= 6 and h < 12:
        # Morning
        data.loc[i,'startHourCat'] = 0
    elif h >= 12 and h < 17:
        # Afternoon
        data.loc[i,'startHourCat'] = 1
    elif h >= 17 and h < 21:
        # Evening
        data.loc[i,'startHourCat'] = 2
    else :
        # Night
        data.loc[i,'startHourCat'] = 3


def aggregateData(data : pd.DataFrame):
    """
    Aggregates game data for a single player based on various statistics.

    This function processes the input data to compute multiple features, including 
    the player's most frequent play times, champion preferences, lane preferences, 
    and game frequency distribution across different time categories.

    Parameters
    ----------
    data : pd.DataFrame
        A pandas DataFrame containing game data for a player.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing aggregated statistics for the player.
    """

    # Data to be computed
    newCol = {'puuid':0,
                # Day on which the player played the most
                'dayMostFreq':0,
                # Hour on which the player played the most
                'hourMostFreq':0,
                # Stats on game frequencies given day and time
                'monday':0,
                'tuesday':0,
                'wednesday':0,
                'thursday':0,
                'friday':0,
                'saturday':0,
                'sunday':0,
                'morning':0,
                'afternoon':0,
                'evening':0,
                'night':0,
                'mondayMorning':0,
                'tuesdayMorning':0,
                'wednesdayMorning':0,
                'thursdayMorning':0,
                'fridayMorning':0,
                'saturdayMorning':0,
                'sundayMorning':0,
                'mondayAfternoon':0,
                'tuesdayAfternoon':0,
                'wednesdayAfternoon':0,
                'thursdayAfternoon':0,
                'fridayAfternoon':0,
                'saturdayAfternoon':0,
                'sundayAfternoon':0,
                'mondayEvening':0,
                'tuesdayEvening':0,
                'wednesdayEvening':0,
                'thursdayEvening':0,
                'fridayEvening':0,
                'saturdayEvening':0,
                'sundayEvening':0,
                'mondayNight':0,
                'tuesdayNight':0,
                'wednesdayNight':0,
                'thursdayNight':0,
                'fridayNight':0,
                'saturdayNight':0,
                'sundayNight':0,
                # Stats on played champions (most used champion and number of different champions used)
                'championPref':None,
                'championCount':0,
                # When the player plays on another lane than the one on which he/she has to play
                'badLane':0,
                # Most played position (lane)
                'favPos':0,
                # Number of different positions (lanes) played
                'nbPos':0}
    
    # Keep the id
    newCol['puuid'] = data.loc[0,'puuid']

    # Data on which to apply the Mode function
    colMode = ["gameMode", "role", "offense", "defense", "flex", 'primaryStyle', 'secondaryStyle', 'primaryPerk0', 'primaryPerk1', 'primaryPerk2', 'primaryPerk3', 'secondaryPerk0', 'secondaryPerk1', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'summoner1Id', 'summoner2Id']
    # Data on which to apply the Max function
    colMax = ["summonerLevel"]
    # All other data will have the Mean function applied to it

    newCol['championPref'] = data.loc[:,'championId'].mode().values.flatten()[0]
    newCol['championCount'] = len(data.loc[:,"championId"].unique())

    newCol['hourMostFreq'] = data.loc[:,'startHourCat'].mode().values.flatten()[0]
    newCol['dayMostFreq'] = data.loc[:,'weekDay'].mode().values.flatten()[0]

    nrow = data.shape[0]

    for i,j in data.loc[:,'weekDay'].value_counts().items():
        if i == 0:
            newCol['monday'] = j / nrow
        if i == 1:
            newCol['tuesday'] = j / nrow
        if i == 2:
            newCol['wednesday'] = j / nrow
        if i == 3:
            newCol['thursday'] = j / nrow
        if i == 4:
            newCol['friday'] = j / nrow
        if i == 5:
            newCol['saturday'] = j / nrow
        if i == 6:
            newCol['sunday'] = j / nrow
    

    for i,j in data.loc[:,'startHourCat'].value_counts().items():
        if i == 0:
            newCol["morning"] = j / nrow
        if i == 1:
            newCol["afternoon"] = j / nrow
        if i == 2:
            newCol["evening"] = j / nrow
        if i == 3:
            newCol["night"] = j / nrow
    
    for i,j in data.loc[:,['startHourCat', 'weekDay']].value_counts().items():
        if i[0] == 0:
            if i[1] == 0:
                newCol["mondayMorning"] = j / nrow
            if i[1] == 1:
                newCol["tuesdayMorning"] = j / nrow
            if i[1] == 2:
                newCol["wednesdayMorning"] = j / nrow
            if i[1] == 3:
                newCol["thursdayMorning"] = j / nrow
            if i[1] == 4:
                newCol["fridayMorning"] = j / nrow
            if i[1] == 5:
                newCol["saturdayMorning"] = j / nrow
            if i[1] == 6:
                newCol["sundayMorning"] = j / nrow
        if i[0] == 1:
            if i[1] == 0:
                newCol["mondayAfternoon"] = j / nrow
            if i[1] == 1:
                newCol["tuesdayAfternoon"] = j / nrow
            if i[1] == 2:
                newCol["wednesdayAfternoon"] = j / nrow
            if i[1] == 3:
                newCol["thursdayAfternoon"] = j / nrow
            if i[1] == 4:
                newCol["fridayAfternoon"] = j / nrow
            if i[1] == 5:
                newCol["saturdayAfternoon"] = j / nrow
            if i[1] == 6:
                newCol["sundayAfternoon"] = j / nrow
        if i[0] == 2:
            if i[1] == 0:
                newCol["mondayEvening"] = j / nrow
            if i[1] == 1:
                newCol["tuesdayEvening"] = j / nrow
            if i[1] == 2:
                newCol["wednesdayEvening"] = j / nrow
            if i[1] == 3:
                newCol["thursdayEvening"] = j / nrow
            if i[1] == 4:
                newCol["fridayEvening"] = j / nrow
            if i[1] == 5:
                newCol["saturdayEvening"] = j / nrow
            if i[1] == 6:
                newCol["sundayEvening"] = j / nrow
        if i[0] == 3:
            if i[1] == 0:
                newCol["mondayNight"] = j / nrow
            if i[1] == 1:
                newCol["tuesdayNight"] = j / nrow
            if i[1] == 2:
                newCol["wednesdayNight"] = j / nrow
            if i[1] == 3:
                newCol["thursdayNight"] = j / nrow
            if i[1] == 4:
                newCol["fridayNight"] = j / nrow
            if i[1] == 5:
                newCol["saturdayNight"] = j / nrow
            if i[1] == 6:
                newCol["sundayNight"] = j / nrow
    
    newCol['badLane'] = len(data[(data['lane'] != 'NONE') & (data['lane'] != '') & (data['teamPosition'] != 'NONE') & (data['teamPosition'] != '') & (data['lane'] != data['teamPosition'])].loc[:,['lane', 'teamPosition']].value_counts()) / nrow
    newCol['favPos'] = data['teamPosition'].mode().values.flatten()[0]
    newCol['nbPos'] = len(data['teamPosition'].unique())
    
    # Drop the data on which we applied some modifications (that are stored in other columns)
    data = data.drop(['startHourCat', 'weekDay', 'championId', 'lane', 'teamPosition', 'puuid'], axis=1)

    new_col_data = pd.DataFrame.from_dict({0 : newCol}, orient='index')
    mode_data = data[colMode].mode()
    max_data = pd.DataFrame(data[colMax].max()).transpose()
    colMax.extend(colMode)
    mean_data = pd.DataFrame(data.drop(columns = colMax).mean()).transpose()

    return pd.concat([new_col_data, mode_data, max_data, mean_data], axis = 1)



def cleanLeagueDataOne(data : pd.DataFrame, birth_date: str):
    """
    Cleans and aggregates game data for a single player.

    This function takes as input a DataFrame containing a player's raw game data and cleans it. It aggregates the data to produce a summary, grouping by age category (`under 18` or `over 18`). 
    As a result, each player may have one or two rows depending on their age at the time of the games.

    Parameters
    ----------
    data : pd.DataFrame
        A pandas DataFrame containing the player's raw game data.
    birth_date : str
        The player's birth date in 'DD/MM/YYYY' format.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the cleaned and aggregated game data, grouped by age category.
    """
    # Birth date of the player
    birth_date = pd.to_datetime(birth_date, format='%d/%m/%Y')


    for i in range(data.shape[0]):

        # We convert time from epoch time to timestamp
        data.loc[i,'gameStartTimestamp'] = pd.Timestamp(datetime.fromtimestamp(data.loc[i,'gameStartTimestamp']/1000))

        # We get the weekday
        data.loc[i,'weekDay'] = data.loc[i,'gameStartTimestamp'].dayofweek

        # We get the hour of the game
        data.loc[i,'startHour'] = data.loc[i,'gameStartTimestamp'].hour

        # We get player's age at game time
        data.loc[i, 'age'] = (data.loc[i,'gameStartTimestamp'] - birth_date).days // 365
    
    # We get the time category of the game
    data.apply(lambda x : getHourCat(data, x.name), axis = 1)

    # Add age category
    data['ageCategory'] = data['age'].apply(lambda x: 'under_18' if x < 18 else 'over_18')

    # We delete data that are no more useful (we only use the time category and the weekday)
    data = data.drop(['gameStartTimestamp', 'startHour', 'age'], axis=1)

    # Group data by age
    data_under_18 = data[data['ageCategory'] == 'under_18']
    data_over_18 = data[data['ageCategory'] == 'over_18']

    # Aggregate data for each group
    aggregated_under_18 = aggregateData(data_under_18) if not data_under_18.empty else pd.DataFrame()
    aggregated_over_18 = aggregateData(data_over_18) if not data_over_18.empty else pd.DataFrame()

    # Concatenate results
    aggregated_result = pd.concat([aggregated_under_18, aggregated_over_18], ignore_index=True)

    return aggregated_result