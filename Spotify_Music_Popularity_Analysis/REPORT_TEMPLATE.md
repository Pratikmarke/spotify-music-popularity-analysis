# Project Report: Spotify Music Popularity Analysis Using Big Data

## 1. Abstract
This project analyzes track popularity and audio characteristics using a structured music dataset. Python is used for cleaning and visualization, while Apache Spark is used for scalable aggregation. A Streamlit dashboard allows users to explore the results interactively.

## 2. Problem Statement
Music catalogs contain many tracks and multiple audio attributes. The project aims to organize and analyze these data to identify descriptive patterns in popularity by genre, artist, and audio features.

## 3. Objectives
1. Load and clean music track data.
2. Analyze popularity by genre and artist.
3. Explore relationships between popularity and audio features.
4. demonstrate Spark DataFrame transformations and aggregations.
5. Present results in charts and an interactive dashboard.

## 4. Tools and Technologies
- Python
- Pandas
- Apache Spark / PySpark
- Matplotlib
- Streamlit
- CSV dataset

## 5. Methodology
1. Collect a public dataset and verify its license.
2. Inspect columns and data types.
3. Remove duplicate rows and handle missing values.
4. Use Spark group-by aggregations for genre and artist.
5. Export results as CSV files.
6. Create visualizations and dashboard filters.
7. Interpret results cautiously.

## 6. Results
Run the program on your chosen real dataset, then insert actual results here:
- Number of rows before and after cleaning: ______
- Highest average-popularity genre (with minimum sample threshold): ______
- Top track by dataset popularity: ______
- Correlation between popularity and danceability: ______
- Any notable patterns: ______

Do not fill this section using the included synthetic demo data as if it were real Spotify data.

## 7. Conclusion
The project demonstrates a reproducible workflow for music data cleaning, aggregation, and visualization. Findings describe associations in the selected dataset and do not establish that any audio feature causes popularity.

## 8. Limitations
- Dataset popularity scores may be time-dependent and source-dependent.
- The dataset may not represent all music listeners or regions.
- Correlation does not imply causation.
- Local Spark execution demonstrates Spark APIs, but is not the same as a multi-node production cluster.

## 9. Future Scope
- Process a larger licensed dataset.
- Compare Pandas and PySpark execution time on the same workload.
- Store curated data in a SQL database or Parquet format.
- Add year filters, artist filters, and richer dashboard visualizations.
