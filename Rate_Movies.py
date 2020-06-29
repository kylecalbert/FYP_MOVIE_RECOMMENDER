from Directories import movies, getHour, userdb
from Directories import SequenceMatcher
from Directories import pd


# the movie name will be passed in and all the movies values in the corresponding row will
# be multiplied  by the users rating, we will use these new ratings to scale the similar movie scores and sort them

class Rate_Movies():

 def rateMovies(self,userId, Setting):
    global userdb

    tempuserDb = pd.DataFrame(columns=['userId', 'movieId', 'rating', 'title', 'socialsetting','timeofday'])

    print("you have chosen to rate movies")
    i = 0;
    numberofratings = int(
        input("enter the number of ratings you want to input"))  # Python 3
    while (i < numberofratings):
        while True:
            inputmovie = input("enter the movie")
            for movie in movies['title']:
                s = SequenceMatcher(None, movie, inputmovie).ratio()
                if s > 0.88:
                    inputmovie = movie
                    break
            foundMovie = movies[movies['title'].isin([inputmovie])]
            movieIndex = foundMovie.index
            getmovieTable = movies.iloc[movieIndex]
            movieid = int(getmovieTable['movieId'])
            movietitle = (getmovieTable['title'])
            movietitle = movietitle.to_string(index=False)
            movietitle = movietitle.strip()
            userRating = int(input("enter the rating"))

            userInput= int(
                input("Were you alone, with friends, with a partner or with family?(1: alone, 2: friends, 3: partner, "
                      "4: family"))
            socialsetting = Setting.get(userInput)


            if Setting.get(userInput):
                break


        tempuserDb = tempuserDb.append(
            pd.Series([userId, movieid, userRating, movietitle, socialsetting,getHour()],
                      index=tempuserDb.columns),
            ignore_index=True)
        i = i + 1
    print(getHour())

    userdb = pd.concat([userdb, tempuserDb], axis=0,sort=True).reset_index(drop=True)

    userdb.to_csv('/Users/macbook/Documents/FYPDATABASE/userdb.csv', mode='w')


# function takes in the users rating and the movie name
# gets similar movies to what the user has rated and returns these siilar movies
# if movie is rated bad we want all similar movies to go down in list so we minus the  similar scores by -2.5, so in esscenceif the movie is rated below 3 the movie correlation will be a negtive











