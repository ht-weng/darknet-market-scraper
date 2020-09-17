import argparse
import subprocess

parser = argparse.ArgumentParser(description='Download, Scrape and Analyse a Set of Darknet Markets')
parser.add_argument('-d', '--download', type=int, choices=[1, 2, 3, 4], help='Download the darknet markets. 1-Cypher Market, 2-White House Market, 3-Yellow Brick Market, 4-All markets')
parser.add_argument('-s', '--scrape', type=int, choices=[1, 2, 3, 4], help='Scrape the downloaded darknet markets. 1-Cypher Market, 2-White House Market, 3-Yellow Brick Market, 4-All markets')
parser.add_argument('-a', '--analyse', action='store_true', help='Analyse the downloaded darknet markets')
args = parser.parse_args()

if args.download:
    if args.download == 4:
        # download all 3 markets
        subprocess.call(['python3', 'src/cypher-market/page-download.py'])
        subprocess.call(['python3', 'src/white-house-market/page-download.py'])
        subprocess.call(['python3', 'src/yellow-brick/page-download.py'])
    elif args.download == 1:
        # download cypher market
        subprocess.call(['python3', 'src/cypher-market/page-download.py'])
    elif args.crawdownloadl == 2:
        # download white house market
        subprocess.call(['python3', 'src/white-house-market/page-download.py'])
    else:
        # download yellow brick market
        subprocess.call(['python3', 'src/yellow-brick/page-download.py'])
elif args.scrape:
    if args.scrape == 4:
        # scrape all 3 markets download today
        subprocess.call(['python3', 'src/cypher-market/page-scrape.py'])
        subprocess.call(['python3', 'src/white-house-market/page-scrape.py'])
        subprocess.call(['python3', 'src/yellow-brick/page-scrape.py'])
    if args.scrape == 1:
        # scrape cypher markets download today
        subprocess.call(['python3', 'src/cypher-market/page-scrape.py'])
    elif args.scrape == 2:
        # scrape white house markets download today
        subprocess.call(['python3', 'src/white-house-market/page-scrape.py'])
    else:
        # scrape yellow brick markets download today
        subprocess.call(['python3', 'src/yellow-brick/page-scrape.py'])
elif args.analyse:
    subprocess.call(['python3', 'src/analysis/drug-types.py'])
else:
    print('Please supply an argument!')
    