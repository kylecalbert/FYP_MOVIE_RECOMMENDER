from Directories import requests,TfidfVectorizer,pandas,pd,linear_kernel

class Cinema_Recommendations():
 def cinemaRecommendations(userId):
    global userdb
    global tmdb
    new_userdb_df = userdb[userdb['userId'].isin([userId])]

    Setting = {1: "alone", 2: "friends", 3: "partner", 4: "family"}

    while True:
        social = int(
            input("Are you going to the cinema 1: Alone, 2: With Friends, 3: With Partner, 4: With Family"))
        getSocial = Setting.get(social)
        if Setting.get(social):
            break

    new_userdb_df = new_userdb_df[userdb['socialsetting'].isin([getSocial])]
    new_userdb_df = new_userdb_df[new_userdb_df['rating'] > 3]

    print("these are the movies you liked" + " " + getSocial)
    print(new_userdb_df['title'])

    userInput = input("Enter the Movie")


    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=95db3b6a42533a2096e949619fe446a2&language=en-US"


    getResults = []
    # Looping through several pages to get films from the api
    # The api can only return one page at a time
    page_num = 1
    while page_num < 5:
        url = "https://api.themoviedb.org/3/movie/now_playing?api_key=95db3b6a42533a2096e949619fe446a2&&page=" + str(
            page_num)
        response = requests.get(url)
        data = response.json()
        getResults = getResults + data['results']
        page_num = page_num + 1

    # These are the columns names i want to retrieve from the api object returned
    columns = ['film', 'overview']
    cinemafilms_df = pandas.DataFrame(columns=columns)

    for film in getResults:
        cinemafilms_df.loc[len(cinemafilms_df)] = [film['title'], (film['overview'])]


    cinemafilms_df = cinemafilms_df.rename(columns={'film': 'title'})
    tmdb = tmdb[tmdb.title == userInput]
    cinemafilms_df = pd.concat([cinemafilms_df, tmdb], axis=0, sort=True).reset_index(drop=True)


    # Defining a TF-IDF vectorizer object which removes all english words such as 'the', 'a' etc..

    tfidf = TfidfVectorizer(stop_words='english')

    cinemafilms_df['overview'] = cinemafilms_df['overview'].fillna('')

    tfidfMatrix = tfidf.fit_transform(cinemafilms_df['overview'])
    cosineSimilarity = linear_kernel(tfidfMatrix, tfidfMatrix)
    indices = pd.Series(cinemafilms_df.index, index=cinemafilms_df['title']).drop_duplicates()

    def cinema_recommendations(title, cosineSimilarity=cosineSimilarity):

        idx = indices[title]

        sim_scores = list(enumerate(cosineSimilarity[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:10]

        movie_indices = [i[0] for i in sim_scores]


        return cinemafilms_df['title'].iloc[movie_indices]

    print(cinema_recommendations(userInput))