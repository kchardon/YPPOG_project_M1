# Youth Privacy Protection and Online Gaming (YPPOG)

For my research project in the Master 1 Data & AI at the [Institut Polytechnique de Paris](https://www.ip-paris.fr/education/masters/mention-informatique/master-year-1-data-and-artificial-intelligence), I worked with Benjamin NGUYEN and Nicolas SOULIE for the YPPOG project of the [Institut DATAIA](https://www.dataia.eu/recherche/yppog).

The aim of the project was to study whether it is possible to predict private data (age, sex, department of residence, etc.) from game data, mainly whether it is possible to predict whether a person is a minor.

Different steps were carried out :
* Look for game APIs
* Collect data from players in a form
* Clean data collected from the form
* Collect game data with the game name from APIs
* Clean game data

For the game APIs, we selected the Riot API (League of Legends, League of Runeterra, Teamfight Tactics), the Steam API and the PlayerUnknow's Battlegrounds API.

To collect data from players, we have contacted players' data protection associations and higher education players' associations to invite members to take part in our data collection For the data collection, a consent notice and a form had to be completed (You can find them in the data folder).

For the cleaning and the collection of the game data, some python scripts have been made (They are available in each game folder).
There are two main functions :
* **cleanLeagueTarget(data : pd.DataFrame)** :  The function is available in *leagueTargetCleaner.py* and is used to clean the data collected in a form from various participants. The data passed to the function is a pandas dataframe containing data collected from the form. It returns a dataframe with the target variables and the game name.
* **getLeagueData(targets : pd.DataFrame)** : The function is available in *leagueGetDataMultiplePlayers.py* and is used to collect and clean game data. The data passed to the function is a pandas dataframe containing the target data (from the previous function). It returns a dataframe with the feature data.

Some examples are available in each game folder in *getDataLeague.ipynb*.

## Requirements

To use the functions, some libraries are needed. They are listed in *requirements.txt*.
You can install all of them by running
```
pip install -r requirements.txt
```
while being in the folder.

## Future work

We have to implement the functions for the games other than League of Legends.

When the website with the form will be finished, we could update the target cleaner function to adapt it to the new form.

When we will have enough data, we have to study the correlations between private data and game data, and attempt to set up a predictive model.
