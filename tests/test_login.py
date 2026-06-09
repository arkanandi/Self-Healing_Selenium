"""Test cases for login functionality"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD


class TestLogin:
    """Login test cases"""
    
    def test_successful_login(self, driver):
        """Test successful login with valid credentials"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        
        # Verify navigation to inventory page
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_page_loaded(), "Inventory page should be loaded after successful login"
    
    def test_login_with_invalid_credentials(self, driver):
        """Test login with invalid credentials"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("invalid_user", "invalid_password")
        
        # Verify error message appears
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed for invalid credentials"
        assert "do not match" in error_message.lower() or "username" in error_message.lower()
    
    def test_login_with_empty_username(self, driver):
        """Test login with empty username"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("", DEFAULT_PASSWORD)
        
        # Verify error message appears
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed for empty username"