from bs4 import BeautifulSoup
import requests
import json
import timeit

base_url = 'https://newyork.craigslist.org/search/apa?s='
ads = []
page_numer = 2880
start_time = timeit.default_timer()

for i in range(page_numer): 
    print(str(i) + '/' + str(page_numer))
    try: 
        response = requests.get(base_url+str(i)).text
        soup = BeautifulSoup(response,'lxml')
        apartment_ads = soup.findAll('li', {'class': 'result-row'})   
        for ad in apartment_ads: 
            try:
                ad_id = ad.get('data-pid')
                ad_url = ad.findChild('a').get('href')
                ad_title = ad.findChild('p').findChild('a').text  
                ad_price = ad.findChild('a').findChild('span').text
                ad_meta = {
                    'ad_date': ad.findChild('p').findChild('time').get('datetime'),
                    'ad_br_size': ad.findChild('p').find('span', {'class': 'result-meta'}).find('span', {'class': 'housing'}).text,
                    'ad_location': ad.findChild('p').find('span', {'class': 'result-meta'}).find('span', {'class': 'result-hood'}).text
                }           
                ads += [{'id': ad_id, 'url': ad_url, 'title': ad_title, 'price': ad_price,'meta': ad_meta}]            
            except:
                continue
    except: 
        continue

with open('data.json', 'w') as outfile:
    json.dump(ads, outfile)

stop = timeit.default_timer()
print('Wrote file with ' + str(len(ads)) + ' ads.')
print('Time it took: ', stop - start)




