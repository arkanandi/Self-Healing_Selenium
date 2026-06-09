"""Base page class for all page objects"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import Logger
from utils.healing_driver import HealingDriver


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        """Initialize the base page with driver instance"""
        self.driver = HealingDriver(driver) if not isinstance(driver, HealingDriver) else driver
        self.wait = WebDriverWait(self.driver.driver, 10)
        self.logger = Logger(__name__).get_logger()
    
    def find_element(self, locator):
        """Find element using self-healing capability"""
        return self.driver.find_element(locator)
    
    def find_elements(self, locator):
        """Find multiple elements"""
        return self.driver.find_elements(locator)
    
    def click_element(self, locator):
        """Click an element"""
        self.logger.info(f"Clicking element: {locator}")
        element = self.find_element(locator)
        element.click()
    
    def type_text(self, locator, text):
        """Type text into an element"""
        self.logger.info(f"Typing text in element: {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from an element"""
        element = self.find_element(locator)
        return element.text
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be visible"""
        self.logger.info(f"Waiting for element: {locator}")
        return WebDriverWait(self.driver.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            self.wait_for_element(locator, 5)
            return True
        except:
            return False