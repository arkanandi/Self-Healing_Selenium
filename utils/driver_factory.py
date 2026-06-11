"""Driver factory for creating WebDriver instances

This module provides the DriverFactory class which is responsible for creating and
configuring WebDriver instances (Chrome, Firefox, etc.) with optimized settings.

Key Features:
- Centralized browser configuration management
- Automatic Chrome options for automation (hiding Selenium detection, disabling popups)
- Password manager pop-up prevention
- Logging of driver creation for debugging

The factory pattern ensures consistent WebDriver setup across all tests.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.settings import BROWSER, HEADLESS
from utils.logger import Logger


class DriverFactory:
    """Factory class for creating WebDriver instances.
    
    This class uses the Factory design pattern to centralize WebDriver creation.
    It ensures all drivers are configured consistently with the same options,
    making it easy to apply global changes to browser behavior across the entire
    test suite.
    """
    
    logger = Logger.get_logger(__name__)
    
    @staticmethod
    def create_driver():
        """Create WebDriver instance based on configuration.
        
        Reads the BROWSER setting from config.settings and creates the appropriate
        WebDriver instance with all necessary options applied.
        
        Returns:
            WebDriver: Configured Chrome or Firefox WebDriver instance
            
        Raises:
            ValueError: If BROWSER setting is not 'chrome' or 'firefox'
        """
        # Check which browser is configured
        if BROWSER == 'chrome':
            return DriverFactory._create_chrome_driver()
        elif BROWSER == 'firefox':
            return DriverFactory._create_firefox_driver()
        else:
            # Raise error if unsupported browser is requested
            raise ValueError(f"Unsupported browser: {BROWSER}")
    
    @staticmethod
    def _create_chrome_driver():
        """Create Chrome WebDriver with optimized automation settings.
        
        This method sets up Chrome with numerous options designed to:
        1. Hide automation detection (avoid bot detection by websites)
        2. Disable pop-ups that can block test execution
        3. Disable features that interfere with automation
        4. Optimize performance
        
        Key options explained:
        - disable-blink-features=AutomationControlled: Removes navigator.webdriver flag
          that websites use to detect Selenium automation
        - disable-notifications: Prevents Chrome notification pop-ups
        - disable-extensions: Prevents extensions from loading, which can slow tests
        - Prefs for password_manager_enabled/False: Prevents password save dialogs
        - excludeSwitches with enable-automation: Hides Selenium detection
        
        Returns:
            WebDriver: Configured Chrome WebDriver ready for test execution
        """
        # Create Chrome options object to hold all configuration
        options = ChromeOptions()
        
        # If HEADLESS mode is enabled in config, run browser in headless mode
        # (invisible - no GUI window)
        if HEADLESS:
            options.add_argument('--headless')
        
        # Hide the fact that we're using Selenium/automation
        # This prevents websites from detecting and blocking automated tests
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Disable sandboxing (may be needed on some systems)
        options.add_argument('--no-sandbox')
        
        # Use /dev/shm instead of RAM for storing temporary data
        # (improves performance on systems with limited /dev/shm)
        options.add_argument('--disable-dev-shm-usage')
        
        # Start with maximized window for better element visibility
        options.add_argument('--start-maximized')
        
        # ============ Disable Pop-up Prevention Options ============
        # Disable system notifications that can interrupt automation
        options.add_argument('--disable-notifications')
        
        # Disable translation UI prompts ("Translate this page?")
        options.add_argument('--disable-features=TranslateUI,TranslateUISecondaryUI')
        
        # Disable Chrome sync to prevent sync-related pop-ups
        options.add_argument('--disable-sync')
        
        # Disable extensions that might interfere with tests
        options.add_argument('--disable-extensions')
        
        # ============ Preferences for Password Manager Suppression ============
        # These prefs target Chrome's password manager and autofill features
        options.add_experimental_option('prefs', {
            # Disable password save prompt completely
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
            # Disable popups (set to 0 = block all popups)
            'profile.default_content_settings.popups': 0,
            # Disable autofill suggestions
            'autofill.server_suggestions_enabled': False,
            # Another password manager flag
            'password_manager.enabled': False,
            # Disable password breach detection (which triggers pop-ups)
            'profile.password_manager_leak_detection': False,
            # Auto-download files instead of prompting
            'profile.default_content_setting_values.automatic_downloads': 1,
            # Disable translation prompts
            'translate_whitelists': {},
            'translate': {'enabled': False}
        })
        
        # ============ Exclude Automation Detection Switches ============
        # These flags prevent Selenium detection
        options.add_experimental_option('excludeSwitches', [
            'enable-automation',      # Removes navigator.webdriver
            'enable-logging',         # Disable Chrome logging
            'disable-popup-blocking'  # Keep popup blocking enabled
        ])
        
        # Disable useAutomationExtension to prevent webdriver property
        options.add_experimental_option('useAutomationExtension', False)
        
        # Log that we're creating the driver for debugging
        DriverFactory.logger.info("Creating Chrome WebDriver")
        # Create and return the configured Chrome WebDriver
        driver = webdriver.Chrome(options=options)
        return driver
    
    @staticmethod
    def _create_firefox_driver():
        """Create Firefox WebDriver.
        
        Similar to Chrome driver creation, this configures Firefox with test automation
        in mind. Firefox is sometimes used as an alternative to Chrome for cross-browser
        testing or when specific Firefox features are needed.
        
        Returns:
            WebDriver: Configured Firefox WebDriver
        """
        # Create Firefox options object
        options = FirefoxOptions()
        
        # Apply headless mode if configured
        if HEADLESS:
            options.add_argument('--headless')
        
        # Log driver creation
        DriverFactory.logger.info("Creating Firefox WebDriver")
        # Create and return the configured Firefox WebDriver
        driver = webdriver.Firefox(options=options)
        return driver
