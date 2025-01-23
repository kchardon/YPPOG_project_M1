import numpy as np
import pandas as pd


def cleanData(data : pd.DataFrame):

    # Clean preliminary data 

    GameGenre PlayTimeHours	InGamePurchases	GameDifficulty SessionsPerWeek AvgSessionDurationMinutes PlayerLevel AchievementsUnlocked EngagementLevel

    # Separate target data and input data
    targets = pd.DataFrame(columns=['id', 'age', 'gender', 'location'])
    input = pd.DataFrame(columns=['id', 'game_genre', 'play_time_hours', 'purchases', 'difficulty', 'sessions_per_week', 'avg_session_duration_minutes', 'level', 'achievements', 'engagement'])




    targets['id'] = data['PlayerID']
    targets['age'] = data['Age']
    targets['gender'] = np.where(data['Gender'] == 'Femme', 0, np.where(data['Gender'] == 'Homme', 1, 2 ) )
    targets['location'] = np.where(data['Location'] == 'USA', 0, np.where(data['Location'] == 'Europe', 1, np.where(data['Location'] == 'Asia', 2, 3 ) ) )

    input['id'] = data['PlayerID']
    input['game_genre'] = np.where(data['Location'] == 'USA', 0, np.where(data['Location'] == 'Europe', 1, np.where(data['Location'] == 'Asia', 2, 3 ) ) )

    return input, targets