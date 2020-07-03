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
# parser.add_argument('--page', nargs='+', type=int, default=[1], help='page number')

args = parser.parse_args()
keywords = args.keywords

page = 1

if keywords is None:
    keywords = "orangeapps"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(settings.chrome_driver, options=options)

class Result:
    code = 1
    msg = "Success"
    data = []

class Job:
    position = ""
    company = ""
    company_image = ""
    location = ""
    description = ""
    seniorities = []
    employment_types = []
    industries = []
    job_functions = []
    date = ""
    type = "job"

result = Result()
result.code = 1
result.msg = "Success"
data = []

try: 
    driver.get(settings.linkedin_base_url + settings.linkedin_job_search_url + "?keywords=" + keywords + "&location=Philippines&page=" + str(page))
    # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result__occluded-item"))) #wait for all listings content
    SCROLL_PAUSE_TIME = 2
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        showMore = driver.find_elements_by_class_name("infinite-scroller__show-more-button")
        if len(showMore) > 0:
            driver.execute_script("arguments[0].style.display = \"block\"", showMore[0])
            driver.execute_script("arguments[0].click();", showMore[0])
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # elems = driver.find_elements_by_class_name('entity-result__item')
    elems = driver.find_elements_by_css_selector('li.job-result-card')
    if len(elems) > 0:
        for elem in elems: 
            position = company = location = date = image = description = ""
            seniorities = []
            employment_types = []
            job_functions = []
            industries = []
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            driver.execute_script("arguments[0].click()", elem)
            time.sleep(2)
            
            positionEl = elem.find_elements_by_css_selector('.job-result-card__title')
            if len(positionEl) > 0:
                position = positionEl[0].text
                print(position)

            companyEl = elem.find_elements_by_css_selector('.job-result-card__subtitle')
            if len(companyEl) > 0:
                company = companyEl[0].text
                print(company)

            locationEl = elem.find_elements_by_css_selector('.job-result-card__location')
            if len(locationEl) > 0:
                location = locationEl[0].text
                print(location)

            dateEl = elem.find_elements_by_css_selector('.job-result-card__listdate')
            if len(dateEl) > 0:
                date = dateEl[0].get_attribute('datetime')
                print(date)


            imageEl = elem.find_elements_by_css_selector('img.result-card__image');
            if(len(imageEl) > 0):
                image = imageEl[0].get_attribute("src")
                print(image)

            descEl = driver.find_elements_by_css_selector('div.show-more-less-html__markup');
            if(len(descEl) > 0):
                description = descEl[0].get_attribute('innerHTML')
                print(description)

            seniorityEl = driver.find_elements_by_css_selector('ul.job-criteria__list li:nth-child(1) .job-criteria__text');
            if(len(seniorityEl) > 0):
                for el in seniorityEl:
                    seniorities.append(el.text)

            print(seniorities)

            empTypeEl = driver.find_elements_by_css_selector('ul.job-criteria__list li:nth-child(2) .job-criteria__text');
            if(len(empTypeEl) > 0):
                for el in empTypeEl:
                    employment_types.append(el.text)

            print(employment_types)

            jobFuncEl = driver.find_elements_by_css_selector('ul.job-criteria__list li:nth-child(3) .job-criteria__text');
            if(len(jobFuncEl) > 0):
                for el in jobFuncEl:
                    job_functions.append(el.text)

            print(job_functions)

            industryEl = driver.find_elements_by_css_selector('ul.job-criteria__list li:nth-child(4) .job-criteria__text');
            if(len(industryEl) > 0):
                for el in industryEl:
                    industries.append(el.text)

            print(industries)

            job = Job()
            job.position = position 
            job.company = company
            job.company_image = image 
            job.description = description
            job.location = location
            job.date = date
            job.seniorities = seniorities
            job.employment_types = employment_types
            job.job_functions = job_functions
            job.industries = industries
            job.type = "job"
            data.append(job)
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