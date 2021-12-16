##Add IMDB score /  Rotten tomatoes / Metascore scores
from Disney_Movie2 import load_data_pickle, save_data_pickle

movie_info_list = load_data_pickle("movie_data_moreclean.pickle")

import requests
import urllib

#API link (where all infolramtion of IMDB / Rotten tomatoes / Metascore scores) (OMDb)
# "http://www.omdbapi.com/?apikey=[yourkey]&"


def get_omdb_info(title):

    base_url = "http://www.omdbapi.com/?"
    parameters = {"apikey": "9b7e2f04", 't': title} #API_KEY
    para_encoded = urllib.parse.urlencode(parameters)
    full_url = base_url + para_encoded

    return requests.get(full_url).json()


def get_rotten_tomato_score(omdb_info):
    #rotten tomato is in the list of rating

    ratings = omdb_info.get("Ratings", [])
    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            return rating["Value"]

    #in case of no ratings
    return None

for movie in movie_info_list:
    title = movie['title']
    omdb_info = get_omdb_info(title)
    movie['imdb'] = omdb_info.get("imdbRating", None)
    movie['Metascore'] = omdb_info.get("Metascore", None)
    movie['Rotten tomatoes'] = get_rotten_tomato_score(omdb_info)


#svae the final data (including these ratings)
save_data_pickle('disney_movie_data_final.pickle', movie_info_list)

