"""Test cases for inventory sorting functionality"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD


class TestInventorySorting:
    """Inventory sorting test cases"""
    
    def test_inventory_page_loaded(self, driver):
        """Test that inventory page loads after login"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_page_loaded(), "Inventory page should be loaded"
    
    def test_get_inventory_items(self, driver):
        """Test getting inventory items"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        inventory_page = InventoryPage(driver)
        items = inventory_page.get_inventory_items()
        assert len(items) > 0, "Inventory should have items"
    
    def test_add_multiple_items_to_cart(self, driver):
        """Test adding multiple items to cart"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart(0)
        inventory_page.add_item_to_cart(1)
        
        cart_count = inventory_page.get_cart_count()
        assert cart_count == 2, f"Cart should have 2 items, but has {cart_count}"
