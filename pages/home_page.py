from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class HomePage(BasePage):
    DROPDOWN = (By.CSS_SELECTOR, "button[role='combobox']")
    MESSAGE_INPUT = (By.NAME, "message")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    # Assistant response bubble (kept as-is; adjust selector if UI changes)
    RESPONSE = (By.CSS_SELECTOR, ".p-4.bg-secondary.text-secondary-foreground.rounded-r-lg.rounded-tl-lg.break-words.max-w-full.whitespace-pre-wrap")

    # Note: These radix IDs are unstable; keep until better selectors are available
    PROFILE_BTN_DESKTOP= (By.ID, "radix-:Rln7mjt6:")
    PROFILE_BTN_MOBILE= (By.ID, "radix-:r0:")

    SETTINGS_BTN = (By.XPATH, "//button[@class='w-full']")

    MENU_BTN = (By.XPATH, "//*[name()='path' and contains(@d,'M1.5 3C1.2')]")
    
    def open(self, url):
        self.driver.get(url)

    def select_model(self, name: str):
        # Open the model dropdown and pick by visible text
        self.click(self.DROPDOWN)
        self.click((By.XPATH, f"//*[normalize-space()={repr(name)}]"))

    def select_gemma3(self):
        # Backward-compatible helper; prefer select_model with env MODEL_NAME
        self.select_model("gemma3:1b")

    def send_message(self, msg):
        self.type_text(self.MESSAGE_INPUT, msg, clear_first=False)
        self.click(self.SUBMIT_BTN)

    def is_message_present(self, msg: str) -> bool:
        # Try exact match on common text nodes, then fallback to contains
        exact = (By.XPATH, f"//*[self::p or self::div or self::span][normalize-space()={repr(msg)}]")
        contains = (By.XPATH, f"//*[self::p or self::div or self::span][contains(normalize-space(), {repr(msg)})]")
        try:
            return self.is_displayed(exact)
        except TimeoutException:
            try:
                return self.is_displayed(contains)
            except TimeoutException:
                return False

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
