#!/usr/bin/env python3

'''
Cypher Market Page Downloader
'''

from datetime import date
from random import randint
import time
import os
import sys

# environment variables
day = str(date.today())
page_download_directory = 'data/cypher-market/page-downloads/' + day + '/'
cookies_location = 'data/cypher-market/cookies.txt'
process_name = 'tor'
bot_user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'
limit_rate_value = 70
max_redirect_value = 0
number_of_tries = 10


pages = (('23ce97c0-3cfb-11ea-8adb-376b000e7b7e', 45),  # Guides & Tutorials
         ('f4cc5410-3cf8-11ea-88bb-2f78883d918a', 110),  # Drugs
         ('cd7eb0f0-3cfb-11ea-b5b7-ef87c7ec1d5b', 45),  # Software & Malware
         ('53303080-3cfb-11ea-ba5c-abc99e72d48b', 31),  # Counterfeits
         ('7c784f00-3cfb-11ea-a3ba-9d1b2c5645ec', 10),   # Hosting & Security
         ('461b4ba0-3cfb-11ea-9311-277cdf981178', 11))   # Other Listings

# gets market URL from cookie file
def get_market_url(cookies_location):
    with open(cookies_location) as cookies_file:
        market_url = cookies_file.read().split('.')[0]
    return market_url

wget_string = ('torify wget --user-agent="' + bot_user_agent + '" ' +
               '--retry-connrefused ' +
               '--content-on-error ' +
               '--tries=' + str(number_of_tries) + ' ' +
               '--limit-rate ' + str(limit_rate_value) + 'k ' +
               '--max-redirect ' + str(max_redirect_value) + ' ' +
               '--header="Referer: http://' + get_market_url(cookies_location) + '.onion" ' +
               '--load-cookies ' + cookies_location + ' ' + ' ')

# checks if Tor process is active on system, if not it will activate it
def check_tor_process():
    # move processes variable here, otherwise it will initiate the variable
    # when the module is imported, rather than when the function is called.
    # this "could" cause issues
    processes = os.popen('ps -Af').read()
    if process_name not in processes[:]:
        new_process = 'nohup python %s &' % (process_name)
        os.system(new_process)
    return


# checks if directory for resulting files exists. Will auto-make it otherwise
def check_directory(download_directory):
    os.system('mkdir -p ' + download_directory)
    return

# check Tor process and directory
def check_tor_and_directory(download_directory):
    check_tor_process()
    check_directory(download_directory)
    return


def get_index(value, list):
    for i in list:
        if i[0] == value:
            return list.index(i)


def get_value(index, list):
    return list[index][0]


def wget_page(directory, category, page):
    time.sleep(randint(1, 3))

    url = get_market_url(cookies_location)

    os.system(wget_string +
              '"http://' + url + '.onion/category/' + category + '?page=' + page + '" ' +
              '-O "' + directory + 'page' + str(get_index(category, pages)) + '-' + page + '.html"')

    time.sleep(randint(2, 4))

if __name__ == '__main__':

    check_tor_and_directory(page_download_directory)

    for list in pages:  # wget pages
        for page in range(1, list[1]+1):
            wget_page(page_download_directory, str(list[0]), str(page))

    for file in os.listdir(age_download_directory):  # rewget any failed pages
        if os.path.getsize(page_download_directory + file) < 1:
            file_name = os.path.basename(file)[4:-5].split('-')
            wget_page(page_download_directory, get_value(int(file_name[0]), pages), int(file_name[1]))
