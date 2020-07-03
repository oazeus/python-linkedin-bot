#!/usr/bin/env python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import argparse
import pandas as pd
import settings
import time
import json
import sys
  

parser = argparse.ArgumentParser()
parser.add_argument('--keywords', nargs='?', type=str, help='keywords to search')
parser.add_argument('--page', nargs='+', type=int, default=[1], help='page number')

args = parser.parse_args()
keywords = args.keywords
page = args.page[0]

if (page > 0):
    page = page
else: 
    page = 1

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
driver = webdriver.Chrome(settings.chrome_driver, options=options)

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
    type = "company"

result = Result()
result.code = 1
result.msg = "Success"
data = []

# try: 
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
# page = page + 1
driver.get(settings.linkedin_base_url + settings.linkedin_company_search_url + "&keywords=" + keywords + "&page=" + str(page))
# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result__occluded-item"))) #wait for all listings content
# elems = driver.find_elements_by_class_name('entity-result__item')
elems = driver.find_elements_by_css_selector('li.search-result__occluded-item')
if len(elems) > 0:
    for elem in elems: 
        # action.move_to_element(elem).perform()
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        name = link = description = image = specialty = followers = ""
        # nameElCont = elem.find_elements_by_class_name('entity-result__title-text')
        # nameElCont = elem.find_elements_by_class_name('search-result__info')
        linkCont = elem.find_elements_by_css_selector('a.search-result__result-link')
        if(len(linkCont) > 0):
            link  = linkCont[0].get_attribute("href")

        nameCont = elem.find_elements_by_css_selector('a.search-result__result-link > h3')
        if(len(nameCont) > 0):
            name = nameCont[0].text

        # specialtyCont = elem.find_elements_by_class_name('entity-result__primary-subtitle')
        specialtyCont = elem.find_elements_by_class_name('subline-level-1')
        if(len(specialtyCont) > 0):
            specialty = specialtyCont[0].text
        
        # followCont = elem.find_elements_by_class_name('entity-result__secondary-subtitle')
        followCont = elem.find_elements_by_class_name('subline-level-2')
        if(len(followCont) > 0):
            followers = followCont[0].text
        
        descCont = elem.find_elements_by_class_name('entity-result__summary')
        if(len(descCont) > 0):
            description = descCont[0].text

        imageCont = elem.find_elements_by_class_name('ivm-view-attr__img--centered');
        if(len(imageCont) > 0):
            image = imageCont[0].get_attribute("src")


        row = Company()
        row.name = name 
        row.link = link
        row.image = image 
        row.description = description
        row.image = image
        row.followers = followers
        row.type = "company"
        data.append(row)
    else:
        search = False
            # break

print(json.dumps(result.__dict__))
# except:
#     result.code = 0
#     result.msg = "There's an error"
# finally:
#     # driver.quit()
#     result.data = [ob.__dict__ for ob in data]
    # print(json.dumps(result.__dict__))

