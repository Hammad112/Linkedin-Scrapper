# config.py
import os
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import sys

# Append your custom path to sys.path
custom_path = os.getenv('path')  # replace 'YOUR_ENV_VARIABLE' with your actual environment variable name


def create_driver():
    chrome_profile_path = custom_path
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")  # Use your Chrome profile
    return uc.Chrome(options=chrome_options)
