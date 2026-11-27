import pandas as pd
import geopandas as gpd
from flask import Flask, jsonify
from flask_cors import CORS
import matplotlib.pyplot as plt
import numpy as np

income_df = pd.read_csv("Data/income_clean.csv")
race_df = pd.read_csv("Data/race_clean.csv")
sexage_df = pd.read_csv("Data/sexage_clean.csv")

tracts = gpd.read_file("Data/census_tracts_density.geojson")
permits = pd.read_csv("Data/permitsMatched.csv")

# Make sure GEOIDs have the same data type
permits["GEOID"] = permits["GEOID"].astype(str)
tracts["geoid10"] = tracts["geoid10"].astype(str)

# Get community area information for each census tract
tract_info = tracts[["geoid10", "community_name"]]

# Match each building permit to its census tract
permits = permits.merge(
    tract_info,
    left_on="GEOID",
    right_on="geoid10",
    how="left"
)

# Count permits per community area
community_counts = permits.groupby("community_name").size()

# Get the top 10 community areas
top_10 = community_counts.sort_values(ascending=False).head(10)

colors = plt.cm.viridis(
    np.linspace(0.25, 0.9, len(top_10))
)
plt.figure(figsize=(10,6))

plt.barh(
    top_10.index,
    top_10.values,
    color=colors,
    edgecolor="black"
)
plt.xlabel("Number of Building Permits")
plt.ylabel("Community")
plt.title("Top 10 Census Tracts by Building Permits")
plt.xlim(0, 800)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_10_community_permits.png", dpi=300, bbox_inches="tight")
plt.show()
