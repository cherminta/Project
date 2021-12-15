##Add IMDB score /  Rotten tomatoes / Metascore scores
from Disney_Movie2 import load_data_pickle

movie_info_list = load_data_pickle("movie_data_moreclean.pickle")

import requests
import urllib

#API link (where all infolramtion of IMDB / Rotten tomatoes / Metascore scores) (OMDb)
# "http://www.omdbapi.com/?apikey=[yourkey]&"


def get_omdb_info(title):

    base_url = "http://www.omdbapi.com/?"
    parameters = {"apikey": "http://www.omdbapi.com/?i=tt3896198&apikey=9b7e2f04", 't': title} #API_KEY
    para_encoded = urllib.parse.urlencode(parameters)
    full_url = base_url + para_encoded

    return requests.get(full_url).json()


def get_rotten_tomato_score(omdb_info):
    #rotten tomato is in the list of rating

    ratings = omdb_info.get("Rating", [])
    

print(get_omdb_info("Bambi"))
