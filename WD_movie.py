#scraping information from website (List of Disney Movies) store it in python dictionary
#first try (Alice in the Wonderland)

import requests
from bs4 import BeautifulSoup as bs

r = requests.get('https://en.wikipedia.org/wiki/Alice_in_Wonderland_(2010_film)')

soup = bs(r.content, "lxml") #html parser
#print the HTML
contents = soup.prettify() #content in the website
#turn a soup into a nicely formatted Unicode string, with a separate line for each tag and each string

info_box = soup.find(class_="infobox vevent") 
#info in the box(of movie)
info_rows = info_box.find_all("tr") #table row
##for row in info_rows:
##  print(row.prettify())

#put info in dictionary
movie_info = {}

def get_content_value(row_data): #some have more little list inside(li or list item)
    #name of producers (more than 1)
    if row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
        #specify string anf strip whitespace   
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0", " ")
        # =row.find("td").get_text()

for index, row in enumerate(info_rows): #counting index from 0
    if index == 0:
        movie_info['title'] = row.find('th').get_text(" ", strip=True) #table head
    
    elif index == 1:
        continue #picture of movie
    else:
        content_key = row.find("th").get_text(" ", strip=True) #left box(directed by)
        #content_value = row.find("td").get_text() #right side(name)(table data)
        content_value = get_content_value(row.find("td"))
        movie_info[content_key] = content_value

print(movie_info)

