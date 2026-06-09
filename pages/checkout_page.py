"""Checkout page object"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout page object"""
    
    # Locators - Step 1 (User Info)
    FIRST_NAME = (By.ID, 'first-name')
    LAST_NAME = (By.ID, 'last-name')
    POSTAL_CODE = (By.ID, 'postal-code')
    CONTINUE_BUTTON = (By.ID, 'continue')
    CANCEL_BUTTON = (By.ID, 'cancel')
    
    # Step 2 (Overview)
    FINISH_BUTTON = (By.ID, 'finish')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Fill checkout information"""
        self.logger.info("Filling checkout information")
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
    
    def continue_to_overview(self):
        """Click continue button"""
        self.click_element(self.CONTINUE_BUTTON)
        self.logger.info("Continuing to order overview")
    
    def finish_checkout(self):
        """Click finish button to complete checkout"""
        self.click_element(self.FINISH_BUTTON)
        self.logger.info("Finished checkout")
    
    def cancel_checkout(self):
        """Click cancel button"""
        self.click_element(self.CANCEL_BUTTON)
        self.logger.info("Cancelled checkout")
