import numpy as np
import pandas as pd


def cleanTarget(data : pd.DataFrame):

    # Clean data from forms

    # Targets data
    targets = pd.DataFrame(columns=['pseudo', 'tagline', 'region', 'age', 'sex', 'department', 'job', 'relationship', 'live_with_others', 'buy_content', 'economic', 'love_team_work',  'play_instrument', 'sport'])

    targets['pseudo'] = data['Pseudo']
    targets['tagline'] = data['Tagline']
    targets['region'] = data['Région']
    targets['age'] = np.floor((pd.to_datetime(pd.Timestamp.now()) - pd.to_datetime(data['Date de naissance'], format = "%d/%m/%Y")).dt.days / 365.25)
    targets['sex'] =  np.where(data['Sexe'] == 'Femme', 0, np.where(data['Sexe'] == 'Homme', 1, 2 ) )
    targets['department'] = data['Département de résidence (numéro) actuel']
    targets['job'] = np.where(data['Avez vous un job / Etes vous étudiant ?'] == 'Oui', 1, 0)
    targets['relationship'] = np.where(data['Statut familial'] == 'En couple', 1, 0)
    targets['live_with_others'] = np.where(data['Situation domicile'] == "Je vis avec d'autres personnes", 1, 0)
    targets['buy_content'] = np.where(data['Achetez vous du contenu de jeu ?'] == 'Non', 0, np.where(data['Achetez vous du contenu de jeu ?'] == 'Rarement', 1, 2 ) )
    targets['economic'] = data['Niveau économique (1 = plus bas, 3 = plus haut)'] - 1
    targets['love_team_work'] = np.where(data["Aimez vous le travail d'équipe ?"] == 'Oui', 1, 0)
    targets['play_instrument'] = np.where(data["Savez vous jouer d'un instrument ?"] == 'Oui', 1, 0)
    targets['sport'] = np.where(data['Pratiquez vous du sport ?'] == 'Non', 0, np.where(data['Pratiquez vous du sport ?'] == 'Parfois', 1, 2 ) )

    return targets