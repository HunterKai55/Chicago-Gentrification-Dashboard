import pandas as pd

income_df = pd.read_csv("Data/income_clean.csv")
race_df = pd.read_csv("Data/race_clean.csv")
sexage_df = pd.read_csv("Data/sexage_clean.csv")

for df in [income_df, race_df, sexage_df]:
    df["geoid"] = df["geoid"].astype(str).str.replace("1400000US", "", regex=False)

income_df.to_csv("Data/income_clean.csv", index=False)
race_df.to_csv("Data/race_clean.csv", index=False)
sexage_df.to_csv("Data/sexage_clean.csv", index=False)