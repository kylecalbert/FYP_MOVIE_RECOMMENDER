from Cinema_Recommendations import Cinema_Recommendations
from Directories import pd
from Get_Recommendations import Recommendations
from Directories import movies,loginfile,sys,randint,getHour
from Rate_Movies import Rate_Movies


#This is a final year  project which allows users to rate movies and get recommendation based on their ratings.
#When the user rates a movie, they are asked to input their social setting, eg. whether alone or with friends
#..so that the system can leearn to determine what their prefrences are given context
#the time of da when the user rates the movie is also recorded


class Login():

 def loginMenu(self):
    statusOptions = {"Y", "N"}
    while True:
        status = input("Have you registered for the System? Y/N")
        if status in statusOptions:
            break
    if status == "Y":
        print("YES")
        self.login()
    else:
        self.create()


#The first time a user signs in they will be asked to rate several movies to get started
 def firsttimeLogin(self,userId, getIndex):
    global userdb
    tempuserDb = pd.DataFrame(columns=['userId', 'movieId', 'rating', 'title', 'socialsetting','timeofday'])

    list = ["Dark Knight", "Inception", "Minions", "Shrek", "Shaun of the Dead", "Deadpool", "Gone Girl",
            "John Wick", "La La Land", "Notebook"]
    print(
        "Welcome! Please rate the following movies to get the system up and running: please note that if you havent seen a movie "
        "give it a 3")

     #Getting information such as the movieId, to write it to the user table
    for movietitle in list:
        foundMovie = movies[movies['title'].isin([movietitle])]
        movieIndex = foundMovie.index
        getmovieTable = movies.iloc[movieIndex]
        movieid = int(getmovieTable['movieId'])
        print("Please rate the movie" + " " + movietitle)
        while True:
            try:
                userRating = int(input("Enter the rating:"))
            except ValueError:
                print("Please enter a valid rating")
            else:
                break

        tempuserDb = tempuserDb.append(
            pd.Series([userId, movieid, userRating, movietitle, "alone",getHour()],
                      index=tempuserDb.columns),
            ignore_index=True)
    userdb = pd.concat([userdb, tempuserDb], axis=0, sort=True).reset_index(drop=True)


    loginfile.at[getIndex, 'firstTime'] = "n"
    loginfile.to_csv('/Users/macbook/Documents/FYPDATABASE/loginfile.csv', mode='w',index=False)
    userdb.to_csv('/Users/macbook/Documents/FYPDATABASE/userdb.csv', mode='w',index=False)


 def login(self):
    userId = -1
    message = "False"
    getIndex = 0
    while True:
        username = input("Please enter a username")
        password = input("Please enter a password")
        for index, row in loginfile.iterrows():
            if row['Username'] == username and row['Password'] == password:
                userId = row['userId']
                message = "True"
                getIndex = index
                break
        if message == "True" and row['firstTime'] == "n":
            break
        elif message == "True" and row['firstTime'] == "y":

            loginfile.to_csv('/Users/macbook/Documents/FYPDATABASE/loginfile.csv', mode='w',index=False)
            self.firsttimeLogin(userId, getIndex)
            sys.exit(-1)

        else:
            self.loginMenu()

    self.optionMenu(userId)


# This is were a user creates an account
 def create(self):
    while True:
        username = input("Please enter a username you want to create")
        password = input("Please enter a password")
        found = loginfile[loginfile['Username'].isin([username])]
        if int(len(found) >= 1):
            print("Username already exists")
        else:
            break

    while True:
        value = randint(672, 2000)
        found2 = loginfile[loginfile['userId'].isin([value])]
        if (int(len(found2) < 1)):
            break
    s = loginfile.append(pd.Series([username, password, value, 'y'], index=loginfile.columns), ignore_index=True)
    s.to_csv('/Users/macbook/Documents/FYPDATABASE/loginfile.csv', mode='w',index=False)
    print("new user succesfuly created")
    sys.exit(-1)

 # Once a user signs in they will be braought to the option menu where they can choose to rate or egt recommendations

 def optionMenu(self,userId):
     recommendation_class = Recommendations()

     Setting = {1: "alone", 2: "friends", 3: "partner", 4: "family"}
     choiceMenu = {1, 2, 3, 4}

     while True:
         userChoice = int(input(
             "Do you want to get reccomendations or rate movies??(1: context based reccomendations, 2: rate movies,3: Genral Recommendations,4: Cinema Movies)"))
         if userChoice in choiceMenu:
             break
     if userChoice == 1:
         recommendation_class.context_recommendations(userId)
     elif userChoice == 2:
         rate_movies_class = Rate_Movies()
         rate_movies_class.rateMovies(userId, Setting)
     elif userChoice == 3:
         recommendation_class.general_recommendations(userId)
     else:
         cinema_recommendations_class = Cinema_Recommendations()
         cinema_recommendations_class.cinemaRecommendations(userId)

login = Login()
login.loginMenu()

# Getting the current timeofweek of day to reccomend movies for specific timeofweek


