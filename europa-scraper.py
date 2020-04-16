# Europa Market Scraper

from bs4 import BeautifulSoup
import re

record_count = 24
website_url = 'http://europamk24ai3hjz.onion/'

with open('europa.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

listings = soup.select('div.content')

for i in range(record_count):
    product = listings[4*i].select('a')[0].get_text().strip()
    product_url = listings[4*i].select('a')[0].get('href')
    vendor = listings[4*i+1].select('a')[0].get_text().replace('@', '')
    vendor_url = listings[4*i+1].select('a')[0].get('href')
    product_descrip = listings[4*i+2].select('div.description')[0].get_text().strip().replace('\n', '')

    price_text = listings[4*i+3].select('span')[0].get_text().strip().replace('\t', '').replace('\n', '')
    if '-' in price_text:
        price_in_eur = float(price_text.split('-')[0].strip())
    else:
        price_in_eur = float(price_text.replace('EUR', ''))
    
    print('Product: ', product)
    print('Product URL: ', product_url)
    print('Vendor: ', vendor)
    print('Vendor URL: ', vendor_url)
    print('Price in EUR: ', price_in_eur)
    print('Product Description: ', product_descrip)

