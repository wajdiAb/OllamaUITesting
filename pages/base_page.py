from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text, clear_first=True):
        el = self.wait.until(EC.presence_of_element_located(locator))
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator)).text

    def is_displayed(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator)).is_displayed()