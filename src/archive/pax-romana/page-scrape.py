#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pax Romana Market Page Scraper
"""

# NOTE untested

from bs4 import BeautifulSoup
import csv
import os
import sys
import time
from datetime import date, timedelta
import re

if len(sys.argv) > 1:
    day = sys.argv[1]
else:
    day = str(date.today() - timedelta(days=0))

writer = csv.writer(open('data/pax-romana/page-scrapes/' + day + '.csv', 'w'))
location = 'data/pax-romana/page-downloads/' + day + '/'
failed_imports = 0
files = os.listdir(location)
record_count = 10
website = 'http://paxromanadfudhte.onion'

writer.writerow(['Product', 'Product URL', 'Vendor', 'Vendor URL', 'Vendor Rating',
                 'Vendor Sales', 'Price in AUD', 'Unit', 'Product Description',
                 'Shipping From', 'Shipping To', 'Views', 'Sold', 'Date Time Recorded'])

for file in files:
    try:
        with open(location + file, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')

            listings = soup.select('a.mp-Listing-coverLink')
            vendor_info = soup.select('div.mp-Listing--sellerInfo')

            for i in range(record_count):
                try:
                    product = listings[i].select('h3')[0].get_text().strip()
                    product_url = listings[i].get('href')
                    product_descrip = listings[i].select('p')[1].get_text().strip().replace('\n', '')
                    vendor = vendor_info[i].select('a')[0].get_text().split('(')[0]
                    vendor_url = website + vendor_info[i].select('a')[0].get('href')
                    vendor_rating = vendor_info[i].select('a')[0].get_text().split('(')[2].replace(')', '')
                    vendor_sales = int(vendor_info[i].select('a')[0].get_text().split('(')[1].replace(')', ''))
                    shipping_from = vendor_info[i].select('span')[2].get_text().replace('Ads', '').split('⟶')[0]
                    shipping_to = vendor_info[i].select('span')[2].get_text().replace('Ads', '').split('⟶')[1]

                    price_text = listings[i].select('span.mp-Listing-price')[0].get_text()
                    if 'for' in price_text:
                        unit = price_text.split('for')[0].strip()
                        price_in_aud = float(price_text.split('for')[1].strip().replace(' AUD', ''))
                    else:
                        unit = 'N/A'
                        price_in_aud = float(price_text.replace(' AUD', ''))

                    sale_text = vendor_info[i].select('span')[3].get_text()
                    try:
                        views = int(re.search('Views: (.+?)Sold', sale_text).group(1))
                        sold = int(sale_text.split('Sold: ')[1])
                    except AttributeError:
                        views = 'N/A'
                        sold = 'N/A'
                    date_time_recorded = time.ctime(int(os.path.getctime(location + file)))

                    print('Processing record ' + str(i + 1) + '/' + str(record_count))
                    print('Product: ', product)
                    print('Product URL: ', product_url)
                    print('Vendor: ', vendor)
                    print('Vendor URL: ', vendor_url)
                    print('Vendor Rating: ', vendor_rating)
                    print('Vendor Sales: ', vendor_sales)
                    print('Price in AUD: ', price_in_aud)
                    print('Unit: ', unit)
                    print('Product Description: ', product_descrip)
                    print('Shipping From: ', shipping_from)
                    print('Shipping To: ', shipping_to)
                    print('Views: ', views)
                    print('Sold: ', sold)
                    print('Date/Time Recorded: ' + date_time_recorded)

                    writer.writerow([product, product_url, vendor, vendor_url, vendor_rating,
                                     vendor_sales, price_in_aud, unit, product_descrip,
                                     shipping_from, shipping_to, views, sold, date_time_recorded])

                except Exception as exc:
                    failed_imports += 1
                    print("Error on file: " + file)
                    print(exc)
                    continue
    except IOError as ioexc:
        print(ioexc)
        continue

print("Total failed: ", failed_imports)
