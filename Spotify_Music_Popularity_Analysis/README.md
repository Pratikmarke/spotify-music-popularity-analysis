# Spotify Music Popularity Analysis using Big Data

A beginner-friendly college mini-project using **Python, PySpark, Pandas, Matplotlib, and Streamlit**.

## What it does
- Loads a Spotify-style tracks CSV file.
- Cleans missing values and duplicates.
- Uses PySpark for distributed-style data processing (runs locally).
- Analyzes popularity by genre and artist.
- Explores relationships between popularity and audio features.
- Creates CSV outputs and a simple interactive dashboard.

> **Dataset note:** `data/spotify_tracks.csv` included here is a small synthetic demo dataset so the project runs immediately. It is NOT real Spotify data. For a meaningful project submission, replace it with a properly licensed public Spotify tracks dataset and check its column names.

## Requirements
- Python 3.10 or newer recommended
- Java 11 or 17 for PySpark (if using PySpark locally)
- VS Code or another Python editor

## Setup
```bash
python -m venv .venv
```
Activate the environment:
- Windows: `.venv\\Scripts\\activate`
- macOS/Linux: `source .venv/bin/activate`

Install packages:
```bash
pip install -r requirements.txt
```

## Run the analysis
From the project root:
```bash
python src/analysis.py
```
Results will be saved in `outputs/`.

If PySpark/Java setup gives trouble, the script automatically falls back to Pandas and still completes the analysis.

## Run the dashboard
```bash
streamlit run src/dashboard.py
```
Open the local URL shown in your terminal.

## Expected CSV columns
The included demo uses:
- `track_name`, `artist_name`, `track_genre`, `popularity`
- `danceability`, `energy`, `loudness`, `speechiness`
- `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `duration_ms`, `release_year`

When replacing the dataset, rename columns to match these names or edit `COLUMN_ALIASES` in `src/analysis.py`.

## Suggested project workflow
1. Dataset collection
2. Data cleaning
3. Exploratory data analysis
4. PySpark aggregations
5. Export analytical tables
6. Interactive dashboard
7. Findings, limitations, and future scope

## Important interpretation
Popularity is not the same as music quality. Correlation does not prove that a feature causes popularity. Results depend on the dataset, collection date, and how popularity is defined.
