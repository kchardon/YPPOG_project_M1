import pandas as pd
from datetime import datetime


def getHourCat(data : pd.DataFrame, i : int):
    h = data.loc[i,'startHour']
    if h >= 6 and h < 12:
        data.loc[i,'startHourCat'] = 0
    elif h >= 12 and h < 17:
        data.loc[i,'startHourCat'] = 1
    elif h >= 17 and h < 21:
        data.loc[i,'startHourCat'] = 2
    else :
        data.loc[i,'startHourCat'] = 3


def cleanLeagueData(data : pd.DataFrame):
    for i in range(data.shape[0]):
        data.loc[i,'gameStartTimestamp'] = pd.Timestamp(datetime.fromtimestamp(data.loc[i,'gameStartTimestamp']/1000))
        data.loc[i,'weekDay'] = data.loc[i,'gameStartTimestamp'].dayofweek
        data.loc[i,'startHour'] = data.loc[i,'gameStartTimestamp'].hour
    data.apply(lambda x : getHourCat(data, x.name), axis = 1)
    data = data.drop(['gameStartTimestamp', 'startHour'], axis=1)

    data.loc[:,'weekDay'].value_counts()

    newCol = {'dayFreq':0,
                'hourFreq':0,
                'mondayCount':0,
                'tuesdayCount':0,
                'wednesdayCount':0,
                'thursdayCount':0,
                'fridayCount':0,
                'saturdayCount':0,
                'sundayCount':0,
                'morningCount':0,
                'afternoonCount':0,
                'eveningCount':0,
                'nightCount':0,
                'mondayMorning':0,
                'tuesdayMorning':0,
                'wednesdayMorning':0,
                'thursdayMorning':0,
                'saturdayMorning':0,
                'sundayMorning':0,
                'mondayAfternoon':0,
                'tuesdayAfternoon':0,
                'wednesdayAfternoon':0,
                'thursdayAfternoon':0,
                'saturdayAfternoon':0,
                'sundayAfternoon':0,
                'mondayEvening':0,
                'tuesdayEvening':0,
                'wednesdayEvening':0,
                'thursdayEvening':0,
                'saturdayEvening':0,
                'sundayEvening':0,
                'mondayNight':0,
                'tuesdayNight':0,
                'wednesdayNight':0,
                'thursdayNight':0,
                'saturdayNight':0,
                'sundayNight':0}
    
    colMode = ["gameMode", "role"]
    colMax = ["summonerLevel"]

    return data
