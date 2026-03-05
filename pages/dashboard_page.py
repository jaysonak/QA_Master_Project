from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.amount_field = (By.ID, "amount")
        self.currency_dropdown = (By.ID, "currency")
        self.transfer_button = (By.ID, "transfer-btn")
        self.success_message = (By.ID, "success-msg")

    def perform_transfer(self, amount, currency_code):
        self.driver.find_element(*self.amount_field).send_keys(amount)
        # Select from dropdown [cite: 14]
        dropdown = Select(self.driver.find_element(*self.currency_dropdown))
        dropdown.select_by_value(currency_code)
        self.driver.find_element(*self.transfer_button).click()

    def get_success_text(self):
        # Tell Selenium to wait up to 5 seconds for the element to become visible
        wait = WebDriverWait(self.driver, 5)
        element = wait.until(EC.visibility_of_element_located(self.success_message))
        
        return element.text