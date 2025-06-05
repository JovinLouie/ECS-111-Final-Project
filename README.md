# Smurf Detection In Valorant - ECS 111 Final Project

## By Jovin Louie, Samarth Sridhara, Iain Hennington

## Professor Zhe Zhao

## Spring Quarter 2025 - UC Davis

The final data, .py files, .ipynb files, as well as report paper and slides for our final project
which focused on detecting smurfs in the online PvP game "Valorant".

---

### Abstract

The purpose of this paper is to attempt to see if tabular data is sufficient in understanding player
skill and detecting whether a user is playing at a rank they’re not supposed to be in, or in other
terms, "smurfing" in competitive multiplayer video games, specifically Valorant. We’re scraping our
data for our models from Tracker.gg, a popular video game stat tracking website. We also clean our
data through winsorization, handling of NA values, hot-label encoding, removing outliers, and
normalizing numeric columns, while plotting data with plots to see variable distributions. The
methods we’re using are machine learning models such as decision trees, logistic regression, naive
bayes, etc. The results from our testing are that random forest is the best overall performing
model, with our decision trees model coming in a close second.
