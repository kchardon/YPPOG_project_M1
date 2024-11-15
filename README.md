# Youth Privacy Protection and Online Gaming (YPPOG)

This research project was initiated during my Master 1 in Data & AI at the [Institut Polytechnique de Paris](https://www.ip-paris.fr/education/masters/mention-informatique/master-year-1-data-and-artificial-intelligence) in collaboration with **Benjamin NGUYEN** and **Nicolas SOULIE** at the [Institut DATAIA](https://www.dataia.eu/index.php/node/950). I am continuing to develop this project during my Master 2 studies and into my PhD.


## Project Overview

The **YPPOG project** explores whether private data (e.g., age, gender, and region of residence) can be inferred from game data, with a primary focus on determining if a player is a minor. This research is critical for enhancing youth privacy protection in online gaming environments.


## Data

### Data Selection

An initial list of multiplayer games was compiled, focusing on those with accessible APIs for data retrieval. After testing multiple APIs, we selected the following:

- **Riot API**: for League of Legends, Legends of Runeterra, and Teamfight Tactics.
- **Steam API**
- **PlayerUnknown's Battlegrounds API**

We currently focus on League of Legends due to its global player base, significant popularity, and extensive youth participation.

### Data Collection

To gather data, we collaborated with player privacy protection organizations and university gaming associations. Participants completed a consent form and a survey, allowing us to collect demographic information and game data. Python scripts were developed to facilitate data cleaning and collection, which can be found within each game’s folder.

The main functions are:

* **cleanTarget(data : pd.DataFrame)** :  Available in *targetCleaner.py*, this function cleans demographic data collected from participants. It takes a pandas DataFrame as input and outputs a cleaned DataFrame with target variables and game identifiers.

* **getData(targets : pd.DataFrame)** : Located in *getDataMultiplePlayers.py*, this function collects and cleans in-game data for each participant. It takes a DataFrame of target data and returns a DataFrame with game feature data.

Example usage of these functions is provided in *getData.ipynb* within each game folder. Currently, we are collecting data from all matches played since 2022.


## Prediction Approaches

Our prediction task is structured around two primary methodologies:

- **Unsupervised Learning**: Clustering the data to identify patterns that may correlate with demographic information without a predefined model.
- **Supervised Learning**: Developing predictive models to infer demographic attributes, ideally with limited data, simulating a privacy attacker scenario.

### Hypotheses for Feature Selection

Some initial hypotheses for identifying minors include:

- **Playing patterns**: Minors may play mostly in the evenings or on weekends.
- **Session length**: Minors may have shorter sessions due to parental controls.

Other demographic characteristics might also be inferred from gaming behavior:

- **Region of residence**: Could potentially be inferred based on regional vacation times.
- **Employment status**: Those unemployed may play more often during daytime hours.

## Preliminary results

While awaiting the collection of project-specific data, I utilized a publicly available dataset [1] to perform initial experiments and test predictive models.

### Dataset Overview

The dataset contains demographic and game-related attributes for each player, including:

- PlayerID: Unique identifier for each player.
- Age: Age of the player.
- Gender: Gender of the player.
- Location: Geographic location of the player.
- GameGenre: Genre of the game the player is engaged in.
- PlayTimeHours: Average hours spent playing per session.
- InGamePurchases: Indicates whether the player makes in-game purchases (0 = No, 1 = Yes).
- GameDifficulty: Difficulty level of the game.
- SessionsPerWeek: Number of gaming sessions per week.
- AvgSessionDurationMinutes: Average duration of each gaming session in minutes.
- PlayerLevel: Current level of the player in the game.
- AchievementsUnlocked: Number of achievements unlocked by the player.
- EngagementLevel: Categorized engagement level reflecting player retention ('High', 'Medium', 'Low').

### Approach

Although the dataset was designed to predict player engagement levels using both demographic and game data, I repurposed it to investigate whether demographic attributes (such as age, gender, and location) could be predicted based solely on game-related features.

This approach allowed me to conduct exploratory analysis and test preliminary models to assess the feasibility of demographic inference from gaming behavior.

## Requirements

To utilize the functions in this project, install the required libraries listed in requirements.txt:

```
pip install -r requirements.txt
```

**Note**: API keys are required for data retrieval from each of the gaming APIs.


## Future work

Several key areas remain for further development:

- Updating the target cleaner function to align with the finalized online consent form.
- Conducting in-depth analysis to examine correlations between game data and demographic attributes.
- Collaborating with experts in each game to identify relevant in-game data that could contribute to privacy-related predictions.
- Collect data.
- Extending data collection functions to games beyond League of Legends.

## References

[1] Rabie El Kharoua. (2024). 🎮 Predict Online Gaming Behavior Dataset [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/8742674