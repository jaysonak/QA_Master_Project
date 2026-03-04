from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        #LOCATORS: We use the IDs we created in our HTML
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-btn")
        self.error_message = (By.ID, "error-msg")

    #ACTIONS: These are the repititive functions you automate [cite: 22]
    def login(self, username, password):
        self.driver.find_element(*self.username_field).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_text(self):
        return self.driver.find_element(*self.error_message).text