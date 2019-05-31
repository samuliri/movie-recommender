import numpy as np
import pandas as pd

# READ RATINGS
ratings_data = pd.read_csv("ratings.csv")
#print(ratings_data.head())

# READ MOVIES
movie_names = pd.read_csv('movies.csv')
#print(movie_names.head)

# MERGE MOVIE DATA
movie_data = pd.merge(ratings_data, movie_names, on = 'movieId')
#print(movie_data.head)
#print(movie_data.groupby('title')['rating'].mean().sort_values(ascending=False).head())
#print(movie_data.groupby('title')['rating'].count().sort_values(ascending=False).head())

# FRAME THE TITLE/RATING DATA
ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
#print(ratings_mean_count.head())

# RATING DATA VISUALIZATIONS
'''
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
ratings_mean_count['rating_counts'].hist(bins=50)
plt.show()

plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
ratings_mean_count['rating'].hist(bins=50)
plt.show()

plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True
sns.jointplot(x='rating',y='rating_counts',data = ratings_mean_count, alpha = 0.4)
plt.show()
'''

# GET USERS MOVIE RATINGS
user_movie_rating = movie_data.pivot_table(index = 'userId', columns = 'title', values = 'rating')
#print(user_movie_rating.head())

# GET RATINGS BY MOVIE TITLE
movie_title = 'Forrest Gump (1994)'
forrest_gump_ratings = user_movie_rating[movie_title]
#print(forrest_gump_ratings)

# PANDAS CORRELATION BETWEEN USERS AND SELECTED MOVIE RATINGS
movies_like_forrest_gump = user_movie_rating.corrwith(forrest_gump_ratings)

corr_forrest_gump = pd.DataFrame(movies_like_forrest_gump,columns=['Correlation'])
corr_forrest_gump.dropna(inplace=True)
corr_forrest_gump = corr_forrest_gump.join(ratings_mean_count['rating_counts'])

# PRINT OUTPUT
#print(corr_forrest_gump.head())
print("\n MOVIES SIMILAR RATINGS THAN:")
print(movie_title)
print(corr_forrest_gump[corr_forrest_gump['rating_counts']>50].sort_values('Correlation', ascending=False))
