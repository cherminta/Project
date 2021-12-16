#clean more of information

import pickle

#load data from json file 

def load_data_pickle(name):
    with open(name, "rb") as f:
        return pickle.load(f)

movie_info_list = load_data_pickle("disney_movie_data_final.pickle")


def dis_com_name(name):
    """distributed by: some company name come in list"""

    if name == "N/A":
        return None
    
    #some of its distributed by name are in list
    if isinstance(name, list):
        return name[0]

    else:
        return name


#imdb / metascore / rooten tomatoes are not integers (convert to int)

import re

imdb_score = r"\d+\.*\d*" #7.1 (out of 10)

def imdb_num(score):
    """convert ex. 7.1 to float"""

    if score == "N/A":
        return None

    try:

        imdb_n = re.search(imdb_score, score).group()
        
        if imdb_n:
            value = float(imdb_n)
            return value
    
    except: 
        
        return None


meta_score = r"\d+"

def meta_int(score):
    """convert 95 into integer"""

    if score == "N/A":
        return None

    try:
        meta_num = re.search(meta_score, score)

        if meta_num:
            value = meta_num.group()
            value = int(value)
            return value
    
    except:
        return None


rotten_tomato_score = r"\d+\%*"

def rotten_tomato_int(score):
    """convert 90% to integer"""

    if score == "N/A":
        return None

    try:
        rotten_tomato_num = re.search(rotten_tomato_score, score)

        if rotten_tomato_num:
            value = rotten_tomato_num.group()
            value = int(value.replace("%", ""))
            return value
    
    except:
        return None

for movie in movie_info_list:

    movie["Distributed by"] = dis_com_name(movie.get("Distributed by", "N/A"))
    movie["imdb"] = imdb_num(movie.get("imdb", "N/A"))
    movie["Metascore"] = meta_int(movie.get("Metascore", "N/A"))
    movie["Rotten tomatoes"] = rotten_tomato_int(movie.get("Rotten tomatoes", "N/A"))
    

""" running_time = df.sort_values(["Running time (int)"], ascending=True) """

print(movie_info_list[2])
