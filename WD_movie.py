#scraping information from website (List of Disney Movies)
#store it in python dictionary
#first try (Alice in the Wonderland)

import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://en.wikipedia.org/wiki/Alice_in_Wonderland_(2010_film)')

soup = bs(r.content)
#print the HTML
contents = soup.prettify() #content in the website
#turn a soup into a nicely formatted Unicode string, 
#with a separate line for each tag and each string

info_box = soup.find(class_="infobox vevent") #info in the box(of movie)
info_rows = info_box.find_all("tr") #table row
##for row in info_rows:
##  print(row.prettify())

#put info in dictionary
movie_info = {}
for index, row in enumerate(info_rows): #counting index from 0
    if index == 0:
        movie_info['title'] = row.find('th').get_text() #table head

print(movie_info)

