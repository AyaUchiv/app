# A Business Intelligence Approach to Evaluating Theatrical Release Suitability Based on Audience Commitment Indicators

MSc Information Technology with Business Intelligence  
Robert Gordon University | April 2026

## Overview

This project develops a Business Intelligence framework to assess whether 
films that are adaptations, franchises or remakes exhibit stronger audience 
commitment indicators that make them more suitable for theatrical release. 
The framework is grounded in the institutional logics theory of Hadida et al. (2021).

A dataset of 1,110 films released between 2020 and 2025 was collected from 
publicly available sources. Quantitative commitment and convenience indices 
were developed and evaluated across nine model configurations. The preferred 
model achieved 89% accuracy in classifying cinema releases and 55.3% for 
streaming releases.

## Data Sources

| Source | Purpose |
|--------|---------|
| IMDb non-commercial dataset | Ratings, vote counts, runtime, genre |
| Kaggle movie revenue dataset | Budget, revenue, MPAA rating, franchise status |
| TMDb API | Netflix franchise, originality, MPAA rating |
| Wikipedia | Netflix film list 2020-2025 |
| Netflix global weekly top ten | Streaming performance classification |

## Repository Structure
- data_preparation/netflix_imdb_tmdb.py — merges Wikipedia, TMDb API and IMDb for the streaming dataset
- analysis/quadrant_analysis.py — runs all 9 model configurations and exports results
- analysis/feature_importance.py — Random Forest feature importance and model evaluation
- sql/imdb_query.sql — BigQuery query to extract IMDb film data
- sql/kaggle_imdb_merge.sql — BigQuery query to merge Kaggle cinema data with IMDb

## Requirements
```
pip install pandas numpy scikit-learn openpyxl requests
```

## How to Run
Step 1 — Prepare streaming dataset
python data_preparation/netflix_imdb_tmdb.py
Requires: netflix_clean.xlsx, title.ratings.tsv, title.basics.tsv, all-weeks-global.xlsx

Step 2 — Run feature importance analysis
python analysis/feature_importance.py
Requires: visuals.xlsx

Step 3 — Run quadrant sensitivity analysis
python analysis/quadrant_analysis.py
Requires: visuals.xlsx
Outputs: model_results.xlsx, model_1a_tableau.xlsx

## Key Results
Model 1A — log normalisation, configuration 1 — was selected as the preferred model.
- Cinema accuracy: 89.0%
- Streaming accuracy: 55.3%
- Overall accuracy: 64.6%

## Notes
- Excel-based data preparation steps are documented in the dissertation Chapter 4
- The TMDb API script requires a valid API key
- IMDb non-commercial datasets are available at https://datasets.imdbws.com
- AI assistance is acknowledged in each script header
- Kaggle dataset is available at https://www.kaggle.com/datasets/michaelmatta0/movies-ultimate-metrics-features-and-metadata
- Netflix top ten global weekly is available at https://www.netflix.com/tudum/top10/data/all-weeks-global.xlsx (https://www.netflix.com/tudum/top10)
