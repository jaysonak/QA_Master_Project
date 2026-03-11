import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime

@pytest.fixture(scope="function")
def selenium_driver():
    # 1. SETUP CHROME OPTIONS FOR HEADLESS MODE
    chrome_options = Options()
    
    # These 3 lines are the "Cloud Secret Sauce" for GitHub Actions
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ADD THIS LINE: Force a standard desktop resolution
    chrome_options.add_argument("--window-size=1920,1080")
    
    # 2. INITIALIZE THE DRIVER
    # This automatically handles the ChromeDriver download
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 3. YIELD THE DRIVER TO THE TEST
    yield driver
    
    # 4. TEARDOWN (Runs after the test)
    driver.quit()

    # Capture screenshot
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        # execute all other hooks to obtain the report object
        outcome = yield
        rep = outcome.get_result()

        # we only look at actual test failures (not setup/teardown)
        if rep.when == "call" and rep.failed:
            mode = "a" if os.path.exists("failures") else "w"
            # Create a failures folder if it doesn't exist
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            # Find the driver fixture in the test
            driver = item.funcargs.get("selenium_driver")
            if driver:
                screenshot_name = f"screenshots/fail_{item.name}_{datetime.now().strftime('%H%M%S')}.png"
                driver.save_screenshot(screenshot_name)