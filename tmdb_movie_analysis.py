import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy.stats import linregress

json_columns = ['genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages']
df = pd.read_csv('tmdb_5000_movies.csv', parse_dates=['release_date'], converters={col: json.loads for col in json_columns})
df.drop_duplicates(subset='id', inplace=True)

df.index = df['id']

# Split JSON keys with 'name' index off into a list for each dataframe entry
def create_name_list(entry):
    if not entry:
        return None
    return [attribute['name'] for attribute in entry if 'name' in attribute]

for col in json_columns:
    df[col] = df[col].apply(lambda x: create_name_list(x))
    
    
# Average rating by decade of movie release
df['release_date'].dt.year.min()

df['decade'] = (df['release_date'].dt.year // 10) * 10
df_decade_rating = df.groupby('decade')['vote_average'].mean()

fig, ax = plt.subplots()
cmap = plt.get_cmap('viridis')
vals = np.linspace(0, 0.5, len(df_decade_rating))
colors = cmap(vals)  
df_decade_rating.plot(kind='bar', color=colors, ax=ax)
ax.set_xticklabels([int(year) for year in df_decade_rating.index], rotation=0)
ax.set_title('Average TMDB Movie Rating by Decade of Movie Release')
ax.set_xlabel('Decade')
ax.set_ylabel('Average Rating (Out of 10)')
plt.savefig('figures/rating_by_decade.png')

# Genres by year of movie release
df_genre = df.explode('genres')
df_genre_frequency = df_genre.groupby([df['release_date'].dt.year, 'genres'])['genres'].size().unstack()
rare_cols = [col for col in df_genre_frequency.columns if df_genre_frequency[col].sum() < df_genre_frequency.sum().mean()]
df_genre_frequency['Other'] = df_genre_frequency[rare_cols].sum(axis=1)
df_genre_frequency = df_genre_frequency.drop(columns=rare_cols)

labelpad = 10
fig, ax = plt.subplots(figsize=(16, 12))
df_genre_frequency.plot.area(stacked=True, ax=ax)

ax.set_xlabel('Year', labelpad=labelpad)
ax.set_ylabel('Number of Movies', labelpad=labelpad)
ax.set_title('Movie Genre By Year of Release')
plt.tight_layout()
plt.savefig('figures/genres_released_by_year.png')

# Compare relationships between budget, revenue, and average rating
corr_mask = ~df[['budget', 'revenue', 'vote_average']].isna()
df_corr = df[corr_mask]
budget = df_corr['budget'] / 1_000_000
revenue = df_corr['revenue'] / 1_000_000
rating = df_corr['vote_average']
random_cmap = np.arange(0, df_corr.shape[0])

fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(30, 12))
ax[0].scatter(budget, revenue, c=random_cmap, cmap='Greens_r')
ax[0].set_ylim(0, revenue.max() + 500)
ax[0].set_xlim(0, budget.max())
ax[0].set_xlabel('Budget (In Millions)', labelpad=labelpad)
ax[0].set_ylabel('Revenue (In Millions)', labelpad=labelpad)
budget_v_revenue_slope = linregress(x=budget, y=revenue).slope
budget_v_revenue_intercept = linregress(x=budget, y=revenue).intercept
budget_v_revenue_regression = budget_v_revenue_slope * budget + budget_v_revenue_intercept
ax[0].plot(budget, budget_v_revenue_regression, color='lightcoral', label='Production Budget to Revenue Trend')
ax[0].set_title('Total Movie Revenue by Total Movie Budget')
ax[0].legend()

ax[1].scatter(budget, rating, c=random_cmap, cmap='Blues_r')
ax[1].set_xlim(0, budget.max())
ax[1].set_xlabel('Budget (In Millions)', labelpad=labelpad)
ax[1].set_ylabel('Average Rating (Out of 10)', labelpad=labelpad)
budget_v_rating_slope = linregress(x=budget, y=rating).slope
budget_v_rating_intercept = linregress(x=budget, y=rating).intercept
budget_v_rating_regression = budget_v_rating_slope * budget + budget_v_rating_intercept
ax[1].plot(budget, budget_v_rating_regression, color='sandybrown', label='Production Budget to Average Rating Trend')
ax[1].set_title('Average user Rating by Total Movie Budget')
ax[1].legend()

ax[2].scatter(revenue, rating, c=random_cmap, cmap='Purples_r')
ax[2].set_xlim(0, revenue.max())
ax[2].set_xlabel('Revenue (In Millions)')
ax[2].set_ylabel('Average Rating (Out of 10)')
revenue_v_rating_slope = linregress(x=revenue, y=rating).slope
revenue_v_rating_intercept = linregress(x=revenue, y=rating).intercept
revenue_v_rating_regression = revenue_v_rating_slope * revenue + revenue_v_rating_intercept
ax[2].plot(revenue, revenue_v_rating_regression, color='yellowgreen', label='Revenue to Average Rating Trend')
ax[2].set_title('Average User Rating by Total Movie Revenue')
ax[2].legend()
plt.savefig('figures/budget_revenue_rating_trends')
plt.show()