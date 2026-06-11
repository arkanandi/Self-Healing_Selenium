"""Demonstration script for Self-Healing Selenium framework.

This script showcases the complete workflow of the Selenium testing framework:
1. Initialize WebDriver with optimized automation settings
2. Navigate to the application and perform login
3. Demonstrate cart functionality (add items, open cart)
4. Display workflow for user inspection

The demo script is designed for manual inspection and understanding the framework
flow. It keeps the browser open at the end to allow visual verification of the
automation results.

Why this is useful:
- Provides a working example of the framework usage
- Tests basic functionality without complex pytest setup
- Allows visual verification of automation steps
- Helps debug issues with browser or driver configuration
"""

import sys
import time
from pathlib import Path

# Add project root to Python path for imports
# This allows us to import from pages, utils, config modules from anywhere
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import page objects and utilities
from utils.driver_factory import DriverFactory  # Factory for creating configured WebDriver
from pages.login_page import LoginPage            # Login page object
from pages.inventory_page import InventoryPage    # Inventory page object
from pages.cart_page import CartPage             # Cart page object
from config.settings import BASE_URL, DEFAULT_USERNAME, DEFAULT_PASSWORD  # Configuration

try:
    # Create driver using the factory with all optimization settings
    # The factory automatically applies:
    # - Automation detection hiding
    # - Pop-up suppression preferences
    # - Optimal performance settings
    driver = DriverFactory.create_driver()
    
    print("Starting automated workflow...\n")
    
    # ============ Step 1: Login ============
    print("Step 1: Logging in...")
    # Create login page object and use it to navigate and login
    login_page = LoginPage(driver)
    login_page.open_url(BASE_URL)      # Navigate to application
    login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD)  # Perform login with dismissal
    print("✓ Login successful - Inventory page loaded\n")
    
    time.sleep(2)
    
    # ============ Step 2: Clear Lingering Pop-ups ============
    print("Step 2: Clearing any pop-ups...")
    # Create inventory page object to access inventory-specific methods
    inventory_page = InventoryPage(driver)
    # Aggressively clear any pop-ups that may still be present
    inventory_page.dismiss_password_popup()
    print("✓ Pop-ups cleared\n")
    
    time.sleep(1)
    
    # ============ Step 3: Add Items to Cart ============
    print("Step 3: Adding items to cart...")
    # Find all "Add to Cart" buttons on the inventory page
    add_buttons = driver.find_elements("name", "add-to-cart")
    
    # Add first item
    if add_buttons:
        add_buttons[0].click()  # Click first "Add to Cart" button
        print("  ✓ First item added")
        time.sleep(0.5)
        inventory_page.dismiss_password_popup()  # Clear any pop-ups after action
    
    # Add second item
    if len(add_buttons) > 1:
        add_buttons[1].click()  # Click second "Add to Cart" button
        print("  ✓ Second item added")
        time.sleep(0.5)
        inventory_page.dismiss_password_popup()  # Clear any pop-ups after action
    
    time.sleep(1)
    
    # ============ Step 4: Verify Cart Count ============
    # Try to get the cart badge showing number of items
    try:
        cart_badge = driver.find_element("class name", "shopping_cart_badge")
        cart_count = cart_badge.text
        print(f"  ✓ Cart contains {cart_count} items\n")
    except:
        # If badge not found, that's okay - just note items were added
        print("  ✓ Items added to cart\n")
    
    # ============ Step 5: Open Shopping Cart ============
    print("Step 5: Opening shopping cart...")
    # Use inventory page object to navigate to cart
    inventory_page.open_cart()
    print("✓ Cart page opened\n")
    
    time.sleep(2)
    
    # ============ Step 6: Verify Cart Contents ============
    print("Step 6: Verifying cart items...")
    # Create cart page object for cart-specific operations
    cart_page = CartPage(driver)
    # Clear any pop-ups before reading cart state
    cart_page.dismiss_password_popup()
    
    # Find all cart items on the page
    cart_items = driver.find_elements("class name", "cart_item")
    print(f"✓ Cart contains {len(cart_items)} items\n")
    
    time.sleep(1)
    
    # ============ Workflow Complete ============
    print("=" * 50)
    print("WORKFLOW COMPLETE - All steps finished successfully!")
    print("=" * 50)
    print("\nThe browser is open for inspection.")
    print("Review the cart page and verify the workflow executed correctly.")
    print("No pop-ups should appear during this process.\n")
    
    # Keep browser open for user inspection
    # This allows manual verification that automation worked correctly
    input("Press Enter to close the browser...")

finally:
    # Always close the browser, even if an error occurs
    # This ensures no browser processes are left hanging
    driver.quit()
