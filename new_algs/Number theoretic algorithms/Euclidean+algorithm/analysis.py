'''
CSCI 620 Project
TMDB Movie Dataset Analysis
Link to dataset: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data

Contributors:
Akshay Pudage (ap7558@rit.edu)
Pallavi Chandanshive (pvc8661@rit.edu)
Sahil Pethe (ssp5329@rit.edu)

This program is the heart of analysis. It returns top 10 similar movies to the user selected
movie.
'''

import pandas as pd
import warnings
from sklearn.neighbors import NearestNeighbors
import sqlalchemy as p
from nltk.corpus import wordnet
warnings.simplefilter(action='ignore', category=FutureWarning)


def addDirector(movies,person,crew):
    """
    Appends directors to the movies dataframe
    :param movies: movies dataframe
    :param person: person dataframe
    :param crew: crew dataframe
    :return: movies dataframe with directors appended
    """
    person_dict = {}
    for i in person.itertuples():
        if i.person_id not in person_dict:
            person_dict[i.person_id] = i.name

    movies['director'] = None
    g_movie = {}
    for j in crew.itertuples():
        if j.job == 'Director':
            if j.movie_id in g_movie:
                l = g_movie[j.movie_id]
                l.append(person_dict[j.person_id])
                g_movie[j.movie_id] = l
            else:
                g_movie[j.movie_id] = [person_dict[j.person_id]]

    for index, row in movies.iterrows():
        movie_id = row.id
        if movie_id in g_movie:
            g = g_movie[movie_id]
            if len(g) >= 1:
                movies.set_value(index, 'director', g[0])
            else:
                movies.set_value(index, 'director', None)
        else:
            movies.set_value(index, 'director', None)

    return movies

def addProduction(movies,production_companies,prouction_movie):
    """
    Appeends production company information to movies dataframe
    :param movies: movies dataframe
    :param production_companies: dataframe
    :param prouction_movie: dataframe
    :return: movies dataframe with appended prodcution companies
    """
    production_dict = {}
    for i in production_companies.itertuples():
        if i.id not in production_dict:
            production_dict[i.id] = i.company_name
    movies['production'] = None
    g_movie = {}
    for j in prouction_movie.itertuples():
        if j.movie_id in g_movie:
            l = g_movie[j.movie_id]
            l.append(production_dict[j.company_id])
            g_movie[j.movie_id] = l
        else:
            g_movie[j.movie_id] = [production_dict[j.company_id]]

    for index, row in movies.iterrows():
        movie_id = row.id
        if movie_id in g_movie:
            g = g_movie[movie_id]
            if len(g) >= 1:
                movies.set_value(index, 'production', g[0])
            else:
                movies.set_value(index, 'director', None)
        else:
            movies.set_value(index, 'director', None)
    return movies


def addActors(movies,person,cast):
    """
    Appends top 3 actors to the movies dataframe
    :param movies: dataframe
    :param person: dataframe
    :param cast: dataframe
    :return: movies dataframe with top 3 actors appended
    """
    person_dict = {}
    for i in person.itertuples():
        if i.person_id not in person_dict:
            person_dict[i.person_id] = i.name

    movies['actor1'] = None
    movies['actor2'] = None
    movies['actor3'] = None
    g_movie = {}
    for j in cast.itertuples():
        if j.movie_id in g_movie:
            l = g_movie[j.movie_id]
            l.append(person_dict[j.person_id])
            g_movie[j.movie_id] = l
        else:
            g_movie[j.movie_id] = [person_dict[j.person_id]]

    for index, row in movies.iterrows():
        movie_id = row.id
        if movie_id in g_movie:
            g = g_movie[movie_id]
            if len(g) >= 3:
                movies.set_value(index, 'actor1', g[0])
                movies.set_value(index, 'actor2', g[1])
                movies.set_value(index, 'actor3', g[2])
            elif len(g) >= 2:
                movies.set_value(index, 'actor1', g[0])
                movies.set_value(index, 'actor2', g[1])
            elif len(g) >= 1:
                movies.set_value(index, 'actor1', g[0])
            else:
                movies.set_value(index, 'actor1', None)
                movies.set_value(index, 'actor2', None)
                movies.set_value(index, 'actor3', None)
        else:
            movies.set_value(index, 'actor1', None)
            movies.set_value(index, 'actor2', None)
            movies.set_value(index, 'actor3', None)
    return movies


