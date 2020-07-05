from dotenv import load_dotenv
import os
load_dotenv()
chrome_driver = os.getenv("CHROME_DRIVER")

linkedin_base_url = "https://www.linkedin.com"
linkedin_login_url = "/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
linkedin_company_search_url = "/search/results/companies/?origin=TYPEAHEAD_ESCAPE_HATCH"
linkedin_job_search_url = "/jobs/search"
linkedin_username_field_id = "username"
linkedin_password_field_id = "password"
linkedin_signin_button_class = "sign-in-form__submit-button"
linkedin_search_field_class = "search-global-typeahead__input"

linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")


fb_base_url = "https://free.facebook.com"
fb_login_url = "/login/"
fb_username_field_id = "m_login_email"
fb_posts_search_url = "/search/posts/?source=filter&isTrending=0"
fb_username = os.getenv("LINKEDIN_USERNAME")
fb_password = os.getenv("LINKEDIN_PASSWORD")

