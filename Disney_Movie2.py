#After finish putting information in json file, Clean the information in json 
#clean up references [1]
#convert running times into integer / convert dates into datetime obj / convert budget&box office into numbers
#split up the long strings
import json

def load_data(title):
    with open(title, encoding='uft-8') as f:
        return json.load(f)

movie_info_list = load_data("disney_movie_dtata.json")


