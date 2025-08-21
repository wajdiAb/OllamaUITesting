from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.components.model_dialog import ModelDialog

class ChatPage(BasePage):
    # TIP: if you can, prefer data-testid in your app and switch to them here.
    MODEL_COMBOBOX = (By.CSS_SELECTOR, "button[role='combobox']")
    CHAT_INPUT     = (By.NAME, "message")
    SEND_BUTTON    = (By.CSS_SELECTOR, ".lucide-send-horizontal")
    # Consider relaxing this selector; it's very specific to the class list.
    ANY_MESSAGE    = (By.CSS_SELECTOR, ".p-4.bg-secondary.text-secondary-foreground.rounded-r-lg.rounded-tl-lg.break-words.max-w-full.whitespace-pre-wrap")

    def open(self):
        # Navigate then wait for page to be ready (combobox clickable, input visible)
        self.visit("/")
        self.wait(EC.element_to_be_clickable(self.MODEL_COMBOBOX), timeout=self.timeout)
        self.wait(EC.visibility_of_element_located(self.CHAT_INPUT), timeout=self.timeout)
        return self

    def open_model_dialog(self):
        # Wait for clickability (prevents stale/covered clicks), then click
        self.wait(EC.element_to_be_clickable(self.MODEL_COMBOBOX), timeout=self.timeout)
        self.click(self.MODEL_COMBOBOX)
        # Ensure dialog is up before returning the component
        return ModelDialog(self.driver, self.base_url, self.timeout).wait_loaded()

    def selected_model_text(self):
        # Ensure the button is visible before reading its text
        self.wait(EC.visibility_of_element_located(self.MODEL_COMBOBOX), timeout=self.timeout)
        return self.text_of(self.MODEL_COMBOBOX)

    def select_model(self, model_name: str):
        # Open, select in dialog, then wait until the selection reflects on the combobox
        dialog = self.open_model_dialog()
        dialog.select_model(model_name)

        # Wait until combobox text reflects the selected model
        base = model_name.split(":")[0].lower()
        def _model_reflected(_):
            try:
                return base in self.selected_model_text().lower()
            except Exception:
                return False

        self.wait(_model_reflected, timeout=30)
        return self

    def send_message(self, text: str):
        # Wait for input visible, type; wait for send button clickable, click
        self.wait(EC.visibility_of_element_located(self.CHAT_INPUT), timeout=self.timeout)
        self.type(self.CHAT_INPUT, text)

        # Capture current message count to wait for a NEW one after sending
        try:
            start_count = len(self.driver.find_elements(*self.ANY_MESSAGE))
        except Exception:
            start_count = 0

        self.wait(EC.element_to_be_clickable(self.SEND_BUTTON), timeout=self.timeout)
        self.click(self.SEND_BUTTON)

        # Wait until a new message appears (handles async/respond times)
        def _new_message_arrived(_):
            try:
                return len(self.driver.find_elements(*self.ANY_MESSAGE)) > start_count
            except Exception:
                return False

        self.wait(_new_message_arrived, timeout=60)
        return self

    def wait_for_any_message(self, timeout=20):
        self.wait(EC.presence_of_element_located(self.ANY_MESSAGE), timeout=timeout)
        return self

    def last_message_text(self):
        # Ensure at least one message exists, then read the last
        self.wait_for_any_message(timeout=self.timeout)
        elems = self.all(self.ANY_MESSAGE)
        return elems[-1].text if elems else ""
