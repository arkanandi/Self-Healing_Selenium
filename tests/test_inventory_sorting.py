"""Test cases for inventory sorting functionality"""

import sys
from pathlib import Path
import time

# Ensure project root is on sys.path when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD


class TestInventorySorting:
    """Inventory sorting test cases"""
    
    def test_inventory_page_loaded(self, driver):
        """Test that inventory page loads after login"""
        print("\n" + "="*60)
        print("TEST: Inventory Page Loads After Login")
        print("="*60)
        
        print("\n[Step 1] Navigating to login page...")
        login_page = LoginPage(driver)
        login_page.navigate()
        time.sleep(1)
        
        print("\n[Step 2] Logging in...")
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        time.sleep(2)
        print("✓ Login successful")
        
        print("\n[Step 3] Verifying inventory page is loaded...")
        inventory_page = InventoryPage(driver)
        page_loaded = inventory_page.is_page_loaded()
        assert page_loaded, "Inventory page should be loaded"
        print("✓ Inventory page is loaded")
        time.sleep(1)
        print("\n✓ Test PASSED: Inventory page loads after login\n")
    
    def test_get_inventory_items(self, driver):
        """Test getting inventory items"""
        print("\n" + "="*60)
        print("TEST: Get Inventory Items")
        print("="*60)
        
        print("\n[Step 1] Logging in...")
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        time.sleep(2)
        print("✓ Login successful")
        
        print("\n[Step 2] Retrieving inventory items...")
        inventory_page = InventoryPage(driver)
        items = inventory_page.get_inventory_items()
        assert len(items) > 0, "Inventory should have items"
        print(f"✓ Found {len(items)} items in inventory")
        time.sleep(1)
        print("\n✓ Test PASSED: Inventory items retrieved successfully\n")
    
    def test_add_multiple_items_to_cart(self, driver):
        """Test adding multiple items to cart"""
        print("\n" + "="*60)
        print("TEST: Add Multiple Items to Cart")
        print("="*60)
        
        print("\n[Step 1] Logging in...")
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        time.sleep(2)
        print("✓ Login successful")
        
        print("\n[Step 2] Adding first item to cart...")
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart(0)
        time.sleep(1)
        print("✓ First item added")
        
        print("\n[Step 3] Adding second item to cart...")
        inventory_page.add_item_to_cart(1)
        time.sleep(1)
        print("✓ Second item added")
        
        print("\n[Step 4] Verifying cart count...")
        cart_count = inventory_page.get_cart_count()
        assert cart_count == 2, f"Cart should have 2 items, but has {cart_count}"
        print(f"✓ Cart now contains {cart_count} items")
        time.sleep(1)
        print("\n✓ Test PASSED: Multiple items added successfully\n")
