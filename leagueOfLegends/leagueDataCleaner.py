import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
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
    
    cleaned_data_list = []

    # For each player
    for puuid, birth_date in zip(players['puuid'], players['birthDate']):
        data = pd.read_csv(os.path.join(path, puuid + ".csv"), index_col=0)
        cleanData = cleanLeagueDataOne(data, birth_date)
        
        # Add cleaned data to the list
        cleaned_data_list.append(cleanData)

    # Combine all cleaned data into a single dataframe
    cleaned_data = pd.concat(cleaned_data_list, axis=0)

    # Merge the players' personal information with the cleaned data
    finalData = pd.merge(players, cleaned_data, on='puuid', how='outer')

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
    conditions = [
        (data['startHour'] >= 6) & (data['startHour'] < 12),  # Morning, 0
        (data['startHour'] >= 12) & (data['startHour'] < 17),  # Afternoon, 1
        (data['startHour'] >= 17) & (data['startHour'] < 21),  # Evening, 2
        (data['startHour'] >= 21) | (data['startHour'] < 6)    # Night, 3
    ]
    categories = [0, 1, 2, 3]

    data['startHourCat'] = np.select(conditions, categories, default=np.nan)


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

    # New features to be computed
    newCol = {}
    

    # Keep the id
    newCol['puuid'] = data.loc[0,'puuid']


    # Stats on played champions (most used champion and number of different champions used)
    newCol['championPref'] = data.loc[:,'championId'].mode().values.flatten()[0]
    newCol['championCount'] = len(data.loc[:,"championId"].unique())


    # Hour on which the player played the most
    newCol['hourMostFreq'] = data.loc[:,'startHourCat'].mode().values.flatten()[0]

    # Day on which the player played the most
    newCol['dayMostFreq'] = data.loc[:,'weekDay'].mode().values.flatten()[0]


    # Stats on game frequencies given day and time
    nrow = data.shape[0]

    # Days of the week and time categories
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    times = ["morning", "afternoon", "evening", "night"]

    # Initialize all day and time combinations to 0
    newCol.update({day: 0 for day in days})
    newCol.update({time: 0 for time in times})
    newCol.update({f"{day}{time.capitalize()}": 0 for day in days for time in times})

    # Calculate proportions for weekDay
    for i, j in data['weekDay'].value_counts().items():
        newCol[days[int(i)]] = j / nrow

    # Calculate proportions for startHourCat
    for i, j in data['startHourCat'].value_counts().items():
        newCol[times[int(i)]] = j / nrow

    # Calculate proportions for combinations of startHourCat and weekDay
    for (time_cat, day), count in data[['startHourCat', 'weekDay']].value_counts().items():
        newCol[f"{days[int(day)]}{times[int(time_cat)].capitalize()}"] = count / nrow


    # When the player plays on another lane than the one on which he/she has to play
    newCol['badLane'] = len(data[(data['lane'] != 'NONE') & (data['lane'] != '') & (data['teamPosition'] != 'NONE') & (data['teamPosition'] != '') & (data['lane'] != data['teamPosition'])].loc[:,['lane', 'teamPosition']].value_counts()) / nrow


    # Most played position (lane)
    newCol['favPos'] = data['teamPosition'].mode().values.flatten()[0]


    # Number of different positions (lanes) played
    newCol['nbPos'] = len(data['teamPosition'].unique())
    

    # Drop the data on which we applied some modifications (that are stored in other columns)
    data = data.drop(['startHourCat', 'weekDay', 'championId', 'lane', 'teamPosition', 'puuid'], axis=1)


    # Data on which to apply the Mode function
    colMode = ['ageCategory', "gameMode", "role", "offense", "defense", "flex", 'primaryStyle', 'secondaryStyle', 'primaryPerk0', 'primaryPerk1', 'primaryPerk2', 'primaryPerk3', 'secondaryPerk0', 'secondaryPerk1', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'summoner1Id', 'summoner2Id']
    
    # Data on which to apply the Max function
    colMax = ["summonerLevel"]
    
    # All other data will have the Mean function applied to it

    new_col_data = pd.DataFrame.from_dict({0 : newCol}, orient='index')
    mode_data = data[colMode].mode().head(1) # To keep the first one if several values are tied (see how to deal with this)
    max_data = pd.DataFrame(data[colMax].max()).transpose()
    colMax.extend(colMode)
    mean_data = pd.DataFrame(data.drop(columns = colMax).mean()).transpose()


    # Concat all features
    finalData = pd.concat([new_col_data, mode_data, max_data, mean_data], axis = 1)


    # I handle string features
    # Possible categories
    favPos_categories = ['UTILITY', 'MIDDLE', 'JUNGLE', 'BOTTOM', 'TOP', 'APEX', None]
    role_categories = ['SUPPORT', 'SOLO', 'CARRY', 'NONE', 'DUO']
    gameMode_categories = [
        "CLASSIC", "ODIN", "ARAM", "TUTORIAL", "URF", "DOOMBOTSTEEMO", "ONEFORALL",
        "ASCENSION", "FIRSTBLOOD", "KINGPORO", "SIEGE", "ASSASSINATE", "ARSR",
        "DARKSTAR", "STARGUARDIAN", "PROJECT", "GAMEMODEX", "ODYSSEY", "NEXUSBLITZ",
        "ULTBOOK"
    ]

    # Initialize the OneHotEncoder
    encoder = OneHotEncoder(categories=[favPos_categories, role_categories, gameMode_categories], handle_unknown='ignore', sparse=False)

    # Fit and transform the categorical data
    encoded_array = encoder.fit_transform(finalData[['favPos', 'role', 'gameMode']])

    # Create a DataFrame for the encoded columns
    encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out())

    # Concatenate the original numerical columns with the encoded columns
    finalData = pd.concat([finalData.drop(columns=['favPos', 'role', 'gameMode']), encoded_df], axis=1)


    return finalData



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
    data_under_18 = data[data['ageCategory'] == 'under_18'].reset_index(drop=True)
    data_over_18 = data[data['ageCategory'] == 'over_18'].reset_index(drop=True)

    # Aggregate data for each group
    aggregated_under_18 = aggregateData(data_under_18) if not data_under_18.empty else pd.DataFrame()
    aggregated_over_18 = aggregateData(data_over_18) if not data_over_18.empty else pd.DataFrame()

    # Concatenate results
    aggregated_result = pd.concat([aggregated_under_18, aggregated_over_18], ignore_index=True)

    return aggregated_result