def addKeywords(movies,keywords,keyword_movie):
    """
    Appends keywords to the movies dataframe.
    :param movies: dataframe
    :param keywords: dataframe
    :param keyword_movie: dataframe
    :return: movies dataframe with appended keywords
    """
    keyword = {}
    for i in keywords.itertuples():
        if i.id not in keyword:
            keyword[i.id] = i.keyword

    movies['keyword'] = None
    # movies['keyword2'] = None
    # movies['keyword3'] = None
    g_movie = {}
    for j in keyword_movie.itertuples():
        if j.movie_id in g_movie:
            l = g_movie[j.movie_id]
            l += "," + keyword[j.keyword_id]
            g_movie[j.movie_id] = l
        else:
            g_movie[j.movie_id] = keyword[j.keyword_id]

    for index, row in movies.iterrows():
        movie_id = row.id
        if movie_id in g_movie:
            g = g_movie[movie_id]
            movies.set_value(index,'keyword',g)
        else:
            movies.set_value(index, 'keyword', None)
    return movies

def addGenres(movies,genres,genre_movie):
    """
    Appends genres to movies dataframe
    :param movies: dataframe
    :param genres: dataframe
    :param genre_movie: dataframe
    :return: movies dataframe with appended genres
    """
    genre = {}
    for i in genres.itertuples():
        if i.id not in genre:
            genre[i.id] = i.genre

    movies['genre'] = None

    g_movie = {}
    for j in genre_movie.itertuples():
        if j.movie_id in g_movie:
            l = g_movie[j.movie_id]
            l += "," + genre[j.genre_id]
            g_movie[j.movie_id] = l
        else:
            g_movie[j.movie_id] = genre[j.genre_id]

    for index, row in movies.iterrows():
        movie_id = row.id
        if movie_id in g_movie:
            g = g_movie[movie_id]
            movies.set_value(index,'genre',g)
        else:
            movies.set_value(index, 'genre', None)
    return movies

def popularKeywords(movies):
    """
    Returns a list of keyword counts.
    :param movies: movies dataframe
    :return:
    """
    popular_keyword = {}
    for keywords in movies['keyword']:
        if pd.isnull(keywords):
            continue
        else:
            keywords = keywords.split(',')
            for keyword in keywords:
                if keyword in popular_keyword:
                    popular_keyword[keyword] += 1
                else:
                    popular_keyword[keyword] = 1
    return popular_keyword

def popularKeywordsList(popular_keywords_dict):
    """
    Converts the popular keywords dictionary to a list
    :param popular_keywords_dict: popular keywords dictionary with count
    :return: list of popular keywords
    """
    popular_keywords_list = []
    for key,value in popular_keywords_dict.items():
        popular_keywords_list.append([key,value])

    popular_keywords_list.sort(key=lambda x: x[1],reverse=True)
    return popular_keywords_list


def simplifyKeywords(popular_keywords,popular_keywords_dict):
    """
    Finds replacement of a keyword with a popular/frequently occuring synonym
    :param popular_keywords:
    :param popular_keywords_dict:
    :return:
    """
    keyword_replacement = {}
    for [keyword,occurrence] in popular_keywords:
            possible_replacements = []
            synonyms = getSynonym(keyword)
            for word in synonyms:
                if word in popular_keywords_dict:
                    possible_replacements.append([word,occurrence])
            possible_replacements.sort(key=lambda x: x[1],reverse=True)
            if len(possible_replacements) > 0:
                keyword_replacement[keyword] = possible_replacements[0][0]
            else:
                keyword_replacement[keyword] = keyword
    return keyword_replacement


def getSynonym(word):
    """
    Returns synonyms of the input word.
    :param word: word
    :return: list of synonyms
    """
    synonyms = set()
    for word in wordnet.synsets(word):
        for w in word.lemma_names():
            if '.n' in word.name():
                synonyms.add(w.replace('_',' '))
    return synonyms

def replaceKeywords(movies,keyword_replacement,popular_keywords_dict):
    """
    Replaces keywords with popular synonyms to simplify number of keywords.
    :param movies: movies dataframe
    :param keyword_replacement: list of keywords and their synonyms to replace
    :param popular_keywords_dict: popular keywords dictionary
    :return: movies dataframe with simplified keywords
    """
    for index,row in movies.iterrows():
        keyword_to_replace = []
        keywords = row.keyword
        if not pd.isnull(keywords):
            keywords = keywords.split(',')
            for keyword in keywords:
                if popular_keywords_dict[keyword] > 3:
                    keyword_to_replace.append(keyword_replacement[keyword])
        movies.set_value(index,'keyword',','.join(keyword_to_replace))
    return movies



