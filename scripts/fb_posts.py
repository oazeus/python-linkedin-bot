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
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--incognito')
        options.add_argument('--log-level=3')
        return webdriver.Chrome(settings.chrome_driver, options=options)

    @staticmethod
    def login(driver):
        try:
            driver.get(settings.fb_base_url + settings.fb_login_url)
            username = driver.find_element_by_id(settings.fb_username_field_id)
            username.send_keys(settings.fb_username)
            password = driver.find_element_by_xpath('//*[@type="password"]')
            password.send_keys(settings.fb_password)
            log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
            log_in_button.click()
            return True
        except Exception as ex:
            return False
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
    def scrap(driver, url:str):
        try:
            driver.get(url)

            resultContainer = driver.find_elements_by_css_selector('#BrowseResultsContainer')
            if(len(resultContainer) == 0):  
                result.ended = True
                return

            elems = resultContainer[0].find_elements_by_css_selector('article')
                
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
                            e = presentationEl.find_elements_by_css_selector('tr td:nth-child(1) img')
                            presentation["image"] = e[0].get_attribute("src")
                        except:
                            presentation["image"] = ""

                        try:
                            e = presentationEl.find_elements_by_css_selector('tr td:nth-child(2) h3')
                            presentation["text"] = e[0].text
                        except:
                            presentation["text"] = ""

                        try:
                            e = presentationEl.find_elements_by_css_selector('tr td:nth-child(2) div')
                            presentation["referrer_url"] = e[0].text
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
                        elike = footer.find_element_by_xpath('.//span[contains(@id, "like_")]')
                        post_id = driver.execute_script("return arguments[0].id", elike)
                        post_id = elike.get_attribute("id").replace("like_").strip()
                    except:
                        post_id = ""

                    try:
                        likesEl = footer.find_element_by_css_selector('div:nth-child(2) span:nth-child(1) > a:nth-child(1)')
                        likes = likesEl.text
                        likes = likes.replace("Likes", "").replace("Like", "").replace(",", "").strip()
                        if likes == "":
                            likes = "0"

                        # Retry getting the post id using the like button
                        if not post_id:
                            try:
                                likesEl = footer.find_element_by_xpath('.//a[contains(text(), "Like")]')
                                like_url = likesEl.get_attribute("href")
                                if like_url:
                                    post_id = Facebook.value_from_url(like_url, "story_fbid")
                                    if not post_id:
                                        post_id  = Facebook.value_from_url(like_url, "ft_ent_identifier")
                            except Exception as ex:
                                post_id = ""
                    except:
                        likes = "0"

                    try:
                        # commentEl = footer.find_element_by_css_selector('div:nth-child(2) span:nth-child(1) + span + a')
                        commentEl = footer.find_element_by_xpath('.//a[contains(text(), "Comment")]')
                        comments = commentEl.text
                        if comments.count("Comment"):
                            comments = comments.replace("Comments", "").replace("Comment", "").replace(",", "").strip()
                            if not comments:
                                comments = "0"
                            
                            # Retry getting the post id using the comment button
                            if not post_id:
                                comment_url = commentEl.get_attribute("href")
                                if comment_url: 
                                    post_id = Facebook.value_from_url(comment_url, "story_fbid")
                                    pid = Facebook.value_from_url(comment_url, "id")
                                    post_url = Facebook.get_post_url(post_id, pid)
                        else: 
                            comments = "0"
                    except:
                        comments = "0"

                    # Retry getting the post id using the full story button
                    if not post_id:
                        try:
                            fullStoryEl = footer.find_element_by_xpath('.//a[contains(text(), "Full Story")]')
                            story_url = fullStoryEl.get_attribute("href")
                            if story_url: 
                                post_id = Facebook.value_from_url(story_url, "story_fbid")
                                pid = Facebook.value_from_url(story_url, "id")
                        except Exception as ex:
                            post_id = ""

                    if post_id:
                        if post_id and not post_url:
                            post_url = Facebook.get_post_url(post_id, "1")

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
                    pagerEl = driver.find_elements_by_css_selector("#see_more_pager a")
                    if len(pagerEl) > 0:
                        url = pagerEl[0].get_attribute("href")
                        Facebook.scrap(driver, url)
                except Exception as ex:
                    result.msg = str(ex)
            else:
                result.ended = True
        except Exception as ex:
            result.code = "0"
            result.msg = str(ex)

if __name__ == '__main__':
    chome_driver = Facebook.init_driver()
    try:
        if Facebook.login(chome_driver):
            keywords = keywords.split("+")
            if len(keywords) > 0:
                for keyword in keywords:
                    date_to_search = str((datetime.today() - timedelta(days=1)).strftime('%B %d, %Y'))
                    date_to_search = ""
                    keyword = keyword + " " + date_to_search
                    url = settings.fb_base_url + settings.fb_posts_search_url + "&q=" + keyword.strip()
                    Facebook.scrap(chome_driver, url)
    except Exception as ex:
        result.code = "0"
        result.msg  = str(ex)
    finally:
        # chome_driver.quit()
        result.data = [ob.__dict__ for ob in result.data]
        print(json.dumps(result.__dict__))

