"""Self-healing WebDriver wrapper"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from difflib import SequenceMatcher
from utils.logger import Logger
from config.settings import ENABLE_HEALING, HEALING_STRATEGIES, HEALING_THRESHOLD


class HealingDriver:
    """Wrapper around WebDriver with self-healing capabilities"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = Logger(__name__).get_logger()
        self.locator_history = {}
    
    def find_element(self, locator):
        """Find element with self-healing capability"""
        try:
            # Try original locator
            element = self.driver.find_element(*locator)
            self._store_locator(locator)
            return element
        except NoSuchElementException:
            if ENABLE_HEALING:
                self.logger.warning(f"Element not found with locator: {locator}. Attempting to heal...")
                return self._heal_element(locator)
            else:
                raise
    
    def find_elements(self, locator):
        """Find multiple elements"""
        return self.driver.find_elements(*locator)
    
    def get(self, url):
        """Navigate to URL"""
        self.driver.get(url)
    
    def __getattr__(self, name):
        """Proxy other attributes to driver"""
        return getattr(self.driver, name)
    
    def _heal_element(self, original_locator):
        """Attempt to heal element using alternative strategies"""
        locator_type, locator_value = original_locator
        
        self.logger.info(f"Healing locator: {locator_type} = {locator_value}")
        
        # Try similar locators from history
        for stored_locator in self.locator_history.get(locator_value, []):
            try:
                element = self.driver.find_element(*stored_locator)
                self.logger.info(f"Healed element using stored locator: {stored_locator}")
                return element
            except:
                pass
        
        # Try alternative locator strategies
        for strategy in HEALING_STRATEGIES:
            try:
                if strategy == 'xpath':
                    # Try XPath variations
                    xpath_variations = [
                        f"//*[@id='{locator_value}']",
                        f"//*[contains(@id, '{locator_value}')]",
                        f"//*[@class='{locator_value}']",
                        f"//*[contains(@class, '{locator_value}')]",
                    ]
                    for xpath in xpath_variations:
                        try:
                            element = self.driver.find_element(By.XPATH, xpath)
                            self.logger.info(f"Healed element using XPath: {xpath}")
                            return element
                        except:
                            pass
            except:
                pass
        
        self.logger.error(f"Could not heal element: {original_locator}")
        raise NoSuchElementException(f"Unable to find or heal element: {original_locator}")
    
    def _store_locator(self, locator):
        """Store successful locator for future reference"""
        locator_type, locator_value = locator
        if locator_value not in self.locator_history:
            self.locator_history[locator_value] = []
        if locator not in self.locator_history[locator_value]:
            self.locator_history[locator_value].append(locator)