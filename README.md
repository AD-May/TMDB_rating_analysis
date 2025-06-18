# Movie Ratings EDA

## User Stories

- **Decade Trends**  
  > As a movie buff, I want to compare average ratings by decade, so I can see how audience tastes have evolved.  
- **Genre Evolution**  
  > As a content strategist, I want to track genre frequency over time, so I can identify rising and declining categories.  
- **Budget–Revenue–Rating Correlation**  
  > As an analyst, I want to explore the relationship between a film’s budget, its box-office revenue, and its average rating, so I can understand what drives success.

## 📂 Data Source

- **Dataset:** TMDB 5000 Movie Dataset  
- **Filename:** `tmdb_5000_movies.csv` (and optionally `tmdb_5000_credits.csv` for cast/crew)  
- **Columns of interest:**  
  - `title`, `release_date`, `budget`, `revenue`, `vote_average`, `genres` (JSON list)  
- **Download:** [Kaggle – TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

## 🔧 Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/AD-May/TMDB_rating_analysis.git
   cd TMDB_rating_analysis
   ```
