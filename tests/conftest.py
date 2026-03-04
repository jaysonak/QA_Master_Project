import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def selenium_driver():
    # 1. SETUP CHROME OPTIONS FOR HEADLESS MODE
    chrome_options = Options()
    
    # These 3 lines are the "Cloud Secret Sauce" for GitHub Actions
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 2. INITIALIZE THE DRIVER
    # This automatically handles the ChromeDriver download
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 3. YIELD THE DRIVER TO THE TEST
    yield driver
    
    # 4. TEARDOWN (Runs after the test)
    driver.quit()