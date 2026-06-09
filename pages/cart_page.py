"""Cart page object"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Cart page object"""
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, 'cart_item')
    ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')
    ITEM_PRICE = (By.CLASS_NAME, 'inventory_item_price')
    REMOVE_BUTTON = (By.NAME, 'remove')
    CONTINUE_SHOPPING = (By.ID, 'continue-shopping')
    CHECKOUT_BUTTON = (By.ID, 'checkout')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_items(self):
        """Get all items in cart"""
        items = self.find_elements(self.CART_ITEMS)
        self.logger.info(f"Found {len(items)} items in cart")
        return items
    
    def remove_item(self, item_index):
        """Remove item from cart by index"""
        items = self.get_cart_items()
        if item_index < len(items):
            items[item_index].find_element(*self.REMOVE_BUTTON).click()
            self.logger.info(f"Removed item at index {item_index} from cart")
    
    def proceed_to_checkout(self):
        """Click checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
        self.logger.info("Proceeding to checkout")
    
    def continue_shopping(self):
        """Click continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING)
        self.logger.info("Continuing shopping")