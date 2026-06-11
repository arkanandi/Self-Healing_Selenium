# Self-Healing Selenium

A robust, self-healing Selenium automation framework that intelligently adapts to UI changes, handles browser pop-ups, and recovers from element locator failures.

## Overview

Self-Healing Selenium is an advanced test automation framework designed to make Selenium testing more resilient and maintainable. It automatically handles:

- **Element locator failures** through intelligent self-healing strategies
- **Browser pop-ups** that interrupt test execution (password managers, notifications, etc.)
- **Page load variations** with smart explicit waits
- **Automation detection** by hiding Selenium indicators

The framework implements the Page Object Model pattern and includes comprehensive logging for easy debugging.

## Key Features

### 🔧 Self-Healing Locators
- Automatically adapts when element locators fail
- Tries multiple strategies: ID, Name, XPath, CSS Selector, Link Text
- Reduces test maintenance overhead when UI changes
- Provides detailed logging of healing attempts

### 🛡️ Browser Pop-up Handling
- Automatically detects and dismisses password manager dialogs
- Handles Chrome notification pop-ups
- Uses three strategies: button clicking, keyboard shortcuts (Escape, Tab+Enter)
- Prevents pop-ups from blocking test execution

### 🤖 Automation Detection Evasion
- Hides Selenium's `navigator.webdriver` indicator
- Disables automation detection features in Chrome
- Bypasses websites that detect and block automated testing
- Reduces false negatives from anti-bot systems

### ⏳ Smart Waits & Synchronization
- Explicit waits for element visibility (not just presence)
- Configurable timeout values (default: 10 seconds)
- Prevents race conditions and timing-dependent failures
- Log-based tracking of wait durations

### 📋 Page Object Model
- Centralized element locators for maintainability
- Consistent interface across all page objects
- Easy to update locators when UI changes
- Improves test readability and organization

### 📝 Comprehensive Logging
- Tracks all WebDriver operations (navigation, clicks, typing)
- Logs self-healing recovery attempts
- Records pop-up dismissal actions
- Helps troubleshoot flaky tests

## Project Structure

```
Self-Healing_Selenium/
├── config/                      # Configuration files
│   ├── settings.py             # Global settings (URLs, credentials, timeouts)
│   └── __init__.py
├── pages/                       # Page objects
│   ├── base_page.py            # Base class with common operations
│   ├── login_page.py           # Login page object
│   ├── inventory_page.py       # Inventory/products page
│   ├── cart_page.py            # Shopping cart page
│   ├── checkout_page.py        # Checkout page
│   └── __init__.py
├── utils/                       # Utilities
│   ├── driver_factory.py       # WebDriver factory with optimizations
│   ├── healing_driver.py       # Self-healing wrapper for WebDriver
│   ├── logger.py               # Centralized logging
│   ├── screenshot.py           # Screenshot utilities
│   └── __init__.py
├── tests/                       # Test suites
│   ├── test_login.py           # Login functionality tests
│   ├── test_inventory_sorting.py # Inventory tests
│   ├── test_checkout.py        # Checkout flow tests
│   └── __init__.py
├── reports/                     # Test reports and screenshots
│   └── screenshots/            # Screenshot directory for failures
├── demo.py                      # Demonstration script
├── conftest.py                  # pytest configuration and fixtures
├── pytest.ini                   # pytest settings
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .github/                     # GitHub Actions workflows
│   └── workflows/
│       └── ui-tests.yml        # CI/CD pipeline
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd Self-Healing_Selenium
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration (optional)
# Default values are already set for Sauce Demo app
```

## Usage

### Running Demo
The demo script showcases the complete automation workflow:

```bash
python demo.py
```

This will:
1. Open Chrome browser
2. Navigate to https://www.saucedemo.com
3. Log in with test credentials
4. Add items to cart
5. Display the cart
6. Keep browser open for inspection
7. Close on user input

### Running Tests
```bash
# Run all tests with verbose output
pytest tests/ -v -s

# Run specific test file
pytest tests/test_login.py -v

# Run specific test
pytest tests/test_login.py::test_login_successful -v

# Run with logging
pytest tests/ -v -s --log-cli-level=INFO
```

### Running Tests in Headless Mode
```bash
# Set environment variable
set HEADLESS=True

# Run tests
pytest tests/ -v
```

## Core Components

### BasePage Class
The foundation of all page objects. Provides:
- Element finding with self-healing
- Explicit waits for element visibility
- Pop-up dismissal methods
- Text input and clicking
- Element visibility checks

**Key Methods:**
- `find_element(locator)` - Find single element with self-healing
- `click_element(locator)` - Click element
- `type_text(locator, text)` - Type text into element
- `wait_for_element(locator, timeout)` - Wait for visibility
- `dismiss_password_popup()` - Handle browser pop-ups
- `is_element_visible(locator)` - Check visibility

