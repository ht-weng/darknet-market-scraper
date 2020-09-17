#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
White House Market Page Scraper
'''

from bs4 import BeautifulSoup
import csv
import os
import sys
import time
from datetime import date, timedelta
import re

page_download_location = 'data/white-house-market/page-downloads/'
page_scrape_location = 'data/white-house-market/page-scrapes/'
record_count = 40


if __name__ == '__main__':
    scrape_list = []
    for file in os.listdir(page_scrape_location):
        scrape_list.append(str(file).strip('.csv'))
    
    for directory in os.listdir(page_download_location):
        day = str(directory)
        if not day in scrape_list:
            
            writer = csv.writer(open('data/white-house-market/page-scrapes/' + day + '.csv', 'w'))
            location = 'data/white-house-market/page-downloads/' + day + '/'
            files = os.listdir(location)
            failed_imports = 0
            counter = 0
            
            writer.writerow(['Product', 'Product URL', 'Category', 'Vendor', 'Vendor URL',
                            'Price in AUD', 'Shipping From', 'Shipping To', 'Date Time Recorded'])

            for file in files:
                try:
                    counter += 1
                    with open(location + file, 'r') as html_file:
                        soup = BeautifulSoup(html_file, 'lxml')

                        try:
                            vendor_list = soup.select('div.col-md-3')
                            price_list = soup.select('div.col-md-2')
                            title_list = soup.select('div.col-md-4')
                        except Exception as exc:
                            print(exc)
                            continue

                        for i in range(record_count):
                            try:
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
                                
                                date_time_recorded = (time.ctime(int(os.path.getctime(location + file))))
                                
                                print('Product: ', product)
                                print('Product URL: ', product_url)
                                print('Category: ', category)
                                print('Vendor: ', vendor)
                                print('Vendor URL: ', vendor_url)
                                print('Price in AUD: ', price_in_aud)
                                print('Shipping From: ', shipping_from)
                                print('Shipping To: ', shipping_to)
                                print('Date Time Recorded: ', date_time_recorded)
                                
                                writer.writerow([product, product_url, category, vendor, vendor_url, price_in_aud,
                                                shipping_from, shipping_to, date_time_recorded])
                            except Exception as exc:
                                print(exc)
                                failed_imports += 1
                                continue

                except IOError as ioexc:
                    print(ioexc)
                    continue
            print("Total failed: ", failed_imports)
            
    print('All crawled webpages have been scraped!')