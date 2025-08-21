from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ModelDialog(BasePage):
    DIALOG = (By.CSS_SELECTOR, "button[role='combobox']")
    OPTIONS = (By.XPATH, "//div[@role='dialog']//button[contains(text(),'gemma3:1b')]")

    def wait_loaded(self):
        self.el(self.DIALOG)
        return self

    def select_model(self, name: str):
        self.wait_loaded()
        buttons = self.all(self.OPTIONS)
        target = next((b for b in buttons if b.text.strip() == name), None)
        if not target:
            raise AssertionError(f"Model '{name}' not found in dialog")
        self.scroll_into_view(target)
        try:
            target.click()
        except Exception:
            self.js_click(target)
        return self
