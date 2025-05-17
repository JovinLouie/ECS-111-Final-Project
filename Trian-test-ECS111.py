# Re-import libraries and re-execute the train-test split logic after reset
import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("/Users/samarthsridhara/Downloads/valorant_players_processedMay12,2025.csv")

# Reconstruct smurf_label from one-hot columns
label_cols = [col for col in df.columns if col.startswith("smurf_label_")]
if label_cols:
    df["smurf_label"] = df[label_cols].idxmax(axis=1).str.replace("smurf_label_", "")

# Features + label
X = df.drop(columns=label_cols, errors="ignore")
y = df["smurf_label"]

# Train-test split (keep ID columns like puuid, user, tag)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Add label back to each set
X_train["smurf_label"] = y_train.values
X_test["smurf_label"] = y_test.values

# Save
X_train.to_csv("/Users/samarthsridhara/Downloads/valorant_train_with_ids.csv", index=False)
X_test.to_csv("/Users/samarthsridhara/Downloads/valorant_test_with_ids.csv", index=False)


