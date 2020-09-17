#!/usr/bin/env python3

'''
Yellow Brick Page Downloader
'''

from datetime import date
from random import randint
import time
import os
import sys


# environment variables
day = str(date.today())
page_download_directory = 'data/yellow-brick/page-downloads/' + day + '/'
cookies_location = 'data/yellow-brick/cookies.txt'
process_name = 'tor'
bot_user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'
limit_rate_value = 70
max_redirect_value = 0
number_of_tries = 10

page_start = 0
page_end = 721


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


def wget_page(directory, page):
    time.sleep(randint(1, 3))

    url = get_market_url(cookies_location)

    os.system(wget_string +
              '"http://' + url + '.onion/?yellowbrick=&reqpage=' + page + '" ' +
              '-O "' + directory + 'page' + page + '.html"')

    time.sleep(randint(2, 4))

if __name__ == '__main__':

    check_tor_and_directory(page_download_directory)

    for page in range(page_start, page_end):
        wget_page(page_download_directory, str(page))

    # FIXME this is broken
    for file in os.listdir(age_download_directory):  # rewget any failed pages
        if os.path.getsize(page_download_directory + file) < 170:
            wget_page(page_download_directory, file[4:-5])
