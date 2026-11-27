import pandas as pd
import geopandas as gpd
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

race = pd.read_csv("Data/race_clean.csv")
income = pd.read_csv("Data/income_clean.csv")
#sexage = pd.read_csv("Data/sexage_clean.csv")
permits = pd.read_csv("Data/permitsMatched.csv")
tracts = gpd.read_file("Data/census_tract_boundaries.geojson")

def format_geoid(column):
    return (
        column.astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(11)
    )

permits["GEOID"] = format_geoid(permits["GEOID"])
income["geoid"] = format_geoid(income["geoid"])
race["geoid"] = format_geoid(race["geoid"])

@app.route("/api/tract/<geoid>")

def get_tract_data(geoid):
    permit_data = permits[permits["GEOID"] == geoid]

    income_data = income[income["geoid"] == geoid]

    race_data = race[race["geoid"] == geoid]

    return jsonify({
        "permits": permit_data.to_dict(orient="records"),
        "income": income_data.to_dict(orient="records"),
        "race": race_data.to_dict(orient="records")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
