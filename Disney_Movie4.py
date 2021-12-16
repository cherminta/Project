#get lastest inforamation (from disney_movie_data_final.pickle)
#to save in json (have to change datetime)

import json
from Disney_Movie2 import load_data_pickle

movie_info_list = load_data_pickle("final2_disney_movie_data.pickle")

#in order to lelt movie_info_data stay the same (not changed)
movie_info_copy = [movie.copy() for movie in movie_info_list]

for movie in movie_info_copy:
    #replace Release date field with an actual string instead of datetime (to save in json)

    current_date = movie["Release date (datetime)"]

    if current_date:
        movie["Release date (datetime)"] = current_date.strftime("%B %d, %Y")
    
    else:
        movie["Release date (datetime)"] = None


def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        #encode Python objects into JSON data
        json.dump(data, f, ensure_ascii=False, indent=2)
        #resulting JSON store Unicode characters as-is instead of \u escape sequence.


save_data("disney_movie_final.json", movie_info_copy)


#CONVERT TO CSV

import pandas as pd

#dataframe of information
df = pd.DataFrame(movie_info_list)

df.to_csv("disney_movie_data_final.csv")