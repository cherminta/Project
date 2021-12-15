#After finish putting information in json file, Clean the information in json 
#convert running times into integer / convert dates into datetime obj / convert budget&box office into numbers
#split up the long strings
from bs4 import BeautifulSoup as bs
import json

def load_data(title):
    with open(title) as f:
        return json.load(f)

movie_info_list = load_data("movie_data_cleaned.json")

#convert running time into integer (minutes)

def minute_to_int(running_time):
    if running_time == "N/A":
        #do not have running time
        return None

    #"85 minute" "85 min" split on a space
    if isinstance(running_time, list):
        #some have more than 1 value (use the first one)
        minute = running_time[0]
        value = int(minute.split(" ")[0])
        return value

    else:
        value = int(running_time.split(" ")[0])
        return value

for movie in movie_info_list:
    movie["Running time (minutes)"] = minute_to_int(movie.get("Running time", "N/A"))

## **get minutes of all** print([movie.get("Running time (minutes)", "N/A")for movie in movie_info_list])

#convert budget and box office (string) to numbers 

import re

#\d+ = digit
#number may come in from of 790,000 (with comma)
#we also want demical like 56.7 millions
number = r"\d+(,\d{3})*\.*\d*"

def str_to_int(budget):
    value_string = re.search(number, budget).group()
    #strip ot comma before solutions
    value = float(value_string.replace(",", ""))
    #search for number 
    #group() = Return the string matched by the RE  
    return value


print(str_to_int("$790,000"))