def extractInfo(movies,movie_id):
    """
    Extracts metadata of the input movie
    :param movies: dataframe
    :param movie_id: movie id of the input movie
    :return: extracted metadata of input movie
    """
    index = movies.id[movies.id == movie_id].index.tolist()[0]
    row = movies.iloc[index]
    keywords = row.keyword
    genre = row.genre
    actor1 = row.actor1
    actor2 = row.actor2
    actor3 = row.actor3
    production = row.production
    director = row.director

    information = keywords.split(',')
    information += genre.split(',')
    information.append(actor1)
    information.append(actor2)
    information.append(actor3)
    information.append(director)
    information.append(production)

    return information

def addRows(movies,information):
    """
    Appends additional rows for K-NN analysis to movies dataframe
    :param movies: movies dataframe
    :param information: input movie metadata
    :return: movies dataframe
    """
    for element in information:
        movies[element] = 0
    return movies

def checkIfMatch(movies,information):
    """
    Checks if metadata of movies in the dataframe matches with the metadata
    of the input movie
    :param movies: dataframe
    :param information: metadata of input movie
    :return: movies dataframe with matched metadata
    """
    columns = ['genre','keyword','director','actor1','actor2','actor3','production']

    for index,row in movies.iterrows():
        for column in columns:
            value = row[column]
            if not pd.isnull(value):
                if column == 'genre' or column == 'keyword':
                    value = value.split(',')
                    for val in value:
                        if val in information:
                            movies.set_value(index,val,1)
                else:
                    if value in information:
                        movies.set_value(index, value, 1)


    return movies




def recommendMovie(input_movie):
    """
    Takes in the movie title and recommends 10 movies similar to it using K-NN classifer
    :param input_movie: title of the input movie
    :return: list of 10 similar movies
    """
    
    # Create SQL connection
    connectionSQL = p.create_engine('postgresql://postgres:1@localhost:5433/tmdb')
    
    # Read SQL Tables into Dataframes
    crew = pd.read_sql_table('crew', connectionSQL)
    genres = pd.read_sql_table('genres', connectionSQL)
    genre_movie = pd.read_sql_table('genre_movie', connectionSQL)
    keywords = pd.read_sql_table('keywords', connectionSQL)
    person = pd.read_sql_table('person', connectionSQL)
    keyword_movie = pd.read_sql_table('keyword_movie', connectionSQL)
    cast = pd.read_sql_table('cast', connectionSQL)
    movies = pd.read_sql_table('movies', connectionSQL)
    production_companies = pd.read_sql_table('production_companies',connectionSQL)
    production_movies = pd.read_sql_table('production_movie',connectionSQL)

    # Merge tables into one for easier analysis
    movies = addProduction(movies,production_companies,production_movies)
    movies = addGenres(movies, genres, genre_movie)
    movies = addKeywords(movies, keywords, keyword_movie)
    movies = addActors(movies, person, cast)
    movies = addDirector(movies, person, crew)

    # Get popular keywords
    popular_keywords_dict = popularKeywords(movies)
    popular_keywords_list = popularKeywordsList(popular_keywords_dict)
    
    # Simplify keywords by replacing with synonyms
    keyword_replacement = simplifyKeywords(popular_keywords_list, popular_keywords_dict)
    movies = replaceKeywords(movies, keyword_replacement, popular_keywords_dict)

    # Extract movie id of the input movie
    inputMovieID = movies.loc[movies['original_title'] == input_movie].id.tolist()[0]

    # Extract metadata of the input movie
    information = extractInfo(movies, inputMovieID)
    
    # Append columns to movies dataframe for analysis.
    movies = addRows(movies, information)
    
    # Check if metadata of the input movie matches with the movies in the dataset
    movies = checkIfMatch(movies, information)

    # Form a matrix of similar movies
    matrix = movies.as_matrix(information)
    
    # Get closest 11 neighbors using K-NN
    nbrs = NearestNeighbors(n_neighbors=11, algorithm='auto', metric='euclidean').fit(matrix)
    index = movies.id[movies.id == inputMovieID].index.tolist()[0]
    matrix = movies.iloc[index].as_matrix(information)
    matrix = matrix.reshape(1, -1)
    distances, indices = nbrs.kneighbors(matrix)
    similar_movies = indices[0][:]
    
    # Get names of the top 10 neighbors
    moviesToRecommend = []
    for movie_id in similar_movies:
        moviesToRecommend.append([movies.iloc[movie_id].original_title,float(movies.iloc[movie_id].vote_average)])

    moviesToRecommend = moviesToRecommend[1:]
    
    # Sort neighbors according to average vote
    moviesToRecommend.sort(key=lambda x: x[1], reverse=True)
    moviesToRecommend = [x[0] for x in moviesToRecommend]
    
    return moviesToRecommend




