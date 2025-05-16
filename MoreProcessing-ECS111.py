import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from scipy.stats.mstats import winsorize

#  Load raw data
df = pd.read_csv("/Users/samarthsridhara/Downloads/valorant_players_processedMay12,2025.csv")

# Impute missing numeric values with MEDIAN
numeric_cols = df.select_dtypes(include='number').columns.tolist()
imputer = SimpleImputer(strategy='median')
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

# Winsorize numeric columns (cap 5th and 95th percentiles)
for col in numeric_cols:
    df[col] = winsorize(df[col], limits=[0.05, 0.05])

#  Normalize numeric columns
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Encode categorical label (smurf_label) using one-hot encoding
df = pd.get_dummies(df, columns=["smurf_label"])

# Feature engineering (KDA ratio and accuracy)
df["kda"] = (df["kills_per_game"] + df["assists_per_game"]) / df["deaths_per_game"]
df["accuracy"] = df["hs_percent"] / (df["hs_percent"] + df["body_percent"] + df["leg_percent"])

#  Apply VarianceThreshold to numeric columns only
numeric_df = df.select_dtypes(include='number')
selector = VarianceThreshold(threshold=0.01)
numeric_selected = selector.fit_transform(numeric_df)
selected_numeric_cols = numeric_df.columns[selector.get_support()]
numeric_df = pd.DataFrame(numeric_selected, columns=selected_numeric_cols)

# Recombine numeric + non-numeric data
non_numeric_df = df.select_dtypes(exclude='number').reset_index(drop=True)
df = pd.concat([non_numeric_df, numeric_df], axis=1)

#  Remove highly correlated features (optional)
corr_matrix = df.select_dtypes(include='number').corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
high_corr_cols = [col for col in upper.columns if any(upper[col] > 0.95)]
df.drop(columns=high_corr_cols, inplace=True)

# Outlier removal using Isolation Forest (optional)
iso = IsolationForest(contamination=0.01, random_state=42)
outliers = iso.fit_predict(df.select_dtypes(include='number'))
df = df[outliers == 1].reset_index(drop=True)

# Train-test split for modeling
X = df.drop(columns=[col for col in df.columns if "smurf_label_" in col], errors='ignore')
y = df.filter(like="smurf_label_").idxmax(axis=1).str.replace("smurf_label_", "")  # Recover label from one-hot

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  Save final preprocessed data
df.to_csv("/Users/samarthsridhara/Downloads/valorant_players_processedMay15,2025+morepreprocessing.csv", index=False)
