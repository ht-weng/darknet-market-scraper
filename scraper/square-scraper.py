# Square Market Scraper

from bs4 import BeautifulSoup
import re

record_count = 10
website_url = 'http://c77yo2fe3f4e3g7tll5qrzzoneymihws2tpjceg6wop2ky6pkcaqczyd.onion'

with open('../data/square2.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

listings = soup.select('div.is-5')
price_list = soup.select('div.is-3')

for i in range(record_count):
    product = listings[i].select('a')[0].get_text().strip()
    product_url = listings[i].select('a')[0].get('href')
    price_in_btc = float(price_list[0].select('p')[0].get_text().strip().replace(' BTC', ''))
    vendor = listings[i].select('a')[1].get_text().strip()
    vendor_url = listings[i].select('a')[1].get('href')
    vendor_level = listings[i].select('span')[2].get_text()
    vendor_pos_rating = int(listings[i].select('span')[0].get_text().replace('+', ''))
    vendor_neg_rating = int(listings[i].select('span')[1].get_text())
    
    shipping_text = listings[i].select('p')[1].get_text()
    try:
        shipping_from = re.search('Ships from (.+?)\n', shipping_text).group(1)
    except AttributeError:
        shipping_from = 'N/A'
    
    print('Product: ', product)
    print('Product URL: ', product_url)
    print('Price in BTC: ', price_in_btc)
    print('Vendor: ', vendor)
    print('Vendor URL: ', vendor_url)
    print('Vendor Level: ',vendor_level)
    print('Vendor Positive Rating: ', vendor_pos_rating)
    print('Vendor Negative Rating: ', vendor_neg_rating)
    print('Shipping From: ', shipping_from)
