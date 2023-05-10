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

    newCol = {'dayMostFreq':0,
                'hourMostFreq':0,
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
                'championPref':None,
                'championCount':0}
    
    colMode = ["gameMode", "role"]
    colMax = ["summonerLevel"]

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
    
    data = data.drop(['startHourCat', 'weekDay', 'championId'], axis=1)


    return data, newCol
