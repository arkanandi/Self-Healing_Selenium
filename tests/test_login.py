"""Test cases for login functionality"""

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


class TestLogin:
    """Login test cases"""
    
    def test_successful_login(self, driver):
        """Test successful login with valid credentials"""
        print("\n" + "="*60)
        print("TEST: Successful Login with Valid Credentials")
        print("="*60)
        
        print("\n[Step 1] Navigating to login page...")
        login_page = LoginPage(driver)
        login_page.navigate()
        time.sleep(1)
        
        print("[Step 2] Entering credentials...")
        print(f"  - Username: {DEFAULT_USERNAME}")
        print(f"  - Password: {'*' * len(DEFAULT_PASSWORD)}")
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        time.sleep(2)
        
        print("[Step 3] Verifying navigation to inventory page...")
        inventory_page = InventoryPage(driver)
        page_loaded = inventory_page.is_page_loaded()
        assert page_loaded, "Inventory page should be loaded after successful login"
        print("✓ Inventory page loaded successfully")
        time.sleep(1)
        print("\n✓ Test PASSED: Successful login workflow complete\n")
    
    def test_login_with_invalid_credentials(self, driver):
        """Test login with invalid credentials"""
        print("\n" + "="*60)
        print("TEST: Login with Invalid Credentials")
        print("="*60)
        
        print("\n[Step 1] Navigating to login page...")
        login_page = LoginPage(driver)
        login_page.navigate()
        time.sleep(1)
        
        print("[Step 2] Entering invalid credentials...")
        print("  - Username: invalid_user")
        print("  - Password: invalid_password")
        login_page.login("invalid_user", "invalid_password")
        time.sleep(2)
        
        print("[Step 3] Verifying error message appears...")
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed for invalid credentials"
        assert "do not match" in error_message.lower() or "username" in error_message.lower()
        print(f"✓ Error message displayed: {error_message}")
        time.sleep(1)
        print("\n✓ Test PASSED: Invalid credentials error handling works\n")
    
    def test_login_with_empty_username(self, driver):
        """Test login with empty username"""
        print("\n" + "="*60)
        print("TEST: Login with Empty Username")
        print("="*60)
        
        print("\n[Step 1] Navigating to login page...")
        login_page = LoginPage(driver)
        login_page.navigate()
        time.sleep(1)
        
        print("[Step 2] Entering empty username...")
        print("  - Username: (empty)")
        print(f"  - Password: {'*' * len(DEFAULT_PASSWORD)}")
        login_page.login("", DEFAULT_PASSWORD)
        time.sleep(2)
        
        print("[Step 3] Verifying error message appears...")
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed for empty username"
        print(f"✓ Error message displayed: {error_message}")
        time.sleep(1)
        print("\n✓ Test PASSED: Empty username validation works\n")
