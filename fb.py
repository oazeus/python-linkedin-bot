from facebook_scraper import get_posts
import datetime
import argparse
import json

default_pages = 20
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

print(pages)

code = 1
msg = "Success"
data = []

try:
    for post in get_posts(keywords, pages=pages):
        if post['post_id'] is None:
            post['post_id'] = ''

        if post['video'] is None:
            post['video'] = ''

        if post['link'] is None:
            post['link'] = ''

        if post['likes'] is None:
            post['likes'] = 0

        if post['comments'] is None:
            post['comments'] = 0

        if post['shares'] is None:
            post['shares'] = 0

        if post['post_url'] is None:
            post['post_url'] = ''

        if post['image'] is None:
            post['image'] = ''

        if post['image'] is None:
            post['image'] = ''


        post['time'] = post['time'].strftime('%Y-%m-%d %H:%M:%S')
        data.append(post)
except Exception as ex:
    code = 0
    msg = str(ex)
finally:
    print(json.dumps({
        "code" : code,
        "msg" : msg,
        "data": data
    }))