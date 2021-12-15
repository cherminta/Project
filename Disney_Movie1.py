import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films')

#convert to bs obj.
soup = bs(r.content, "lxml") #html parser
#print the HTML
contents = soup.prettify() #content in the website

#select finds multiple instances and returns a list
movies = soup.select(".wikitable.sortable i a") #a bec of some movies have no links
#movies[0].a['href'] = link of the first movie

def get_content_value(row_data): #some have more little list inside(li or list item)
    #name of producers (more than 1)
    if row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
        #specify string anf strip whitespace   
    elif row_data.find("br"):
        #strip the long string into a list (keep them seperated)
        #names of people are in one line
        return[text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0", " ")
        # =row.find("td").get_text()

def clean_tags(soup):
    for tag in soup.find_all(["sup", "span", "b"]):
        #delete the tags [1] [2] / additional date / specific position 
        tag.decompose()

def get_info_box(url):      

    r = requests.get(url)
    soup = bs(r.content, "lxml") #html parser
    #print the HTML
    info_box = soup.find(class_="infobox vevent") 
    #info in the box(of movie)
    info_rows = info_box.find_all("tr") #table row

    clean_tags(soup)

    movie_info = {}

    for index, row in enumerate(info_rows): #counting index from 0
        if index == 0:
            movie_info['title'] = row.find('th').get_text(" ", strip=True) #table head
    
        else:

            header = row.find("th")

            if header:
                content_key = row.find("th").get_text(" ", strip=True) #left box(directed by)
                #content_value = row.find("td").get_text() #right side(name)(table data)
                #.get_text(" ", strip=True) to join them together (production companies)
                content_value = get_content_value(row.find("td"))
                movie_info[content_key] = content_value

    return movie_info

#Clean the references (remove these [1] [2] and more)
#Split up the long strings

movies = soup.select(".wikitable.sortable i a")
#Find tags beneath other tags
base_path = "https://en.wikipedia.org/"

movie_info_list = []

for index, movie in enumerate(movies):
    if index % 10 == 0:
        print(index)
        
    try:
        rel_path = movie['href']
        full_path = base_path + rel_path
        title = movie['title']
        
        movie_info_list.append(get_info_box(full_path))

    except Exception as e:
        print(movie.get_text())
        print(e)
        

#Save/Reload Movie Data
#save in json file 

import json

def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        #encode Python objects into JSON data
        json.dump(data, f, ensure_ascii=False, indent=2)
        #resulting JSON store Unicode characters as-is instead of \u escape sequence.

def load_data(title):
    with open(title, encoding='uft-8') as f:
        return json.load(f)

save_data("movie_data_cleand.json", movie_info_list)