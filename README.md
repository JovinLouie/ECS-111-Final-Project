# Smurf Detection In Valorant - ECS 111 Final Project

By Jovin Louie, Samarth Sridhara, Iain Hennington\
Professor Zhe Zhao\
Spring Quarter 2025 - UC Davis

---

The final data, .py files, .ipynb files, as well as report paper and slides for our final project
which focused on detecting smurfs in the online PvP game "Valorant".

## Abstract

The purpose of this paper is to attempt to see if tabular data is sufficient in understanding player
skill and detecting whether a user is playing at a rank they’re not supposed to be in, or in other
terms, "smurfing" in competitive multiplayer video games, specifically Valorant. We’re scraping our
data for our models from Tracker.gg, a popular video game stat tracking website. We also clean our
data through winsorization, handling of NA values, hot-label encoding, removing outliers, and
normalizing numeric columns, while plotting data with plots to see variable distributions. The
methods we’re using are machine learning models such as decision trees, logistic regression, naive
bayes, etc. The results from our testing are that random forest is the best overall performing
model, with our decision trees model coming in a close second.

## Data Gathering

There wasn't any sort of dataset we could use that was real players, so we ended up going with using the unofficial Valorant API: https://github.com/raimannma/ValorantAPI. This API allowed us to essential search up players using their username and unique player ID, grabbing info on their most recent matches. With this API, we developed a script (scrape_stats.py) which recursively traversed through players' most recent matches, adding their username and player ID to a dataframe. With this dataframe, we built a web scraper that went to the player's respective player profile page on Tracker.gg (a website for tracking player stats), scraped the data, and put it back in the dataframe. With the webscraping we used a undetected chrome driver, randomization of time spent on webpage, as well as IP switching to maximize how many scrapes we could get before being blocked by CloudFlare or the built in rate-limiter on Tracker.gg.

## Data Labeling

Our data was obviously not labeled as these are real players, so we built a set of conditional if statements to give points to a player, if they passed a certain threshold of points they were considered a smurf, regular player, or suspicious. This was done in the label_preprocess.ipynb.

## Data Preprocessing Pipeline

Below is a summary of the preprocessing steps applied to our dataset before modeling:

1. **Load Raw Data**: The dataset was loaded from a CSV file containing processed player statistics using pandas, which allowed for efficient data manipulation and analysis.
2. **Identify and Handle Missing Values**: We checked for blank or missing fields in the dataset by iterating through each row and identifying entries with empty strings. These rows were cataloged to keep track of which player records had missing data.
3. **Impute or Replace Missing Values**: For missing values, we replaced empty strings with "N/A" to standardize the representation of missing data. In some cases, missing numeric values were imputed using the median of each column to ensure no loss of data due to NA values.
4. **Winsorization**: Numeric columns were winsorized at the 5th and 95th percentiles to reduce the influence of outliers.
5. **Normalization**: All numeric columns were normalized using standard scaling to ensure features are on the same scale.
6. **Label Encoding**: The target variable (`smurf_label`) was mapped to numeric values (e.g., "normal player" = 0, "suspicious" = 1, "most likely smurf" = 2) for compatibility with machine learning models. Additionally, one-hot encoding was applied to the `smurf_label` column to create separate binary columns for each class.
7. **Feature Engineering**: New features were created, such as KDA ratio (`(kills_per_game + assists_per_game) / deaths_per_game`) and accuracy (`hs_percent / (hs_percent + body_percent + leg_percent)`).
8. **Variance Threshold**: Features with very low variance (threshold = 0.01) were removed to reduce noise.
9. **Correlation Filtering**: Highly correlated features (correlation > 0.95) were dropped to prevent multicollinearity.
10. **Outlier Removal**: Isolation Forest was used to remove outliers, further improving data quality.
11. **Train-Test Split**: The cleaned data was split into training and testing sets (80/20 split) for model evaluation.
12. **Save Preprocessed Data**: The final preprocessed dataset was saved for downstream modeling.

These steps ensured our data was clean, robust, and suitable for training machine learning models to detect smurfing behavior in Valorant.

## Model Development
**Models Used:** Decision Tree, Random Forest, Logistic Regression

Leveraged For Analyzing Data and Models:
1. **Classification Reports**
2. **Confusion Matrices**
3. **Feature Importance**

We made sure to drop unneccessary columns for the models, as well as encode categorical variables. For tuning, grid search was used, results for our Random Forest Model looked like:

- **Best Parameters:** `{'bootstrap': True, 'max_depth': None, 'min_samples_leaf': 7, 'min_samples_split': 2, 'n_estimators': 200}`
- **Best Cross-Validated F1 Score:** `0.8974214472396291`
- **Final Model:** `RandomForestClassifier(min_samples_leaf=7, n_estimators=200, random_state=123)`

These results indicate that the Random Forest model, with the above hyperparameters, achieved the highest performance in detecting smurfing behavior.