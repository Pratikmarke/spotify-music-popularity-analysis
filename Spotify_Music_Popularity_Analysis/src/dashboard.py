"""Simple Streamlit dashboard for Spotify Music Popularity Analysis."""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "spotify_tracks.csv"

st.set_page_config(page_title="Spotify Popularity Analysis", page_icon="🎵", layout="wide")
st.title("🎵 Spotify Music Popularity Analysis")
st.caption("A student Big Data analytics project using Python and PySpark")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    aliases = {"track": "track_name", "name": "track_name",
               "artists": "artist_name", "artist": "artist_name",
               "genre": "track_genre", "year": "release_year"}
    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})
    for c in ["popularity", "danceability", "energy", "tempo", "release_year"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "track_name" not in df.columns:
        df["track_name"] = "Unknown track"
    if "artist_name" not in df.columns:
        df["artist_name"] = "Unknown artist"
    if "track_genre" not in df.columns:
        df["track_genre"] = "Unknown genre"
    return df.dropna(subset=["popularity"])

if not DATA_PATH.exists():
    st.error("Dataset not found. Add data/spotify_tracks.csv.")
    st.stop()

df = load_data()
st.sidebar.header("Filters")
genres = sorted(df["track_genre"].dropna().astype(str).unique().tolist())
selected_genres = st.sidebar.multiselect("Genre", genres, default=genres)
minimum_popularity = st.sidebar.slider("Minimum popularity", 0, 100, 0)
filtered = df[df["track_genre"].astype(str).isin(selected_genres)]
filtered = filtered[filtered["popularity"] >= minimum_popularity]

c1, c2, c3 = st.columns(3)
c1.metric("Tracks", f"{len(filtered):,}")
c2.metric("Average popularity", f"{filtered['popularity'].mean():.1f}" if len(filtered) else "N/A")
c3.metric("Artists", f"{filtered['artist_name'].nunique():,}")

st.subheader("Top 10 tracks")
st.dataframe(
    filtered.sort_values("popularity", ascending=False)
    [["track_name", "artist_name", "track_genre", "popularity"]]
    .head(10), use_container_width=True, hide_index=True
)

left, right = st.columns(2)
with left:
    st.subheader("Average popularity by genre")
    genre_stats = (filtered.groupby("track_genre", as_index=False)
                   .agg(average_popularity=("popularity", "mean"),
                        tracks=("track_name", "count"))
                   .sort_values("average_popularity", ascending=False).head(15))
    if not genre_stats.empty:
        st.bar_chart(genre_stats.set_index("track_genre")["average_popularity"])
with right:
    st.subheader("Popularity vs audio features")
    feature = st.selectbox("Choose feature", [
        c for c in ["danceability", "energy", "tempo"] if c in filtered.columns
    ] or ["popularity"])
    if feature in filtered.columns:
        chart_data = filtered[[feature, "popularity"]].dropna()
        st.scatter_chart(chart_data, x=feature, y="popularity")

st.subheader("Data preview")
st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV",
                   filtered.to_csv(index=False).encode("utf-8"),
                   file_name="spotify_filtered_tracks.csv", mime="text/csv")

st.info("Demo data is synthetic. Replace it with a properly licensed public dataset before interpreting or reporting real-world findings.")
