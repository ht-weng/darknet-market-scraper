#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Yellow Brick Page Scraper
'''

from bs4 import BeautifulSoup
import csv
import os
import sys
import time
import re
from datetime import date, timedelta, datetime
from currency_converter import CurrencyConverter

page_download_location = 'data/yellow-brick/page-downloads/'
page_scrape_location = 'data/yellow-brick/page-scrapes/'
cookies_location = 'data/yellow-brick/cookies.txt'

c = CurrencyConverter()

record_count = 11

# gets market URL from cookie file
def get_market_url(cookies_location):
    with open(cookies_location) as cookies_file:
        market_url = cookies_file.read().split('.')[0]
    return market_url

website_url = 'http://' + get_market_url(cookies_location) + '.onion/'

if __name__ == '__main__':
    scrape_list = []
    for file in os.listdir(page_scrape_location):
        scrape_list.append(str(file).strip('.csv'))
    
    for directory in os.listdir(page_download_location):
        day = str(directory)
        if not day in scrape_list:
            
            day_datetime = datetime.strptime(day, '%Y-%m-%d')
            if day_datetime < datetime(2020, 6, 9):
                converter_datetime = day_datetime
            else:
                converter_datetime = datetime(2020, 6, 9)

            writer = csv.writer(open('data/yellow-brick/page-scrapes/' + day + '.csv', 'w'))
            location = 'data/yellow-brick/page-downloads/' + day + '/'
            failed_imports = 0
            files = os.listdir(location)
            file_count = len(files)
            counter = 0

            writer.writerow(['Product', 'Vendor', 'Price in AUD',
                            'Vendor Level', 'Category', 'Shipping From', 'Product URL'
                            'Vendor URL', 'Date Time Recorded'])

            for file in files:
                try:
                    with open(location + file, 'r') as html_file:
                        soup = BeautifulSoup(html_file, 'lxml')
                        try:
                            listings = soup.select('div#listing')
                        except Exception as e:
                            print(e)
                            failed_imports += 1

                        for i in range(record_count):
                            try:
                                product = listings[i].select('a')[1].get_text().strip()
                                category = listings[i].select('a')[3].get_text().strip()

                                product_url = website_url + listings[i].select('a')[1].get('href')
                                price_text = listings[i].select('b')[0].get_text().replace('$', '')
                                if price_text != 'Highly Sold' and price_text != 'Legit':
                                    price_in_usd = float(price_text)
                                else:
                                    price_in_usd = float(listings[i].select('b')[1].get_text().replace('$', ''))
                                price_in_aud = round(c.convert(price_in_usd, 'USD', 'AUD', date=converter_datetime), 2)
                                vendor = listings[i].select('span#ah_name')[0].select('a')[0].get_text()
                                vendor_url = website_url + listings[i].select('span#ah_name')[0].select('a')[0].get('href')
                                vendor_level_text = listings[i].select('span#ah_level')
                                if len(vendor_level_text) == 0:
                                    vendor_level = listings[i].select('span#tag_level')[0]['title']
                                else:
                                    vendor_level = vendor_level_text[0]['title']
                                shipping_from = listings[i].select('span#ah_ships')[0].get_text()

                                date_time_recorded = (time.ctime(int(os.path.getctime(location + file))))

                                print('Processing record ' + str(i+1) + '/' +
                                    str(record_count) + ' of ' + str(file) + ' [' +
                                    str(counter) + '/' + str(file_count) + ']')
                                print('Product: ' + product)
                                print('Vendor: ' + vendor)
                                print('Price in AUD: ' + str(price_in_aud))
                                print('Vendor Level: ' + vendor_level)
                                print('Category: ' + category)
                                print('Shipping From: ' + shipping_from)
                                print('Product URL: ' + product_url)
                                print('Vendor URL: ' + vendor_url)
                                print('Failed: ' + str(failed_imports))
                                print('Date/Time Recorded: ' + date_time_recorded)

                                writer.writerow([product, vendor, price_in_aud, vendor_level, category,
                                                shipping_from, product_url, vendor_url, date_time_recorded])
                            except Exception as exc:
                                print(exc)
                                failed_imports += 1

                except IOError as ioexc:
                    print(ioexc)

            print("Total failed: ", failed_imports)

    print('All crawled webpages have been scraped!')