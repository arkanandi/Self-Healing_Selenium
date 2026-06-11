"""Pytest configuration and fixtures"""

import pytest
from utils.driver_factory import DriverFactory
from utils.screenshot import Screenshot
from utils.logger import Logger


logger = Logger.get_logger(__name__)


@pytest.fixture(scope='function')
def driver():
    """Pytest fixture for WebDriver"""
    logger.info("Creating WebDriver instance")
    driver = DriverFactory.create_driver()
    
    yield driver
    
    logger.info("Closing WebDriver instance")
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def screenshot_on_failure(request, driver):
    """Automatically take screenshot on test failure"""
    yield
    
    # Safely check if test failed
    try:
        if hasattr(request, 'node') and hasattr(request.node, 'rep_call'):
            if request.node.rep_call is not None and hasattr(request.node.rep_call, 'failed'):
                if request.node.rep_call.failed:
                    test_name = request.node.name
                    screenshot_name = f"failure_{test_name}.png"
                    Screenshot.take_screenshot(driver, screenshot_name)
                    logger.info(f"Screenshot taken for failed test: {test_name}")
    except Exception as e:
        pass  # Silently ignore screenshot errors


def pytest_configure(config):
    """Pytest configuration hook"""
    logger.info("Starting pytest execution")


def pytest_unconfigure(config):
    """Pytest unconfiguration hook"""
    logger.info("Completed pytest execution")
