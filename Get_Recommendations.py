from Directories import movies,movie_correlation,moviesWithGenres,pd,userdb,re,getHour


class Recommendations():
 def get_simimlar_movies(self,movie_name, user_rating):
    similar_score= movie_correlation[movie_name] * (
            user_rating - 2.5)
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score


 def get_recommendations(self,retrieved_user_movies):
    retrieved_user_movies = retrieved_user_movies.drop_duplicates('movieId',keep='last')

    #Getting retrieved user movie table which will be used to generate recommendations
    retrieved_user_movies = retrieved_user_movies.drop('socialsetting', 1).drop('userId', 1).drop('timeofday', 1)
    print("These are the movies the user rated:")
    print(retrieved_user_movies)

    similar_movies = pd.DataFrame()
    for index, row in retrieved_user_movies.iterrows():
        movie = str(row[2])
        rating = int(row[1])
        similar_movies = similar_movies.append(self.get_simimlar_movies(movie, rating), ignore_index=True)
    similar_movies = str(similar_movies.sum().sort_values(ascending=False).head(50))
    similar_movies = re.sub(r'[^a-zA-Z-, ]', '', similar_movies)
    similar_movies = re.split(r" {3,}", similar_movies)

    collabf_df= pd.DataFrame(columns=['movieId', 'title', 'genres'])
    for i in similar_movies:
        s = movies[movies['title'] == i]
        if i not in  collabf_df['title']:
            collabf_df =  collabf_df.append(s, ignore_index=True, sort=True)

    print("below shows the collaborative filtering only recommendation")
    collabf_df = collabf_df[~ collabf_df['movieId'].isin(userdb["movieId"])]
    print( collabf_df.filter(['title','genres']))
    self.get_hybrid(collabf_df, retrieved_user_movies)




 def get_hybrid(self,collabf_df,retrieved_user_movies ):
    # CONTENT BASED FILTERING(BUILDING USER PROFILE)

    # Here we are converting the users movie table  into to a list format
    inputMovies = pd.merge(movies, retrieved_user_movies).drop('genres', axis=1).drop('year', axis=1)

    # getting list of user rating which will be required to be used to calculate the users genre table
    user_rating_list = []
    for i in inputMovies['rating']:
        user_rating_list.append(i)

    # building the user content based profile
    # getting only the genre values so that it can be transposed to create the users profile

    userMovies = moviesWithGenres[moviesWithGenres['movieId'].isin(inputMovies['movieId'])]
    userMovies = userMovies.fillna(0)
    userMovies = userMovies.reset_index(drop=True)
    userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
    print(userGenreTable)
    userProfile = userGenreTable.transpose().dot(user_rating_list)
    print("This is the users movie profile")
    print(userProfile.sort_values(ascending=False))

    # getting the new reccomendations with the hybrid approach( multiplying user profile with reccomended movies)
    # I am then sorting the sum, this should push the genre movies the useer tends to like the most to the top of the page
    collabf_genretable_df = moviesWithGenres[moviesWithGenres['movieId'].isin(collabf_df['movieId'])]
    collabf_genretable_df = collabf_genretable_df.set_index(collabf_genretable_df['movieId']).fillna(0)
    collabf_genretable_df = collabf_genretable_df.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
    recommendationTable = ((collabf_genretable_df * userProfile).sum(axis=1)) / (userProfile.sum())
    recommendationTable = recommendationTable.sort_values(ascending=False)
    recommendationTable = recommendationTable.reset_index()


    hybridRecommendations = pd.DataFrame(columns=['movieId', 'title', 'genres'])
    for i in recommendationTable['movieId']:
        get_movie_row = collabf_df[collabf_df['movieId'] == i]
        hybridRecommendations = hybridRecommendations.append(get_movie_row, ignore_index=True, sort=True)
        hybridRecommendations = hybridRecommendations.filter(['title', 'genres', 'movieId'])
        hybridRecommendations = hybridRecommendations[~hybridRecommendations['movieId'].isin(userdb["movieId"])]
    print("Here are your hybrid recommendations:")
    print(hybridRecommendations.filter(['title', 'genres']))

    return recommendationTable



 def general_recommendations(self,userId):
    general_userdb = userdb[userdb['userId'].isin([userId])]
    printRec = self.get_recommendations(general_userdb)


 def context_recommendations(self,userId):
    current_user_db = userdb
    current_user_db  = current_user_db [current_user_db ['userId'].isin([userId])]
    while True:
        Social = {1: "alone", 2: "friends", 3: "partner", 4: "family"}
        socialInput = int(
            input("Are you with alone with a partner or with family?(1: alone, 2: friends, 3: partner, 4:family"))
        socialContent = Social.get(socialInput)
        if Social.get(socialInput):
            break
    current_user_db  = current_user_db  [current_user_db ['socialsetting'].isin([socialContent])]
    print("these are movies we recommend when you are " + " " + socialContent)
    self.get_recommendations(current_user_db)

    print("these are the top picks for the current timeofday")
    current_user_db = current_user_db[current_user_db['timeofday'].isin([getHour()])]
    self.get_recommendations(current_user_db)