### HealingDriver Wrapper
Implements self-healing locator recovery:
- Tries primary locator
- Falls back to alternative strategies if primary fails
- Logs all recovery attempts
- Maintains test execution without failure

**Locator Recovery Strategy Order:**
1. ID selector
2. Name attribute
3. XPath
4. CSS Selector
5. Link text

### DriverFactory
Creates optimized WebDriver instances with:
- Chrome automation detection evasion
- Password manager pop-up suppression
- Performance optimizations
- Configurable headless mode
- Consistent browser settings

### Logger
Centralized logging with:
- File and console output
- Multiple log levels (INFO, DEBUG, WARNING, ERROR)
- Timestamped entries
- Test-specific logging contexts

## Configuration

All settings are in `config/settings.py`:

```python
# Browser Settings
BROWSER = 'chrome'           # 'chrome' or 'firefox'
HEADLESS = False             # Run browser hidden

# Application URLs
BASE_URL = 'https://www.saucedemo.com'
LOGIN_URL = f"{BASE_URL}/"

# Test Data
DEFAULT_USERNAME = 'standard_user'
DEFAULT_PASSWORD = 'secret_sauce'

# Waits & Timeouts
TIMEOUT = 10                 # Default element wait timeout

# Logging
LOG_LEVEL = 'INFO'
LOG_DIR = 'reports'

# Self-Healing
ENABLE_HEALING = True
HEALING_THRESHOLD = 0.7      # Similarity threshold for recovery
```

### Environment Variables
Create `.env` file for sensitive data:

```env
# Credentials
DEFAULT_USERNAME=standard_user
DEFAULT_PASSWORD=secret_sauce

# Browser Settings
BROWSER=chrome
HEADLESS=False

# Logging
LOG_LEVEL=INFO
```

## Pop-up Handling Strategy

The framework automatically handles browser pop-ups using a three-pronged approach:

### Strategy 1: Button Clicking
Looks for and clicks common dialog buttons:
- "Not now" (password save dialogs)
- "Skip", "Never", "Dismiss"
- Accessible buttons with aria-label attributes

### Strategy 2: Escape Key
Sends the Escape key which universally dismisses most browser dialogs

### Strategy 3: Keyboard Navigation
Uses Tab key to navigate to button, then Enter to click

This multi-strategy approach ensures pop-ups are reliably dismissed regardless of browser state or website design.

## Example Test

```python
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL

def test_login_and_add_to_cart(driver):
    """Test login and add item to cart"""
    # Navigate and login
    login_page = LoginPage(driver)
    login_page.open_url(BASE_URL)
    login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)
    
    # Add item to cart
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(1)
    
    # Verify cart count
    assert inventory_page.get_cart_count() == 1
```

## Troubleshooting

### Test Fails with "Element Not Found"
- Check if element locator is still valid (may have changed in app update)
- Review logs in `reports/` for healing attempts
- Verify element is visible (not hidden by CSS display: none)
- Check if pop-up is blocking element interaction

### Test Hangs at Login
- Browser pop-up is not being dismissed automatically
- Check Chrome is not prompting for password save
- Review browser console for JavaScript errors
- Try running in headless mode: `HEADLESS=True`

### "ModuleNotFoundError" When Running Tests
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check that all `__init__.py` files exist in packages

### Screenshot Not Captured on Failure
- Verify `reports/screenshots/` directory exists
- Check file permissions for write access
- Review conftest.py screenshot fixture configuration

## CI/CD Integration

The project includes GitHub Actions workflow for automated testing:

```yaml
# .github/workflows/ui-tests.yml
- Runs on every push and PR
- Tests on Chrome in headless mode
- Generates test reports
- Uploads screenshots on failure
```

Run locally to match CI behavior:
```bash
HEADLESS=True pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Commit: `git commit -m "Add feature: description"`
6. Push: `git push origin feature/my-feature`
7. Submit a Pull Request

## Performance Tips

- Use headless mode for faster execution: `HEADLESS=True`
- Reduce explicit wait timeouts for reliable apps
- Run tests in parallel with pytest-xdist: `pip install pytest-xdist && pytest -n auto`
- Use proper waits instead of `time.sleep()`

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review logs in `reports/` for debugging

## Changelog

### v2.0 - Pop-up Handling & Enhanced Logging
- Added aggressive pop-up dismissal for browser dialogs
- Implemented three-pronged pop-up handling strategy
- Added comprehensive code comments and documentation
- Improved Chrome automation detection evasion
- Enhanced logging throughout framework

### v1.0 - Initial Release
- Self-healing locator strategies
- Page object model implementation
- Basic test framework setup
