CREATE OR REPLACE TABLE `imdb_project.kaggle_with_tconst` AS
SELECT 
    k.*,
    t.tconst,
    t.runtimeMinutes,
    t.genres
FROM `imdb_project.movie_revenue` AS k
LEFT JOIN `imdb_project.movie_title` AS t
    ON TRIM(LOWER(REGEXP_REPLACE(
           REGEXP_REPLACE(k.`Movie Name`, r'[^a-zA-Z0-9 ]', ''),
           r'\s+', ' ')))
     = TRIM(LOWER(REGEXP_REPLACE(
           REGEXP_REPLACE(t.primaryTitle, r'[^a-zA-Z0-9 ]', ''),
           r'\s+', ' ')))
    AND ABS(SAFE_CAST(EXTRACT(YEAR FROM k.`Release Date`) AS INT64) 
          - SAFE_CAST(t.startYear AS INT64)) <= 1
    AND t.titleType = 'movie'
WHERE k.`Production Budget _USD_` > 0
    AND k.`Worldwide Gross _USD_` > 0
    AND EXTRACT(YEAR FROM k.`Release Date`) BETWEEN 2020 AND 2025;


CREATE OR REPLACE TABLE `imdb_project.final_cinema` AS
SELECT
    k.*,
    r.averageRating,
    r.numVotes
FROM `imdb_project.kaggle_with_tconst` AS k
LEFT JOIN `imdb_project.movie_ratings` AS r
    ON k.tconst = r.tconst
WHERE k.tconst IS NOT NULL
    AND r.numVotes IS NOT NULL;