#!/usr/bin/env python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from urllib.parse import parse_qs
import urllib.parse as urlparse
from selenium import webdriver
import pandas as pd
import argparse
import settings
import time
import json
import sys
  

parser = argparse.ArgumentParser()
parser.add_argument('--keywords', nargs='?', type=str, help='keywords to search')
parser.add_argument('--max', nargs='+', type=int, default=[1000], help='max result to search')

args = parser.parse_args()
keywords = args.keywords
max_result = args.max[0]

base_url = settings.fb_base_url
search_url = "/public/"

if (max_result > 0):
    max_result = max_result
else: 
    max_result = 1000000

if keywords is None:
    keywords = "nike"

class Result:
    code = 1
    msg = "Success"
    ended = False
    data = []

class Account:
    id  = ""
    name = ""
    link = ""
    image = ""
    position = ""
    address = ""
    type = "account"

result = Result()
result.code = 1
result.ended = False
result.msg = "Success"
result.data = []
i = 0

class Facebook:
    @staticmethod
    def init_driver():
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--incognito')
        options.add_argument('--log-level=3')
        return webdriver.Chrome(settings.chrome_driver, options=options)

    @staticmethod
    def get_post_url(story_fbid, id):
        return settings.fb_base_url + "/story.php?story_fbid=" + story_fbid + "&id=" + id

    @staticmethod
    def value_from_url(url:str, key:str):
        v = ['']
        try:
            parsed = urlparse.urlparse(url)
            v = parse_qs(parsed.query)[key]
            if v is None:
                v = ['']
        finally:
            return  v[0]

    @staticmethod
    def scrap(driver, url:str, max_result:int, item:int):
        try:
            if item >= max_result:
                return item
                
            driver.get(url)
            time.sleep(0.5)
            resultContainer = driver.find_elements_by_css_selector('#BrowseResultsContainer')
            if(len(resultContainer) == 0):  
                result.ended = True
                return

            elems = resultContainer[0].find_elements_by_css_selector('div table')
                
            if len(elems) > 0:
                for elem in elems: 
                    id = name = link = image = ""

                    try:
                        nameEl = elem.find_element_by_css_selector('tr td:nth-child(2) a div div')
                        name = nameEl.text
                    except:
                        name = name
                    # print("[NAME]: ", name)

                    try:
                        imageEl = elem.find_element_by_css_selector('tr td:nth-child(1) a img')
                        image = imageEl.get_attribute("src")
                        if not name:
                            try:
                                name = imageEl.get_attribute("alt").replace(", profile picture")
                            except:
                                name = name
                    except:
                        image = ""
                    # print("[IMAGE]: ", image)

                    try:
                        linkEl = elem.find_element_by_css_selector('tr td:nth-child(1) a')
                        link = linkEl.get_attribute("href")
                    except:
                        link = ""
                    # print("[LINK]: ", link)

                    try:
                        if link:
                            if link.count("profile.php?"):
                                id = Facebook.value_from_url(link, 'id')
                                if id:
                                    image = "https://graph.facebook.com/" + id + "/picture?type=small" 

                            if not id:
                                tempkoText = link.split("?")
                                if tempkoText[0] :
                                    id = tempkoText[0].replace((base_url + "/"), "")
                    except:
                        id = ""


                    if id:
                        link = base_url + "/" + id
                        link = link.replace("//mbasic.", "//")
                        row = Account()
                        row.id = id
                        row.name = name
                        row.link = link
                        row.image = image
                        row.type = "account"
                        result.data.append(row)
                        item = item + 1

                    if item >= max_result:
                        break

                try:
                    if item >= max_result:
                        max_result = max_result
                    else:
                        pagerEl = driver.find_elements_by_css_selector("#see_more_pager a")
                        if len(pagerEl) > 0:
                            url = pagerEl[0].get_attribute("href")
                            Facebook.scrap(driver, url, max_result, item)
                except Exception as ex:
                    result.msg = str(ex)
            else:
                result.ended = True
        except Exception as ex:
            result.code = "0"
            result.msg = str(ex)

        return item

if __name__ == '__main__':
    chome_driver = Facebook.init_driver()
    try:        
        keywords = keywords.split("+")
        if len(keywords) > 0:
            for keyword in keywords:
                date_to_search = str((datetime.today() - timedelta(days=1)).strftime('%B %d, %Y'))
                date_to_search = ""
                keyword = keyword + " " + date_to_search
                url = base_url + search_url + keyword.strip()
                i = Facebook.scrap(chome_driver, url, max_result, i)
    except Exception as ex:
        result.code = "0"
        result.msg  = str(ex)
    finally:
        # chome_driver.quit()
        result.data = [ob.__dict__ for ob in result.data]
        print(json.dumps(result.__dict__))

