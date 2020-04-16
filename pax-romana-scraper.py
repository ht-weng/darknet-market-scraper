# Pax Romana Market Scraper

from bs4 import BeautifulSoup
import re

record_count = 10
website_url = 'http://paxromanadfudhte.onion/'

with open('pax.html', 'r') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

listings = soup.select('a.mp-Listing-coverLink')
vendor_info = soup.select('div.mp-Listing--sellerInfo')

for i in range(record_count):
    product = listings[i].select('h3')[0].get_text().strip()
    product_url = listings[i].get('href')
    product_descrip = listings[i].select('p')[1].get_text().strip().replace('\n', '')
    price_in_usd = float(listings[i].select('span.mp-Listing-price')[0].get_text().replace(' USD', ''))
    vendor = vendor_info[i].select('a')[0].get_text().split('(')[0]
    vendor_url = vendor_info[i].select('a')[0].get('href')
    vendor_rating = vendor_info[i].select('a')[0].get_text().split('(')[2].replace(')', '')
    vendor_sales = int(vendor_info[i].select('a')[0].get_text().split('(')[1].replace(')', ''))
    shipping_from = vendor_info[i].select('span')[2].get_text().replace('Ads', '').split('⟶')[0]
    shipping_to = vendor_info[i].select('span')[2].get_text().replace('Ads', '').split('⟶')[1]
    
    sale_text = vendor_info[i].select('span')[3].get_text()
    try:
        views = int(re.search('Views: (.+?)Sold', sale_text).group(1))
        sold = int(sale_text.split('Sold: ')[1])
    except AttributeError:
        views = 'N/A'
        sold = 'N/A'
    
    print('Product: ', product)
    print('Product URL: ', product_url)
    print('Vendor: ', vendor)
    print('Vendor URL: ', vendor_url)
    print('Vendor Rating: ', vendor_rating)
    print('Vendor Sales: ', vendor_sales)
    print('Price in USD: ', price_in_usd)
    print('Product Description: ', product_descrip)
    print('Shipping From: ', shipping_from)
    print('Shipping To: ', shipping_to)
    print('Views: ', views)
    print('Sold: ', sold)
    

