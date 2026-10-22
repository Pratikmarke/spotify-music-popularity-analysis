"""Spotify Music Popularity Analysis mini-project.

Runs with PySpark when available; otherwise uses Pandas.
Input: data/spotify_tracks.csv
Outputs: outputs/*.csv and outputs/*.png
"""
from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "spotify_tracks.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

FEATURES = [
    "popularity", "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
    "duration_ms", "release_year"
]

def load_and_clean():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Put a CSV named spotify_tracks.csv inside the data folder."
        )
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Simple aliases for common dataset column names
    aliases = {
        "track": "track_name", "name": "track_name",
        "artists": "artist_name", "artist": "artist_name",
        "genre": "track_genre", "track_genre": "track_genre",
        "year": "release_year"
    }
    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})

    required = ["track_name", "artist_name", "popularity"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. "
            "See README.md for the expected column names."
        )

    for c in FEATURES:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.drop_duplicates()
    df["track_name"] = df["track_name"].fillna("Unknown track")
    df["artist_name"] = df["artist_name"].fillna("Unknown artist")
    if "track_genre" not in df.columns:
        df["track_genre"] = "Unknown genre"
    else:
        df["track_genre"] = df["track_genre"].fillna("Unknown genre")
    df = df.dropna(subset=["popularity"])
    df["popularity"] = df["popularity"].clip(0, 100)
    return df

def run_pyspark_aggregations(df):
    """Use Spark DataFrames for aggregations; return False if Spark is unavailable."""
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import avg, count, desc, col
        spark = (SparkSession.builder
                 .appName("SpotifyMusicPopularityAnalysis")
                 .master("local[*]")
                 .config("spark.ui.enabled", "false")
                 .getOrCreate())
        sdf = spark.createDataFrame(df)
        print(f"PySpark loaded {sdf.count():,} rows.")
        genre = (sdf.groupBy("track_genre")
                 .agg(avg("popularity").alias("average_popularity"),
                      count("*").alias("track_count"))
                 .filter(col("track_count") >= 1)
                 .orderBy(desc("average_popularity")))
        artist = (sdf.groupBy("artist_name")
                  .agg(avg("popularity").alias("average_popularity"),
                       count("*").alias("track_count"))
                  .orderBy(desc("average_popularity")))
        genre.toPandas().to_csv(OUT / "popularity_by_genre.csv", index=False)
        artist.toPandas().to_csv(OUT / "popularity_by_artist.csv", index=False)
        spark.stop()
        return True
    except Exception as exc:
        print(f"PySpark unavailable or failed ({exc}). Using Pandas fallback.")
        return False

def main():
    df = load_and_clean()
    print(f"Rows after cleaning: {len(df):,}")
    print("\nPreview:")
    print(df.head().to_string(index=False))

    used_spark = run_pyspark_aggregations(df)
    if not used_spark:
        (df.groupby("track_genre", dropna=False)
           .agg(average_popularity=("popularity", "mean"),
                track_count=("track_name", "count"))
           .sort_values("average_popularity", ascending=False)
           .to_csv(OUT / "popularity_by_genre.csv"))
        (df.groupby("artist_name", dropna=False)
           .agg(average_popularity=("popularity", "mean"),
                track_count=("track_name", "count"))
           .sort_values("average_popularity", ascending=False)
           .to_csv(OUT / "popularity_by_artist.csv"))

    top_tracks = df.sort_values("popularity", ascending=False).head(20)
    top_tracks.to_csv(OUT / "top_20_tracks.csv", index=False)

    numeric = [c for c in FEATURES if c in df.columns]
    if "popularity" in numeric:
        df[numeric].corr(numeric_only=True).to_csv(OUT / "feature_correlations.csv")

    # Charts
    top = df.nlargest(min(10, len(df)), "popularity").sort_values("popularity")
    plt.figure(figsize=(10, 6))
    plt.barh(top["track_name"].astype(str), top["popularity"])
    plt.xlabel("Popularity (0-100)")
    plt.title("Most Popular Tracks in Dataset")
    plt.tight_layout()
    plt.savefig(OUT / "top_tracks.png", dpi=150)
    plt.close()

    genre_summary = pd.read_csv(OUT / "popularity_by_genre.csv")
    genre_summary = genre_summary.sort_values("average_popularity", ascending=True).tail(10)
    plt.figure(figsize=(10, 6))
    plt.barh(genre_summary["track_genre"].astype(str), genre_summary["average_popularity"])
    plt.xlabel("Average popularity")
    plt.title("Top Genres by Average Popularity")
    plt.tight_layout()
    plt.savefig(OUT / "genre_popularity.png", dpi=150)
    plt.close()

    if "danceability" in df.columns:
        plt.figure(figsize=(8, 5))
        plt.scatter(df["danceability"], df["popularity"], alpha=0.7)
        plt.xlabel("Danceability")
        plt.ylabel("Popularity")
        plt.title("Danceability vs Popularity")
        plt.tight_layout()
        plt.savefig(OUT / "danceability_vs_popularity.png", dpi=150)
        plt.close()

    print(f"\nAnalysis complete. Outputs saved to: {OUT}")
    print("PySpark used:", used_spark)

if __name__ == "__main__":
    main()
