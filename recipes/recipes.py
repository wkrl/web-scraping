import requests
from bs4 import BeautifulSoup
import json

dict = {
	'type': {
		'breakfast': {
			'request_link': 'https://www.allrecipes.com/recipes/78/breakfast-and-brunch/',
			'items': [] 
		},
		'dessert': {
			'request_link': 'https://www.allrecipes.com/recipes/79/desserts/',
			'items': []
		},
		'dinner': {
			'request_link': 'https://www.allrecipes.com/recipes/17562/dinner/',
			'items': []
		},
		'lunch': {
			'request_link': 'https://www.allrecipes.com/recipes/17561/lunch/',
			'items': []
		}
	}
}

def get_recipes(number_of_pages):
	for meal_type in dict['type']: 
		request_link =  dict['type'][meal_type]['request_link']
		for i in range(number_of_pages):
			response = requests.get(request_link).text + '?page=' + str(i)
			soup = BeautifulSoup(response,'lxml')
			recipes = soup.find_all('div',{'class':'grid-card-image-container'})
			for item in recipes:
				try:
					# title and url
					title_not_clean = item.a.img["alt"].split(' -')[0]
					title = title_not_clean.replace('and Video', '').replace('Recipe', '')
					url = item.a['href']
					# new request of specific recipe for more information 
					response = requests.get(url).text 
					soup = BeautifulSoup(response, 'lxml')
					# rating
					rating = soup.find('div',{'class','rating-stars'})['data-ratingstars'];
					# image, does not include videos
					img = soup.find('img',{'class','rec-photo'})['src']
					# instructions
					steps = [step.get_text().rstrip() for step in soup.find_all('span',{'class','recipe-directions__list--item'})]
					#ingredients 
					ingredients = [item.get_text().rstrip() for item in soup.find_all('span', {'class','recipe-ingred_txt'})[:-3]]
					print 'Adding: ' + title
					dict['type'][meal_type]['items'] = dict['type'][meal_type]['items'] + [{'title': title, 'url': url, 'rating': round(float(rating),2), 'img_url': img, 'steps': steps, 'ingredients': ingredients}]
				except: 
					continue

get_recipes(10)
result = json.dumps(dict)
with open ('output.json','wb+') as file: 
	file.write(result)
