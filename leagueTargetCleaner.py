


def cleanLeagueTarget(data : pd.DataFrame):
    targets = pd.DataFrame(columns=['pseudo', 'region', 'age', 'sex', 'department', 'job', 'relationship', 'live_with_others', 'buy_content', 'economic', 'love_team_work',  'play_instrument', 'sport'])

    targets['pseudo'] = data['Pseudo']
    targets['region'] = data['Région / TagLine']
    targets['age'] = np.floor((pd.to_datetime(pd.Timestamp.now()) - pd.to_datetime(data['Date de naissance'], format = "%d/%m/%Y")).dt.days / 365.25)
    targets['sex'] = np.where(data['Sexe'] == 'Femme', 0, 1 )
    targets['department'] = data['Département de résidence (numéro) actuel']
    targets['job'] = np.where(data['Avez vous un job / Etes vous étudiant ?'] == 'Oui', 1, 0)
    targets['relationship'] = np.where(data['Statut familial'] == 'En couple', 1, 0)
    targets['live_with_others'] = np.where(data['Situation domicile'] == "Je vis avec d'autres personnes", 1, 0)