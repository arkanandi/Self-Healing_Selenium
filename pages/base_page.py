"""Base page class for all page objects

This module contains the BasePage class which serves as the parent class for all page objects
in the Selenium framework. It provides common methods for interacting with web elements,
including explicit waits, element finding with self-healing capability, and pop-up dismissal.

The class wraps the native Selenium WebDriver with a HealingDriver to enable automatic
locator recovery when elements are not found, improving test reliability.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import Logger
from utils.healing_driver import HealingDriver
import time


class BasePage:
    """Base class for all page objects.
    
    This class encapsulates common Selenium operations and provides a consistent interface
    for all page objects (LoginPage, InventoryPage, CartPage, etc.). It handles element
    finding, waiting, typing, clicking, and most importantly, dismissing pop-ups that may
    interrupt the test workflow.
    
    Every page object inherits from this class to ensure consistent behavior and reusable methods.
    """
    
    def __init__(self, driver):
        """Initialize the base page with driver instance.
        
        Args:
            driver: Selenium WebDriver instance. Will be wrapped with HealingDriver
                   to enable self-healing locator recovery on element not found errors.
        """
        # Wrap driver with HealingDriver if not already wrapped - this enables self-healing
        # which automatically tries alternative locator strategies when an element is not found
        self.driver = HealingDriver(driver) if not isinstance(driver, HealingDriver) else driver
        # Initialize WebDriverWait with 10-second timeout for all explicit waits
        self.wait = WebDriverWait(self.driver.driver, 10)
        # Get logger instance for this class to log all page interactions
        self.logger = Logger.get_logger(__name__)
    
    def find_element(self, locator):
        """Find element using self-healing capability.
        
        This method waits for element visibility before returning it. It uses the
        HealingDriver wrapper which automatically attempts alternative locators
        if the primary locator fails, improving robustness.
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for element location
            
        Returns:
            WebElement: The found element
        """
        # Wait for element to be visible before proceeding
        self.wait_for_element(locator)
        # Return element using HealingDriver wrapper which enables self-healing on failures
        return self.driver.find_element(locator)
    
    def find_elements(self, locator):
        """Find multiple elements matching the locator.
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for element location
            
        Returns:
            List[WebElement]: List of matching elements (may be empty)
        """
        # Use HealingDriver to find all elements - also supports self-healing
        return self.driver.find_elements(locator)
    
    def click_element(self, locator):
        """Click an element at the specified locator.
        
        This method finds an element and clicks it. Logging is included for test
        troubleshooting and workflow visibility.
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for element location
        """
        # Log the action for test reporting and debugging purposes
        self.logger.info(f"Clicking element: {locator}")
        # Find element with self-healing capability
        element = self.find_element(locator)
        # Perform the click action
        element.click()
    
    def type_text(self, locator, text):
        """Type text into an input field.
        
        This method finds an element, clears any existing text, and types new text.
        Used primarily for form inputs like username, password, search boxes.
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for the input element
            text: String text to type into the element
        """
        # Log the action for test reporting
        self.logger.info(f"Typing text in element: {locator}")
        # Wait for element to be visible and ready for interaction
        element = self.wait_for_element(locator)
        # Clear any pre-existing text in the field (handles autofill scenarios)
        element.clear()
        # Type the new text into the field
        element.send_keys(text)
    
    def open_url(self, url):
        """Open a URL in the current browser session.
        
        This method navigates the browser to a new URL. Used to start tests or
        navigate between pages within the application.
        
        Args:
            url: String URL to navigate to
        """
        # Log navigation for test reporting
        self.logger.info(f"Opening URL: {url}")
        # Navigate to the URL using Selenium's get() method
        self.driver.get(url)
    
    def get_text(self, locator):
        """Get text content from an element.
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for element location
            
        Returns:
            String: Text content of the element
        """
        # Find element with self-healing capability
        element = self.find_element(locator)
        # Return the text content of the element
        return element.text
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to become visible on the page.
        
        Uses WebDriverWait with an explicit timeout to ensure the element is
        visible before returning. This prevents race conditions where elements
        haven't loaded or are not yet visible when accessed.
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for element location
            timeout: Max seconds to wait for element visibility (default: 10)
            
        Returns:
            WebElement: The visible element
            
        Raises:
            TimeoutException: If element is not visible within timeout period
        """
        # Log the wait operation for debugging
        self.logger.info(f"Waiting for element: {locator}")
        # Use WebDriverWait with explicit timeout and visibility condition
        # This ensures the element is not just present in DOM, but actually visible to user
        return WebDriverWait(self.driver.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def dismiss_password_popup(self):
        """Aggressively dismiss password manager or browser notification pop-ups.
        
        This method uses multiple strategies to handle pop-ups that may appear after
        login or form submission. Chrome's password manager pop-ups can block test
        execution, so this implements a three-pronged approach:
        
        1. Click skip/not-now/dismiss buttons (for password manager dialogs)
        2. Press Escape key (universal dialog dismissal)
        3. Use keyboard navigation (Tab + Enter for fallback closure)
        
        Why this is needed: Chrome's password manager often appears after login,
        blocking further automation if not dismissed. By combining multiple strategies,
        we ensure robust handling across different browser configurations and websites.
        
        Returns:
            bool: True if a pop-up was successfully dismissed, False if none found
        """
        try:
            # Strategy 1: Try clicking various skip/not-now buttons that appear in dialogs
            # These XPaths target common button labels and classes used by password managers
            skip_buttons = [
                (By.XPATH, "//button[contains(text(), 'Not now')]"),  # Common password manager text
                (By.XPATH, "//button[contains(text(), 'Never')]"),     # Never save password variant
                (By.XPATH, "//button[contains(text(), 'Skip')]"),      # Generic skip button
                (By.XPATH, "//button[contains(text(), 'Dismiss')]"),   # Notification dismissal
                (By.XPATH, "//button[@aria-label='Not now']"),        # Accessible button label
                (By.XPATH, "//button[@aria-label='Dismiss']"),        # Accessible label variant
                (By.XPATH, "//button[@aria-label='Skip']"),           # Another accessible variant
                (By.XPATH, "//*[contains(@class, 'cancel')]"),        # Fallback: cancel button class
                (By.XPATH, "//*[contains(@class, 'close')]"),         # Fallback: close button class
            ]
            
            # Try each button strategy with short 1-second timeout
            for locator in skip_buttons:
                try:
                    # Look for button with short timeout - quick fail if not present
                    button = WebDriverWait(self.driver.driver, 1).until(
                        EC.presence_of_element_located(locator)
                    )
                    # Only click if button is actually visible to the user
                    if button.is_displayed():
                        button.click()
                        # Brief pause to allow dialog to close before continuing
                        time.sleep(0.5)
                        # Log successful dismissal for test reporting
                        self.logger.info("Dismissed password pop-up")
                        return True
                except:
                    # This strategy didn't find a button, try next one
                    continue
            
            # Strategy 2: Press Escape key to close any modal dialogs
            # This is the most reliable method for dismissing browser pop-ups
            # as Escape is universally handled by modal dialogs
            try:
                # Wait for body element to be available
                WebDriverWait(self.driver.driver, 1).until(
                    lambda d: d.switch_to.active_element
                )
                # Send Escape key to close any open dialogs
                self.driver.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                # Brief pause for dialog to close
                time.sleep(0.5)
                # Log successful dismissal
                self.logger.info("Pressed Escape to dismiss dialog")
                return True
            except:
                # Escape strategy failed, try next approach
                pass
            
            # Strategy 3: Use Tab key to navigate to button, then Enter to click
            # This is a fallback for cases where dialog is keyboard-focused
            try:
                # Tab to next focusable element (should be the skip button in most dialogs)
                self.driver.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
                # Brief pause for focus change
                time.sleep(0.3)
                # Press Enter to activate the focused button
                self.driver.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                # Brief pause for dialog to close
                time.sleep(0.5)
                # Log successful dismissal
                self.logger.info("Used Tab+Enter to dismiss dialog")
                return True
            except:
                # This strategy also failed, all options exhausted
                pass
                
        except Exception as e:
            # Log any unexpected errors during pop-up dismissal (usually minor)
            self.logger.debug(f"No password pop-up found: {e}")
        # Return False if no pop-up was found or could be dismissed
        return False
    
    def is_element_visible(self, locator):
        """Check if an element is visible on the page.
        
        This is a utility method for conditional logic in tests. It returns a boolean
        without raising an exception, making it useful for assertions and conditional
        test flow (e.g., 'if error message is visible, take action').
        
        Args:
            locator: Tuple of (By.xxx, 'selector') for element location
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            # Try to wait for element with 5-second timeout
            # If successful, element is visible
            self.wait_for_element(locator, 5)
            return True
        except:
            # If wait times out or any error occurs, element is not visible
            return False
