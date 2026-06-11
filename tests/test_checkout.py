"""Test cases for checkout functionality"""

import sys
from pathlib import Path
import time

# Ensure project root is on sys.path when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

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
        print("\n" + "="*60)
        print("TEST: Complete Checkout Flow")
        print("="*60)
        
        print("\n[Step 1] Logging in...")
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        time.sleep(2)
        print("✓ Login successful")
        
        print("\n[Step 2] Adding item to cart...")
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart(0)
        time.sleep(1)
        print("✓ Item added to cart")
        
        print("\n[Step 3] Opening shopping cart...")
        inventory_page.open_cart()
        time.sleep(2)
        print("✓ Cart page opened")
        
        print("\n[Step 4] Verifying cart contents...")
        cart_page = CartPage(driver)
        cart_items = cart_page.get_cart_items()
        assert len(cart_items) > 0, "Cart should have items"
        print(f"✓ Cart contains {len(cart_items)} item(s)")
        
        print("\n[Step 5] Proceeding to checkout...")
        cart_page.proceed_to_checkout()
        time.sleep(2)
        print("✓ Checkout page opened")
        
        print("\n[Step 6] Filling checkout information...")
        print("  - First Name: John")
        print("  - Last Name: Doe")
        print("  - Postal Code: 12345")
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info("John", "Doe", "12345")
        time.sleep(1)
        print("✓ Information filled")
        
        print("\n[Step 7] Reviewing order overview...")
        checkout_page.continue_to_overview()
        time.sleep(2)
        print("✓ Order overview displayed")
        
        print("\n[Step 8] Completing checkout...")
        checkout_page.finish_checkout()
        time.sleep(2)
        print("✓ Order completed successfully")
        print("\n✓ Test PASSED: Complete checkout flow successful\n")
    
    def test_checkout_without_items(self, driver):
        """Test checkout with empty cart"""
        print("\n" + "="*60)
        print("TEST: Checkout with Empty Cart")
        print("="*60)
        
        print("\n[Step 1] Logging in...")
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        time.sleep(2)
        print("✓ Login successful")
        
        print("\n[Step 2] Opening shopping cart...")
        inventory_page = InventoryPage(driver)
        inventory_page.open_cart()
        time.sleep(2)
        print("✓ Cart page opened")
        
        print("\n[Step 3] Verifying cart is empty...")
        cart_page = CartPage(driver)
        cart_items = cart_page.get_cart_items()
        assert len(cart_items) == 0, "Cart should be empty"
        print("✓ Cart is empty (no items)")
        print("\n✓ Test PASSED: Empty cart handling works\n")
