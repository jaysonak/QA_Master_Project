from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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
        return self.driver.find_element(*self.success_message).text