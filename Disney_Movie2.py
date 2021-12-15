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

amount = r"thousand|million|billion"

#money_conversion ("$12.2 million") --> 12200000 #word syntax
word_con = rf"\${number}(-)?\s({amount})"
# - dash (12-13 million) ? = exist or doesn't exist
#money conversion ("$790,000") --> #value syntax
value_con = rf"\${number}"


def word_to_value(word):
    value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    return value_dict[word]

def word_syn(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    word = re.search(amount, string).group()
    word_value = word_to_value(word)
    return value*word_value


def value_syn(string):

    value_string = re.search(number, string).group()
    #strip ot comma before solutions
    value = float(value_string.replace(",", ""))
    #search for number 
    #group() = Return the string matched by the RE  
    return value


def money_conversion(money):

    if isinstance(money, list):
        money = money[0]
    
    word_s = re.search(word_con, money)
    value_s = re.search(value_con, money)

    if word_s:
        word_s = word_s.group()
        return word_syn(word_s)

    elif value_s:
        value_s = value_s.group()
        return value_syn(value_s)


print(money_conversion("$790 million"))
