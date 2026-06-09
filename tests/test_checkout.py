"""Test cases for checkout functionality"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD


class TestCheckout:
    """Checkout test cases"""
    
    def test_complete_checkout_flow(self, driver):
        """Test complete checkout flow"""
        # Login
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        # Add item to cart
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart(0)
        
        # Go to cart
        cart_page = CartPage(driver)
        cart_items = cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should have items"
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        
        # Fill checkout information
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info("John", "Doe", "12345")
        checkout_page.continue_to_overview()
        checkout_page.finish_checkout()
    
    def test_checkout_without_items(self, driver):
        """Test checkout with empty cart"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        # Verify cart is empty
        inventory_page = InventoryPage(driver)
        assert inventory_page.get_cart_count() == 0, "Cart should be empty"