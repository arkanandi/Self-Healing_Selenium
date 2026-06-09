"""Screenshot utility for capturing screenshots during test execution"""

import os
from datetime import datetime
from config.settings import SCREENSHOT_DIR
from utils.logger import Logger


class Screenshot:
    """Screenshot utility class"""
    
    logger = Logger(__name__).get_logger()
    
    @staticmethod
    def take_screenshot(driver, filename=None):
        """Take screenshot and save to file"""
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        try:
            driver.save_screenshot(filepath)
            Screenshot.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            Screenshot.logger.error(f"Failed to take screenshot: {str(e)}")
            return None
    
    @staticmethod
    def take_element_screenshot(driver, element, filename=None):
        """Take screenshot of specific element"""
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"element_screenshot_{timestamp}.png"
        
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        try:
            element.screenshot(filepath)
            Screenshot.logger.info(f"Element screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            Screenshot.logger.error(f"Failed to take element screenshot: {str(e)}")
            return None