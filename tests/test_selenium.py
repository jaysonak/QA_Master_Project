import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# Notice we pass 'selenium_driver' into the function. 
# Pytest automatically finds this fixture in your conftest.py, 
# opens the browser, and hands it to this test!

def test_successful_login(selenium_driver):
    """Test that a user can log in with valid credentials"""

    #1. ARRANGE: Load the Login Page Object
    login_page = LoginPage(selenium_driver)

    # 2. ACT: Use the action we defined in the POM
    login_page.login("qa_user", "password123")

    # 3. ASSERT: Prove it worked by checking the URL
    assert "dashboard" in selenium_driver.current_url


def test_invalid_login(selenium_driver):
    """Test that bad credentials throw an error"""

    login_page = LoginPage(selenium_driver)
    login_page.login("wrong_user", "bad_password")

    #Prove the error message appears
    error_text = login_page.get_error_text()
    assert "Invalid Credentials" in error_text


def test_currency_transfer(selenium_driver):
    """Test the Fintech transfer form"""
    
    # Prerequisite: We must log in first to see the dashboard
    login_page = LoginPage(selenium_driver)
    login_page = login_page.login("qa_user", "password123")

    # 1. ARRANGE: Load the Dashboard Page Object
    dashboard_page = DashboardPage(selenium_driver)

    # 2. ACT: Perform a $100 transfer to Euros (EUR)
    dashboard_page.perform_transfer("100", "EUR")

    # 3. ASSERT: Verify the success message on the UI
    success_text = dashboard_page.get_success_text()
    assert "Successfully transferred" in success_text
    assert "EUR" in success_text


    