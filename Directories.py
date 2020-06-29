
from difflib import SequenceMatcher
from datetime import datetime
import re
from random import randint
from sklearn.linear_model import LinearRegression
import pandas
import pandas as pd
import requests # to make TMDB API calls
import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )
import sys


#Sample username: james
#Password: password
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

userdb = pd.read_csv('/Users/macbook/Documents/FYPDATABASE/userdb.csv')
loginfile = pd.read_csv('/Users/macbook/Documents/FYPDATABASE/loginfile.csv')
movies = pd.read_csv('/Users/macbook/Documents/FYPDATABASE/movies.csv')
ratings = pd.read_csv('/Users/macbook/Documents/FYPDATABASE/ratings.csv')
tmdb = pd.read_csv('/Users/macbook/Documents/FYPDATABASE/tmdb.csv')


movies["year"] = movies.title.str.extract('(\(\d\d\d\d\))', expand=False)
movies["year"] = movies.year.str.extract('(\d\d\d\d)', expand=False)
movies["title"] = movies.title.str.replace('(\(\d\d\d\d\))', '')
movies['title'] = movies['title'].apply(lambda x: x.strip())



ratings = pd.merge(movies, ratings).drop(['genres'], axis=1)
user_ratings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')
print("LOADING")
# remmoving all coloumns which have less than 15 non NA values to improve accuracy of system
user_ratings = user_ratings.dropna(thresh=20, axis=1).fillna(0)  # axis = 1 means  dropping of coloumns  0 would be rows
# finding similaritty between movies(using the pearsons correlation)

movie_correlation = user_ratings.corr(method='pearson')
#Creating a copy the movies dataframe and making a movies table which contains the genre table of all movies
moviesWithGenres = movies

genre_list = []
for genres in moviesWithGenres.loc[:, 'genres']:
    split_genres = genres.split('|')
    for genre in split_genres:
        if not genre in genre_list:
            genre_list.append(genre)

for genre in genre_list:
    true_values = moviesWithGenres.loc[moviesWithGenres.genres.str.contains(genre)].movieId.tolist()
    new_values = [1 if movie_id in true_values else 0 for movie_id in moviesWithGenres.loc[:, 'movieId']]
    moviesWithGenres[genre] = new_values


#method to get the time a user rates a movie
def getHour():

    getHour= ""
    now = datetime.now()
    currenthour = now.hour
    print(currenthour)
    hour = int(currenthour)
    if hour >= 2 and hour < 12:
        getHour = "morning"
    elif hour >= 12 and hour < 17:
        getHour = "afternoon"
    elif hour >= 17 and hour < 21:
        getHour= "evening"
    elif hour >= 21 and hour < 24:
        getHour = "night"
    return getHour

