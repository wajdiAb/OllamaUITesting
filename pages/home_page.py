from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    DROPDOWN = (By.CSS_SELECTOR, "button[role='combobox']")
    GEMMA3 = (By.XPATH, "//*[text()='gemma3:1b']")
    MESSAGE_INPUT = (By.NAME, "message")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    SENT_MESSAGE = (By.XPATH, "//p[text()='Hello! Can you help me with Python?']")
    RESPONSE = (By.CSS_SELECTOR, ".p-4.bg-secondary.text-secondary-foreground.rounded-r-lg.rounded-tl-lg.break-words.max-w-full.whitespace-pre-wrap")

    PROFILE_BTN_DESKTOP= (By.ID, "radix-:Rln7mjt6:")
    PROFILE_BTN_MOBILE= (By.ID, "radix-:r0:")

    SETTINGS_BTN = (By.XPATH, "//button[@class='w-full']")


    MENU_BTN = (By.XPATH, "//*[name()='path' and contains(@d,'M1.5 3C1.2')]")
    
    def open(self, url):
        self.driver.get(url)

    def select_gemma3(self):
        self.click(self.DROPDOWN)
        self.click(self.GEMMA3)

    def send_message(self, msg):
        self.type_text(self.MESSAGE_INPUT, msg, clear_first=False)
        self.click(self.SUBMIT_BTN)

    def get_sent_message(self):
        return self.get_text(self.SENT_MESSAGE)

    def is_response_displayed(self):
        return self.is_displayed(self.RESPONSE)

    def open_profile_settings(self):
        self.click(self.PROFILE_BTN_DESKTOP)
        self.click(self.SETTINGS_BTN)

    def open_profile_settings_mobile(self): 
        self.open_menu()
        self.click(self.PROFILE_BTN_MOBILE)
        self.click(self.SETTINGS_BTN)

    def open_menu(self):
        self.click(self.MENU_BTN)

    def get_title(self):
        return self.driver.title