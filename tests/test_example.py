
import os, sys, unittest
import time

# Ensure repo root is on sys.path (so imports work without pytest fixtures/pytest.ini)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.Driver_factory import get_driver  # your existing factory
from pages.chat_page import ChatPage

class ChatFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.base_url = os.environ.get("OLLAMA_URL", "http://localhost:3000").rstrip("/")
        cls.driver.implicitly_wait(10)  # Set a default implicit wait

    @classmethod
    def tearDownClass(cls):
        try:
            cls.driver.quit()
        except Exception:
            pass

    def test_select_model_and_send_prompt(self):
        chat = ChatPage(self.driver, self.base_url).open()

        # Select model
        chat.select_model("gemma3:1b")
        # time.sleep(5)  # wait for model selection to complete
        self.assertIn("gemma3:1b", chat.selected_model_text())

        # Send a message
        chat.send_message("write hello world!")
        chat.wait_for_any_message()
        
        # Verify the message appears
        # messages = self.driver.find_elements(*chat.ANY_MESSAGE)
        # print("Messages found:", [msg.text for msg in messages])  # Add this line for debugging
        # self.assertTrue(any("hello world" in msg.text.lower() for msg in messages), "Message not found in chat")
        # print("Messages found:", [msg.text for msg in messages])
        # print(self.driver.page_source)  # Add this to debug the HTML

if __name__ == "__main__":
    unittest.main()








# # tests/test_example.py
# import os
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# from utils.Driver_factory import get_driver

# OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:3000')  # Default to localhost if not set


# class ExampleTestCase(unittest.TestCase):
#     def setUp(self):
#         self.driver = get_driver()

#     def tearDown(self):
#         self.driver.quit()


#     def test_text_to_prompt(self):
#         self.driver.get(OLLAMA_URL)
#         wait = WebDriverWait(self.driver, 20)

#         # Step 1: Open the model dropdown
#         model_button = wait.until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "button[role='combobox']"))
#         )
#         model_button.click()
#         time.sleep(3)

#         # Step 2: Find all button options in the open dialog
#         popover_buttons = self.driver.find_elements(By.CSS_SELECTOR, "div[role='dialog'] button")

#         # Step 3: Click the correct model
#         target_model = "gemma3:1b"
#         model_option = None
#         for btn in popover_buttons:
#             if btn.text.strip() == target_model:
#                 model_option = btn
#                 break

#         self.assertIsNotNone(model_option, f"Model '{target_model}' not found in dialog!")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", model_option)
#         try:
#             model_option.click()
#         except Exception:
#             self.driver.execute_script("arguments[0].click();", model_option)

#         time.sleep(3)

#         # Optional: Verify selection
#         model_button = wait.until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "button[role='combobox']"))
#         )
#         self.assertIn(target_model, model_button.text)
#         chat_input = self.driver.find_element(By.NAME, "message")
#         chat_input.clear()
#         wait = WebDriverWait(self.driver, 10)  # מחכה עד 10 שניות
#         chat_input = wait.until(EC.presence_of_element_located((By.NAME, "message")))
#         chat_input.send_keys("wrtie hello world!")
#         time.sleep(2)
#         element = self.driver.find_element(By.CLASS_NAME, "lucide-send-horizontal")
#         element.click()
#         time.sleep(20)

# if __name__ == '__main__':
#     unittest.main()

    