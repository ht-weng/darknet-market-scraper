#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Square Market Page Scraper
'''

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

writer = csv.writer(open('data/square-market/page-scrapes/' + day + '.csv', 'w'))
location = 'data/square-market/page-downloads/' + day + '/'
failed_imports = 0
files = os.listdir(location)
file_count = len(files)
record_count = 10
counter = 0


writer.writerow(['Product', 'Product URL', 'Price in BTC', 'Vendor', 'Vendor URL', 'Vendor Level',
                 'Vendor Positive Rating', 'Vendor Negative Rating', 'Shipping From', 'Date Time Recorded'])

for file in files:
    try:
        counter += 1
        with open(location + file, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')

            try:
                listings = soup.select('div.is-5')
                price_list = soup.select('div.is-3')
            except Exception as exc:
                print(exc)
                continue

            for i in range(record_count):
                try:
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
                    
                    date_time_recorded = (time.ctime(int(os.path.getctime(location + file))))
                    
                    print('Product: ', product)
                    print('Product URL: ', product_url)
                    print('Price in BTC: ', price_in_btc)
                    print('Vendor: ', vendor)
                    print('Vendor URL: ', vendor_url)
                    print('Vendor Level: ',vendor_level)
                    print('Vendor Positive Rating: ', vendor_pos_rating)
                    print('Vendor Negative Rating: ', vendor_neg_rating)
                    print('Shipping From: ', shipping_from)
                    print('Date/Time Recorded: ', date_time_recorded)
                    
                    writer.writerow([product, product_url, price_in_btc, vendor, vendor_url, vendor_level,
                                     vendor_pos_rating, vendor_neg_rating, shipping_from, date_time_recorded])
                except Exception as exc:
                    print(exc)
                    # print(exc.message)
                    # Comment out the below message if you want to print the attributes of error
                    # print(getattr(exc, 'Message : ', str(exc)))
                    failed_imports += 1
                    continue

    except IOError as ioexc:
        print(ioexc)
        # print(ioexc.message)
        # Comment out the below message if you want to print the attributes of error
        # print(getattr(ioexc, 'Message : ', str(ioexc)))
        continue
