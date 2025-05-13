import pandas as pd
import numpy as np
import csv

# # Load data using pandas
file_path = "filepath"  # Update path if needed
df = pd.read_csv('filepath')

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    raw_rows = [row for row in reader]

rows_with_blank_fields = [
    {"puuid": row[0], "user": row[1], "row": row}
    for row in raw_rows if "" in row
]

df_blanks = pd.DataFrame(rows_with_blank_fields)
print("Rows with blank values:")
print(df_blanks[['puuid', 'user']]) 
#showing which values are the blank values

input_file = 'filepath' ##file path of the original file
output_file = 'filepath' ##file path of the new file after editing it

with open(input_file, mode="r", newline="") as infile, open(output_file, mode="w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        # Replace empty strings with "N/A"
        cleaned_row = ["N/A" if cell.strip() == "" else cell for cell in row]
        writer.writerow(cleaned_row)
#NA values here

label_map = {
    "normal player": 0,
    "suspicious": 1,
    "most likely smurf": 2
}
df["smurf_label_num"] = df["smurf_label"].map(label_map)
df.to_csv("filepath", index=False) ##fiepath is necessary here as well
#this would be the labeling version of the code



df.replace("", np.nan, inplace=True)

df_encoded = pd.get_dummies(df, columns=['smurf_label'])

print(df_encoded.filter(like='smurf_label_').head())

df_encoded.to_csv("filepath", index=False) #file path here is necessary as well
#hot encoded here

