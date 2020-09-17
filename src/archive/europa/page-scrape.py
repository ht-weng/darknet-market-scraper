#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
europa Market Page Scraper
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

writer = csv.writer(open('data/europa/page-scrapes/' + day + '.csv', 'w'))
location = 'data/europa/page-downloads/' + day + '/'
failed_imports = 0
files = os.listdir(location)
record_count = 24
website = 'http://europamk24ai3hjz.onion'

writer.writerow(['Product', 'Product URL', 'Vendor', 'Vendor URL',
                 'Price in EUR', 'Product Description', 'Date Time Recorded'])

for file in files:
    try:
        with open(location + file, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')

            listings = soup.select('div.content')

            for i in range(record_count):
                try:
                    product = listings[4*i].select('a')[0].get_text().strip()
                    product_url = website + listings[4*i].select('a')[0].get('href')
                    vendor = listings[4*i+1].select('a')[0].get_text().replace('@', '')
                    vendor_url = website + listings[4*i+1].select('a')[0].get('href')
                    product_descrip = listings[4*i+2].select('div.description')[0].get_text().strip().replace('\n', '')

                    price_text = listings[4*i+3].select('span')[0].get_text().strip().replace('\t', '').replace('\n', '')
                    if '-' in price_text:
                        price_in_eur = float(price_text.split('-')[0].strip())
                    else:
                        price_in_eur = float(price_text.replace('EUR', ''))
                    date_time_recorded = time.ctime(int(os.path.getctime(location + file)))


                    print('Processing record ' + str(i + 1) + '/' + str(record_count))
                    print('Product: ', product)
                    print('Product URL: ', product_url)
                    print('Vendor: ', vendor)
                    print('Vendor URL: ', vendor_url)
                    print('Price in EUR: ', price_in_eur)
                    print('Product Description: ', product_descrip)
                    print('Date/Time Recorded: ' + date_time_recorded)

                    writer.writerow([product, product_url, vendor, vendor_url,
                                     price_in_eur, product_descrip, date_time_recorded])

                except Exception as exc:
                    failed_imports += 1
                    print("Error on file: " + file)
                    print(exc)
                    continue
    except IOError as ioexc:
        print(ioexc)
        continue

print("Total failed: ", failed_imports)
