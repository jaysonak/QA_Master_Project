import pytest
from playwright.sync_api import expect

def test_playwright_transfer(page):
    # 1. Navigate
    page.goto("http://127.0.0.1:5000")
    
    # 2. Login - Using CSS selectors (#id) which are faster for the engine
    page.locator("#username").fill("qa_user")
    page.locator("#password").fill("password123")
    page.locator("#login-btn").click()
    
    # 3. Perform Transfer
    # We use 'wait_for_selector' to ensure the page finished loading
    page.wait_for_selector("#amount")
    page.locator("#amount").fill("250")
    page.select_option("#currency", "GHS")
    page.locator("#transfer-btn").click()
    
    # 4. ASSERT
    success_message = page.locator("#success-msg")
    expect(success_message).to_be_visible(timeout=10000) # Give it 10s
    expect(success_message).to_contain_text("GHS")