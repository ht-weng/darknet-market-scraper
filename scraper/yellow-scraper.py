# Yellow Brick Market Scraper

from bs4 import BeautifulSoup
import re

record_count = 11
website_url = 'http://ck73ugjvx5a4wkhsmrfvwhlrq7evceovbsb7tvaxilpahybdokbyqcqd.onion/'

with open('../data/yellow2.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

listings = soup.select('div#listing')

for i in range(record_count):
    product = listings[i].select('a')[1].get_text().strip()
    product_url = website_url + listings[i].select('a')[1].get('href')
    price_text = listings[i].select('b')[0].get_text().replace('$', '')
    if price_text != 'Highly Sold':
        price_in_usd = float(price_text)
        vendor = listings[i].select('span')[0].select('a')[0].get_text()
        vendor_url = website_url + listings[i].select('span')[0].select('a')[0].get('href')
    else:
        price_in_usd = float(listings[i].select('b')[1].get_text().replace('$', ''))
        vendor = listings[i].select('span')[1].select('a')[0].get_text()
        vendor_url = website_url + listings[i].select('span')[1].select('a')[0].get('href')
    
    category = listings[i].select('a')[3].get_text()
    shipping_from = listings[i].select('span')[2].get_text()
    
    print('Product: ', product)
    print('Product URL: ', product_url)
    print('Price in USD: ', price_in_usd)
    print('Category: ', category)
    print('Vendor: ', vendor)
    print('Vendor URL: ', vendor_url)
    print('Shipping From: ', shipping_from)
