# Darknet Market Spider

## Overview

This darknet market spider is designed to download, scrape and analyse a set of darknet markets.

The list of included darknet markets is as follows:

* **Cypher Market**
* ~~**Europa Market**~~ (currently down)
* ~~**Pax-Romana Market**~~ (currently down)
* ~~**Square Market**~~ (currently down)
* **White House Market**
* **Yellow Brick Market**

## Dependencies

[Python 3.7+](https://www.python.org/downloads/)  
[wget](https://www.gnu.org/software/wget/) (comes with most Linux distributions)  
[torify](https://trac.torproject.org/projects/tor/wiki/doc/TorifyHOWTO) (install by `sudo apt install tor`)  
[Tor Browser](https://www.torproject.org/download/)  
[Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)  

### Python Packages

bs4  
CurrencyConverter  
matplotlib  
pandas  

## Getting Started

Fisrt install all the dependencies.

```bash
pip install -r requirements.txt
```

Then use [Tor Browser](https://www.torproject.org/download/) to log in to the markets. Then copy and paste the cookie values with [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/) to `data/[market name]/cookies.txt` (Click the Cookie Quick Manager icon and then click 'Search Cookies for ...' to access the cookies manager page. Copy the cookie value in the 'Details' column). Note that there are two cookie values to copy and paste for each market.  

Now start up the spider.

```bash
python3 main.py [option] [argument]
```

```bash
usage: main.py [-h] [-c {1,2,3,4}] [-s {1,2,3,4}] [-a]

download, Scrape and Analyse a Set of Darknet Markets

optional arguments:
  -h, --help            show this help message and exit
  -d {1,2,3,4}, --download {1,2,3,4}
                        Download the darknet markets. 1-Cypher Market, 2-White
                        House Market, 3-Yellow Brick Market, 4-All markets
  -s {1,2,3,4}, --scrape {1,2,3,4}
                        Scrape the downloaded darknet markets. 1-Cypher Market,
                        2-White House Market, 3-Yellow Brick Market, 4-All
                        markets
  -a, --analyse         Analyse the downloaded darknet markets
```

Examples

1. Download Cypher Market: `python3 main.py -d 1`.  

2. Download all 3 markets: `python3 main.py -d 4`.  

3. Scrape Cypher Market: `python3 main.py -s 1`.  

4. Scrape all 3 markets: `python3 main.py -s 4`.  

5. Analyse the scraped markets and produce some diagrams: `python3 main.py -a`.  

Note that downloading may take a long time as there are hundreds of pages on each market website. Use `Ctrl C` to interrupt the process. Some sample downloaded market webpages are in the `data/[market name]/page-downloads/` folder. Scraping is relatively fast. Use `Ctrl C` to interrupt the process.
