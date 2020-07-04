from twitter_scraper import get_tweets
import datetime
import argparse
import json

default_pages = 10
parser = argparse.ArgumentParser()
parser.add_argument('--keywords', nargs='?', type=str, help='keywords to search')
parser.add_argument('--pages', nargs='+', type=int, default=[default_pages], help='number of pages')

args = parser.parse_args()
keywords = args.keywords
pages = args.pages[0]

if pages > 0:
    pages = pages
else:
    pages = default_pages

code = 1
msg = "Success"
data = []

try:
    for tweet in get_tweets(keywords, pages):
        tweet['time'] = tweet['time'].strftime('%Y-%m-%d %H:%M:%S')
        data.append(tweet)
except Exception as ex:
    code = 0
    msg = str(ex)
finally:
    print(json.dumps({
        "code" : code,
        "msg" : msg,
        "data": data
    }))