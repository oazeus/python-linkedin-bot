#!/usr/bin/env python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import settings
import time
import json
import sys

from bs4 import BeautifulSoup
import re

class Result:
    code = 1
    msg = "Success"
    data = []

class Company:
    name = ""
    link = ""
    followers = ""
    image = ""
    specialty = ""
    description = ""
  
# keywords = sys.argv[1]
keywords = "corona"
result = Result()
result.code = 1
result.msg = "Success"
data   = []

try: 
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')

    driver = webdriver.Chrome('/Users/zeusaaron14/Downloads/chromedriver', options=options)
    driver.get(settings.linkedin_base_url + settings.linkedin_login_url)

    username = driver.find_element_by_id(settings.linkedin_username_field_id)
    # send_keys() to simulate key strokes
    username.send_keys(settings.linkedin_username)

    password = driver.find_element_by_id(settings.linkedin_password_field_id)
    # send_keys() to simulate key strokes
    password.send_keys(settings.linkedin_password)

    # locate submit button by_class_name
    # log_in_button = driver.find_element_by_class_name(settings.linkedin_signin_button_class)

    # locate submit button by_class_id
    # log_in_button = driver.find_element_by_form('login submit-button')

    # locate submit button by_xpath
    log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

    # .click() to mimic button click
    log_in_button.click()

    page = 0

    # while True:
    page = page + 1
    driver.get(settings.linkedin_base_url + settings.linkedin_company_search_url + "&keywords=" + keywords + "&page=" + str(page))
    actions = ActionChains(driver)

    # WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search__results-list"))) #wait for all listings content

    # SCROLL_PAUSE_TIME = 0.5
    # # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    itemClass = 'search-result__occluded-item'
    elems = driver.find_elements_by_class_name(itemClass)
    a = 0
    if len(elems) > 0:
        for elem in elems:
            a = a + 1
            actions.move_to_element(elem).perform()
            if a == len(elems):
                break

    pageSource = driver.page_source  
    lxml_soup = BeautifulSoup(pageSource, 'lxml')  
    elems = lxml_soup.findAll('li', class_ = itemClass) 

    if len(elems) > 0:
        for elem in elems: 
            name = link = description = image = specialty = followers = ""

            linkEl = elem.find('a', class_ = 'search-result__result-link', href=True)
            if linkEl is not None:
                link = linkEl['href']

            nameEl  = elem.find('h3', class_ = 'search-result__title')
            if nameEl is not None:
                name = nameEl.text
            
            specialtyEl  = elem.find('p', class_ = 'subline-level-1')
            if specialtyEl is not None:
                specialty = specialtyEl.text

            followersEl  = elem.find('p', class_ = 'subline-level-2')
            if followersEl is not None:
                followers = followersEl.text

            descriptionEl = elem.find('p', class_ = 'entity-result__summary')
            if descriptionEl is not None:
                description = descriptionEl.text

            imageEl = elem.find('img', class_ = 'ivm-view-attr__img--centered')
            if imageEl is not None:
                image = imageEl['src']

            row = Company()
            row.name = name 
            row.link = link
            row.image = image 
            row.description = description
            row.image = image
            row.followers = followers
            data.append(row)
        else:
            search = False
            # break
except:
    result.code = 0
    result.msg = "There's an error"
finally:
    driver.quit()
    result.data = [ob.__dict__ for ob in data]
    print(json.dumps(result.__dict__))