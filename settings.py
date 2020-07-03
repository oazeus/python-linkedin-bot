from dotenv import load_dotenv
import os
load_dotenv()
linkedin_base_url = "https://www.linkedin.com"
linkedin_login_url = "/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
linkedin_company_search_url = "/search/results/companies/?origin=TYPEAHEAD_ESCAPE_HATCH"
linkedin_username_field_id = "username"
linkedin_password_field_id = "password"
linkedin_signin_button_class = "sign-in-form__submit-button"
linkedin_search_field_class = "search-global-typeahead__input"

linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")
chrome_driver = os.getenv("CHROME_DRIVER")