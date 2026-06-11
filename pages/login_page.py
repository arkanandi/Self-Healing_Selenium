"""Login page object for Sauce Demo application.

This module contains the LoginPage class which encapsulates all login functionality.
It extends BasePage to inherit common Selenium operations and adds login-specific methods.

The page object model separates test logic from page structure, making tests more
maintainable and allowing easy updates if the login form changes.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.settings import LOGIN_URL
import time


class LoginPage(BasePage):
    """Login page object for handling authentication.
    
    This class represents the login page and provides methods to interact with
    login form elements. All locators are defined as class constants for easy
    maintenance and to catch typos at import time rather than at runtime.
    
    Example:
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login('username', 'password')
    """
    
    # ============ Page Element Locators ============
    # These are defined as class constants using Selenium's By class
    # This centralized locator definition makes updates easy if the page HTML changes
    USERNAME_INPUT = (By.ID, 'user-name')              # Username input field
    PASSWORD_INPUT = (By.ID, 'password')               # Password input field
    LOGIN_BUTTON = (By.ID, 'login-button')            # Login submit button
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message-container')  # Error message container
    
    def __init__(self, driver):
        """Initialize LoginPage with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
        """
        # Call parent class constructor to set up base functionality
        super().__init__(driver)
        # Store the login URL from configuration
        self.url = LOGIN_URL
    
    def navigate(self):
        """Navigate to the login page.
        
        Opens the login page URL in the browser. This is typically called at the
        start of a login test to ensure we're on the correct page.
        """
        # Open the login URL using the base class method
        self.open_url(self.url)
        # Log navigation for test reporting
        self.logger.info(f"Navigated to {self.url}")
    
    def login(self, username, password):
        """Perform login with provided credentials.
        
        This method handles the complete login flow:
        1. Type username into the username field
        2. Type password into the password field
        3. Click the login button
        4. Dismiss any pop-ups that appear after login
        5. Wait for page to settle
        
        This multi-step approach ensures stable test execution by handling common
        browser behaviors like password manager pop-ups.
        
        Args:
            username: String username to enter
            password: String password to enter
        """
        # Log the login attempt with username for debugging
        self.logger.info(f"Logging in with username: {username}")
        
        # Type username into the username input field
        self.type_text(self.USERNAME_INPUT, username)
        
        # Type password into the password input field
        self.type_text(self.PASSWORD_INPUT, password)
        
        # Click the login button to submit the form
        self.click_element(self.LOGIN_BUTTON)
        
        # Wait for any pop-ups to appear after login
        # (e.g., Chrome password manager dialog appears shortly after login)
        time.sleep(1)
        
        # Dismiss any password manager or notification pop-ups
        # This is critical for test reliability - pop-ups block further automation
        self.dismiss_password_popup()
        
        # Wait for page to settle after login and pop-up dismissal
        # This ensures the inventory page is fully loaded before test continues
        time.sleep(1)
    
    def get_error_message(self):
        """Get error message if login fails.
        
        This method is used to verify error handling in tests. If login fails
        (e.g., invalid credentials), an error message is displayed.
        
        Returns:
            String: Error message text if visible, None if not visible
        """
        # Check if error message element is visible on the page
        if self.is_element_visible(self.ERROR_MESSAGE):
            # If visible, return the error text
            return self.get_text(self.ERROR_MESSAGE)
        # If not visible, login succeeded (no error message)
        return None
