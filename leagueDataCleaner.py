import pandas as pd
from datetime import datetime


def getHourCat(data : pd.DataFrame, i : int):
    h = data.loc[i,'startHour']
    if h >= 6 and h < 12:
        data.loc[i,'startHourCat'] = 'Morning'
    elif h >= 12 and h < 17:
        data.loc[i,'startHourCat'] = "Afternoon"
    elif h >= 17 and h < 21:
        data.loc[i,'startHourCat'] = "Evening"
    else :
        data.loc[i,'startHourCat'] = "Night"


def cleanLeagueData(data : pd.DataFrame):
    for i in range(data.shape[0]):
        data.loc[i,'gameStartTimestamp'] = pd.Timestamp(datetime.fromtimestamp(data.loc[i,'gameStartTimestamp']/1000))
        data.loc[i,'gameEndTimestamp'] = pd.Timestamp(datetime.fromtimestamp(data.loc[i,'gameEndTimestamp']/1000))
        data.loc[i,'weekDay'] = data.loc[i,'gameStartTimestamp'].dayofweek
        data.loc[i,'weekDayName'] = data.loc[i,'gameStartTimestamp'].day_name()
        data.loc[i,'startHour'] = data.loc[i,'gameStartTimestamp'].hour
    data.apply(lambda x : getHourCat(x.name), axis = 1)