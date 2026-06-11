"""Inventory page object"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class InventoryPage(BasePage):
    """Inventory page object"""
    
    # Locators
    INVENTORY_CONTAINER = (By.CLASS_NAME, 'inventory_container')
    INVENTORY_ITEMS = (By.CLASS_NAME, 'inventory_item')
    ITEM_NAME = (By.CLASS_NAME, 'inventory_item_name')
    ITEM_PRICE = (By.CLASS_NAME, 'inventory_item_price')
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'button[id^="add-to-cart"]')
    CART_LINK = (By.CLASS_NAME, 'shopping_cart_link')
    CART_BADGE = (By.CLASS_NAME, 'shopping_cart_badge')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_page_loaded(self):
        """Check if inventory page is loaded"""
        return self.is_element_visible(self.INVENTORY_CONTAINER)
    
    def get_inventory_items(self):
        """Get all inventory items"""
        items = self.find_elements(self.INVENTORY_ITEMS)
        self.logger.info(f"Found {len(items)} inventory items")
        return items
    
    def add_item_to_cart(self, item_index):
        """Add item to cart by index"""
        items = self.get_inventory_items()
        if item_index < len(items):
            # Click add to cart button within the item
            items[item_index].find_element(*self.ADD_TO_CART_BUTTON).click()
            self.logger.info(f"Added item at index {item_index} to cart")
    
    def open_cart(self):
        """Open the shopping cart page"""
        self.click_element(self.CART_LINK)
        self.logger.info("Opened cart page")
    
    def get_cart_count(self):
        """Get items in cart count"""
        try:
            badge = self.find_element(self.CART_BADGE)
            return int(badge.text)
        except:
            return 0
