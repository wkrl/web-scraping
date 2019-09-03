import re
import requests
from bs4 import BeautifulSoup

response = requests.get('https://en.wikipedia.org/wiki/List_of_animal_names').text
soup = BeautifulSoup(response,'lxml')

my_table = soup.find_all('table',{'class':'wikitable sortable'})[1].tbody
rows = my_table.find_all('tr')[2:]
animals = []

for row in rows:
    try:
        for col in row.find('td'):
            animals.append(re.sub('\(.*\)', '', col.get('title')))
    except:
        continue

with open('animal_names.txt','w+') as f:
    for animal in animals:
        f.write(animal.encode('UTF-8')+'\n')
