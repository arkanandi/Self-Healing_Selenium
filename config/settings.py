"""Configuration settings for the Self-Healing Selenium framework"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Browser Configuration
BROWSER = os.getenv('BROWSER', 'chrome').lower()
HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
TIMEOUT = int(os.getenv('TIMEOUT', '10'))

# Application URLs
BASE_URL = os.getenv('BASE_URL', 'https://www.saucedemo.com')
LOGIN_URL = f"{BASE_URL}/"

# Test Data
DEFAULT_USERNAME = os.getenv('DEFAULT_USERNAME', 'standard_user')
DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD', 'secret_sauce')

# Self-Healing Configuration
ENABLE_HEALING = os.getenv('ENABLE_HEALING', 'True').lower() == 'true'
HEALING_STRATEGIES = ['id', 'name', 'xpath', 'css_selector', 'link_text']
HEALING_THRESHOLD = float(os.getenv('HEALING_THRESHOLD', '0.7'))

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')
SCREENSHOT_DIR = os.path.join(LOG_DIR, 'screenshots')

# Report Configuration
REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')