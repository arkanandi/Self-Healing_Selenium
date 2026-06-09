"""Login page object"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import BASE_URL


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message-container')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = BASE_URL
    
    def navigate(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        self.logger.info(f"Navigated to {self.url}")
    
    def login(self, username, password):
        """Perform login"""
        self.logger.info(f"Logging in with username: {username}")
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def get_error_message(self):
        """Get error message if login fails"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None