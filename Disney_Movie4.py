#get lastest inforamation (from disney_movie_data_final.pickle)
#to save in json (have to change datetime)

import json

from numpy.core.numeric import full
from pandas.core.indexes import base
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


# save_data("disney_movie_final.json", movie_info_copy)


#CONVERT TO CSV

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
#dataframe of information
df = pd.DataFrame(movie_info_list)
#add HTML to wiki
r = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films')
soup = bs(r.content, "lxml")
movies = soup.select(".wikitable.sortable i a")
base_path = "https://en.wikipedia.org/"
link = []

title_list = []
for mov in movie_info_list:
    title_list.append(mov['title'])


count = 0
prev = 0
for movie in movies:
    rel_path = movie['href']
    full_path = base_path + rel_path
    title = movie['title'].strip()
    if len(link) == 501:
        break
    
    if '(' in title:
        title = title.split('(')
        title = title[0]
        title = title[:-1]
    
    if count == 0:
        link.append(full_path)
        count += 1
    elif title == title_list[count] and prev == 0:
        link.append(full_path)
        count += 1
    elif title == title_list[count]:
        link.append(full_path)
        count += 1
        prev = 0
    elif title == title_list[count+1] and prev == 1:
        link.append(prev_path)
        link.append(full_path)
        count += 2
        prev = 0
    else:
        prev = 1 #have but not correct name 

    prev_path = full_path

df = df.assign( HTML=link)

df.to_csv("last_disney_movie_data_final.csv")

ar_title = df.sort_values(['title'], ascending=True)
ar_title.to_csv("movie_title_ar")

ar_title_back = df.sort_values(['title'], ascending=False)
ar_title_back.to_csv("movie_title_ba")

ar_date = df.sort_values(['Release date (datetime)'], ascending=True)
ar_date.to_csv("movie_date_ar")

ar_date_back = df.sort_values(['Release date (datetime)'], ascending=False)
ar_date_back.to_csv("movie_date_ba")

ar_length = df.sort_values(["Running time (minutes)"], ascending=True)
ar_length.to_csv("movie_length_ar")

ar_length_back = df.sort_values(["Running time (minutes)"], ascending=False)
ar_length_back.to_csv("movie_length_ba")

ar_budget = df.sort_values(['Budget (float)'], ascending=True)
ar_budget.to_csv("movie_budget_ar")

ar_budget_back = df.sort_values(['Budget (float)'], ascending=False)
ar_budget_back.to_csv("movie_budget_ba")

ar_imdb = df.sort_values(['imdb'], ascending=True)
ar_imdb.to_csv("movie_imdb_ar")

ar_imdb_back = df.sort_values(['imdb'], ascending=False)
ar_imdb_back.to_csv("movie_imdb_ba")

ar_meta = df.sort_values(['Metascore'], ascending=True)
ar_meta.to_csv("movie_meta_ar")

ar_meta_back = df.sort_values(['Metascore'], ascending=False)
ar_meta_back.to_csv("movie_meta_ba")

ar_rotten = df.sort_values(['Rotten tomatoes'], ascending=True)
ar_rotten.to_csv("movie_rotten_ar")

ar_rotten_back = df.sort_values(['Rotten tomatoes'], ascending=False)
ar_rotten_back.to_csv("movie_rotten_ba")