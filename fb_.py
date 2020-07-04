#!/usr/bin/env python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
parser.add_argument('--page', nargs='+', type=int, default=[1], help='page number')

args = parser.parse_args()
keywords = args.keywords
page = args.page[0]

if (page > 0):
    page = page
else: 
    page = 1

if keywords is None:
    keywords = "nike"

class Result:
    code = 1
    msg = "Success"
    ended = False
    data = []

class Post:
    post_id  = ""
    post_url    = ""
    profile_name = ""
    profile_link = ""
    caption = ""
    content_html = ""
    post_images = ""
    presentation = { "image": "", "text": "", "link": "", "referrer_url": ""}
    date_posted = ""
    likes = "0"
    comments = "0"
    type = "post"

result = Result()
result.code = 1
result.ended = False
result.msg = "Success"
result.data = []

class Facebook:
    @staticmethod
    def init_driver():
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--no-sandbox')
        return webdriver.Chrome(settings.chrome_driver, options=options)

    @staticmethod
    def login(driver):
        driver.get(settings.fb_base_url + settings.fb_login_url)
        username = driver.find_element_by_id(settings.fb_username_field_id)
        username.send_keys(settings.fb_username)
        password = driver.find_element_by_xpath('//*[@type="password"]')
        password.send_keys(settings.fb_password)
        log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
        log_in_button.click()

    @staticmethod
    def get_post_url(story_fbid, id):
        return settings.fb_base_url + "/story.php?story_fbid=" + story_fbid + "&id=" + id

    @staticmethod
    def value_from_url(url:str, key:str):
        parsed = urlparse.urlparse(url)
        v = parse_qs(parsed.query)[key]
        if v is None:
            v = ['']
        return  v[0]

    @staticmethod
    def scrap(driver, url:str):
        try:
            driver.get(url)
            
            SCROLL_PAUSE_TIME = 2
            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            
            time.sleep(0.2)

            resultContainer = driver.find_elements_by_css_selector('#BrowseResultsContainer')
            if(len(resultContainer) == 0):  
                return

            elems = resultContainer[0].find_elements_by_css_selector('article')

            print("ELEMENTS", len(elems))
                
            if len(elems) > 0:
                for elem in elems: 
                    post_id = post_url = profile_name = profile_link = caption = image = content = date_posted = likes = comments = ""
                    presentation = { "image": "", "text": "", "link": "", "referrer_url": ""}
                    post_images = []

                    profileLinkCont = elem.find_elements_by_css_selector('article header table tr td:nth-child(2) h3 a')
                    if(len(profileLinkCont) > 0):
                        profile_link  = profileLinkCont[0].get_attribute("href")
                        profile_name = profileLinkCont[0].text
                        # print("[PROFILE LINK]: ", profile_link)
                        # print("[PROFILE NAME]: ", profile_name)

                    captionEls = elem.find_elements_by_css_selector('div div span p')
                    if(len(captionEls) > 0):
                        for el in captionEls:
                            caption = caption + el.text
                        # print("[CAPTION]: ", caption)

                    contentEl = elem.find_elements_by_css_selector('div div div')
                    if(len(contentEl) > 0):
                        content = contentEl[0].get_attribute('innerHTML')
                        # print("[POST CONTENT]: ", content)

                    
                    postImagesEl = elem.find_elements_by_css_selector('div header + div + div > div a img')
                    if(len(postImagesEl) > 0):
                        for el in postImagesEl:
                            post_images.append(el.get_attribute("src"))
                        # print("[POST IMAGES]: ", post_images)

                    presentationEl = elem.find_elements_by_css_selector('div div a table')
                    if(len(presentationEl) > 0):
                        presentationEl = presentationEl[0]
                        try:
                            a = presentationEl.find_elements_by_css_selector('tr td:nth-child(1) img')
                            presentation["image"] = a[0].get_attribute("src")
                        except:
                            presentation["image"] = ""

                        try:
                            a = presentationEl.find_elements_by_css_selector('tr td:nth-child(2) h3')
                            presentation["text"] = a[0].text
                        except:
                            presentation["text"] = ""

                        try:
                            a = presentationEl.find_elements_by_css_selector('tr td:nth-child(2) div')
                            presentation["referrer_url"] = a[0].text
                        except:
                            presentation["referrer_url"] = ""

                    # print("[PRESENTATION]: ", presentation)

                    footer = elem.find_elements_by_css_selector('footer')
                    if len(footer) > 0:
                        footer = footer[0]

                    try:
                        date_posted = footer.find_element_by_css_selector('div abbr').text
                    except:
                        date_posted = ""
                    
                    # print("[DATE POSTED]: ", date_posted)

                    try:
                        likes = footer.find_element_by_css_selector('div:nth-child(2) span:nth-child(1) > a:nth-child(1)').text
                        likes = likes.replace("Likes", "").replace("Like", "").replace(",", "").strip()
                    except:
                        likes = "0"

                    # print("[LIKES]: ", likes)

                    try:
                        commentEl = footer.find_element_by_css_selector('div:nth-child(2) span:nth-child(1) + span + a')
                        comments = commentEl.text
                        comments = comments.replace("Comments", "").replace("Comment", "").replace(",", "").strip()
                        
                        comment_url = commentEl.get_attribute("href")
                        if comment_url is not None: 
                            # print("[COMMENT_URL]: ", comment_url)
                            post_id = Facebook.value_from_url(comment_url, "story_fbid")

                            # print("[POST_ID]: ", post_id)
                            pid = Facebook.value_from_url(comment_url, "id")
                            post_url = Facebook.get_post_url(post_id, pid)
                    except:
                        comments = "0"
                        post_id = ""
                        post_url = ""

                    # print("[COMMENTS]: ", comments)
                    # print("[POST ID]: ", post_id)
                    # print("[POST URL]: ", post_url)

                    post = Post()
                    post.post_id = post_id
                    post.post_url = post_url
                    post.profile_name = profile_name
                    post.profile_link = profile_link
                    post.caption = caption
                    post.likes = likes
                    post.comments = comments
                    post.date_posted = date_posted
                    post.post_images = post_images
                    # post.content_html = content
                    post.presentation = presentation
                    post.type = "post"
                    result.data.append(post)

                try:
                    url = driver.find_element_by_css_selector("#see_more_pager a").get_attribute("href")
                    Facebook.scrap(driver, url)
                except Exception as ex:
                    # print("[ERROR]: ", "No view more button", ex)
                    result.msg = str(ex)
            else:
                result.ended = True
        except Exception as ex:
            result.code = "0"
            result.msg = str(ex)


if __name__ == '__main__':
    chome_driver = Facebook.init_driver()
    Facebook.login(chome_driver)
    url = settings.fb_base_url + settings.fb_posts_search_url + "&q=" + keywords
    Facebook.scrap(chome_driver, url)
    chome_driver.quit()
    result.data = [ob.__dict__ for ob in result.data]
    print(json.dumps(result.__dict__))
    print(len(result.data))
