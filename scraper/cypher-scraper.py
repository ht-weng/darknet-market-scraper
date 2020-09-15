# Cypher Market Scraper

from bs4 import BeautifulSoup
import re

record_count = 24
website_url = 'http://xtzqxvmi6p7hul6i.onion/'

with open('../data/cypher.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

listings = soup.select('div.card-body')

for i in range(record_count):
    product = listings[i].select('a')[0].get_text().strip()
    product_url = listings[i].select('a')[0].get('href')
    vendor = listings[i].select('a')[1].get_text().strip()
    vendor_url = listings[i].select('a')[1].get('href')
    quantity = float(listings[i].select('span')[1].get_text().replace('Stock:', ''))

    price_cat_text = listings[i].select('p.card-subtitle')[0].get_text()
    try: 
        price_in_usd = float(re.search('From: (.+?) -', price_cat_text).group(1).replace(' $', ''))
        category = re.search('- (.+?) -', price_cat_text).group(1)
    except AttributeError:
        price_in_usd = 'N/A'
        category = 'N/A'
    
    print('Product: ', product)
    print('Product URL: ', product_url)
    print('Price in USD: ', price_in_usd)
    print('Vendor: ', vendor)
    print('Vendor URL: ', vendor_url)
    print('Category: ', category)
    print('quantity: ', quantity)
