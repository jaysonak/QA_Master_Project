import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# The @pytest.fixture decorator tells Pytest this is a setup/teardown function.
# scope="function" means it will open a fresh browser for EVERY individual test.
@pytest.fixture(scope="function")
def selenium_driver():
    # ==========================================
    # 1. SETUP (Runs BEFORE the test)
    # ==========================================
    
    # Automatically downloads and uses the correct ChromeDriver for your machine
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Tell Selenium to wait up to 5 seconds if an element isn't instantly visible
    driver.implicitly_wait(5)
    driver.maximize_window()

    # Navigate to your local Flask app
    driver.get("http://127.0.0.1:5000")

def get_driver():
    chrome_options = Options()
    # These three lines are the "Cloud Secret Sauce"
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

    # ==========================================
    # 2. THE HANDOFF
    # ==========================================
    
    # 'yield' is a special Python keyword. It hands the 'driver' over to your test,
    # pauses this function, and waits for your test to finish passing or failing.
    yield driver 
    
    # ==========================================
    # 3. TEARDOWN (Runs AFTER the test)
    # ==========================================
    
    # Close the browser completely so you don't have 100 zombie windows open
    driver.quit()