#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cypher Market Page Scraper
"""

# NOTE untested

from bs4 import BeautifulSoup
import csv
import os
import sys
import time
from datetime import date, timedelta
import re

page_download_location = 'data/cypher-market/page-downloads/'
page_scrape_location = 'data/cypher-market/page-scrapes/'
record_count = 24

if __name__ == '__main__':
    scrape_list = []
    for file in os.listdir(page_scrape_location):
        scrape_list.append(str(file).strip('.csv'))
    
    for directory in os.listdir(page_download_location):
        day = str(directory)
        if not day in scrape_list:
            
            writer = csv.writer(open('data/cypher-market/page-scrapes/' + day + '.csv', 'w'))
            location = 'data/cypher-market/page-downloads/' + day + '/'
            failed_imports = 0
            files = os.listdir(location)

            writer.writerow(['Product', 'Product URL', 'Vendor', 'Vendor URL',
                            'Price in AUD', 'Category', 'Quantity', 'Date Time Recorded'])

            for file in files:
                try:
                    with open(location + file, 'r') as html_file:
                        soup = BeautifulSoup(html_file, 'lxml')

                        listings = soup.select('div.card-body')
                        
                        for i in range(record_count):
                            try:
                                product = listings[i].select('a')[0].get_text().strip()
                                product_url = listings[i].select('a')[0].get('href')
                                vendor = listings[i].select('a')[1].get_text().strip()
                                vendor_url = listings[i].select('a')[1].get('href')
                                quantity = float(listings[i].select('span')[1].get_text().replace('Stock:', ''))

                                price_cat_text = listings[i].select('p.card-subtitle')[0].get_text()
                                try:
                                    price_in_aud = float(re.search('From: (.+?) -', price_cat_text).group(1).split(" ")[0])
                                    category = re.search('- (.+?) -', price_cat_text).group(1)
                                except AttributeError:
                                    price_in_aud = 'N/A'
                                    category = 'N/A'
                                date_time_recorded = time.ctime(int(os.path.getctime(location + file)))

                                print('Processing record ' + str(i + 1) + '/' + str(record_count))
                                print('Product: ', product)
                                print('Product URL: ', product_url)
                                print('Price in AUD: ', price_in_aud)
                                print('Vendor: ', vendor)
                                print('Vendor URL: ', vendor_url)
                                print('Category: ', category)
                                print('quantity: ', quantity)
                                print('Date/Time Recorded: ' + date_time_recorded)

                                writer.writerow([product, product_url, vendor, vendor_url,
                                                price_in_aud, category, quantity,
                                                date_time_recorded])

                            except Exception as exc:
                                failed_imports += 1
                                print("Error on file: " + file)
                                print(exc)
                                continue
                except IOError as ioexc:
                    print(ioexc)
                    continue

            print("Total failed: ", failed_imports)

    print('All crawled webpages have been scraped!')