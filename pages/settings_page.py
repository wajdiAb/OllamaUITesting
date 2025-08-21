from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SettingsPage(BasePage):
    NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter your name']")
    CHANGE_BTN = (By.XPATH, "//button[normalize-space()='Change name']")
    NAME_TEXT = (By.CSS_SELECTOR, "button[type='button'] div.text-xs p")
    NAME_TEXT_MOBILE = lambda self, name: (By.XPATH, f"//div[@data-collapsed='false']//div//button[@type='button']//div//p[contains(text(),'{name}')]")

    def change_name(self, name):
        el = self.driver.find_element(*self.NAME_INPUT)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
        el.send_keys(name)
        self.click(self.CHANGE_BTN)

    def get_name(self):
        return self.driver.find_element(*self.NAME_TEXT).text
    
    def get_name_mobile(self, expected_name):
        el = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.NAME_TEXT_MOBILE(expected_name))
        )
        # Wait until the element's text equals expected_name
        WebDriverWait(self.driver, 10).until(
            lambda driver: el.text.strip() == expected_name
        )
        return el.text.strip()