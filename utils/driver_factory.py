"""Driver factory for creating WebDriver instances"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.settings import BROWSER, HEADLESS
from utils.logger import Logger


class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    logger = Logger(__name__).get_logger()
    
    @staticmethod
    def create_driver():
        """Create WebDriver instance based on configuration"""
        if BROWSER == 'chrome':
            return DriverFactory._create_chrome_driver()
        elif BROWSER == 'firefox':
            return DriverFactory._create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {BROWSER}")
    
    @staticmethod
    def _create_chrome_driver():
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if HEADLESS:
            options.add_argument('--headless')
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        DriverFactory.logger.info("Creating Chrome WebDriver")
        driver = webdriver.Chrome(options=options)
        return driver
    
    @staticmethod
    def _create_firefox_driver():
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if HEADLESS:
            options.add_argument('--headless')
        
        DriverFactory.logger.info("Creating Firefox WebDriver")
        driver = webdriver.Firefox(options=options)
        return driver