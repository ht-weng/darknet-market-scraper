# White House Market Scraper

from bs4 import BeautifulSoup
import re

record_count = 40
website_url = 'http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion'

with open('../data/whitehouse.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

vendor_list = soup.select('div.col-md-3')
price_list = soup.select('div.col-md-2')
title_list = soup.select('div.col-md-4')

for i in range(record_count):
    product = title_list[i+1].select('a')[0].get_text().strip()
    product_url = title_list[i+1].select('a')[0].get('href')
    category = price_list[2*i+7].select('a')[0].get_text().strip()
    vendor = vendor_list[i+4].select('a')[0].get_text()
    vendor_url = vendor_list[i+4].select('a')[0].get('href')
    shipping_from = price_list[2*i+8].select('p')[2].get_text().replace('Ships from: ', '')
    shipping_to = price_list[2*i+8].select('p')[3].get_text().replace('Ships to: ', '')
    
    price_text = soup.select('div.col-md-2')[2*i+8].select('p')[1].get_text()
    try:
        price_in_aud = float(re.search('AUD\xa0(.+?) CAD', price_text).group(1))
    except AttributeError:
        price_in_aud = 'N/A'
    
    print('Product: ', product)
    print('Product URL: ', product_url)
    print('Category: ', category)
    print('Vendor: ', vendor)
    print('Vendor URL: ', vendor_url)
    print('Shipping From: ', shipping_from)
    print('Shipping To: ', shipping_to)
    print('Price in AUD: ', price_in_aud)