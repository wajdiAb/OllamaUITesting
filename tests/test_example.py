import os
import sys
import unittest
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Driver_factory import get_driver
from pages.home_page import HomePage
from pages.settings_page import SettingsPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:3000")

class ExampleTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.driver.implicitly_wait(5)
        self.home = HomePage(self.driver)
        self.settings = SettingsPage(self.driver)

    def tearDown(self):
        self.driver.quit()
    
    def test_page_title(self):
        self.home.open(OLLAMA_URL)
        self.assertIn("Ollama UI", self.home.get_title())


    def test_send_message(self):
        self.home.open(OLLAMA_URL)
        self.home.select_gemma3()
        self.home.send_message("Hello! Can you help me with Python?")
        self.assertEqual(self.home.get_sent_message(), "Hello! Can you help me with Python?")
        self.assertTrue(self.home.is_response_displayed())  

    def test_change_name(self):
        self.home.open(OLLAMA_URL)
        if self.driver.get_window_size()['width'] < 768:
            self.home.open_profile_settings_mobile()
            self.settings.change_name("wajdi")
            self.home.open_menu()
            self.assertEqual(self.settings.get_name_mobile("wajdi"), "wajdi")

        else:
            self.home.open_profile_settings()
            self.settings.change_name("wajdi") 
            self.assertEqual(self.settings.get_name(), "wajdi")

if __name__ == '__main__':
    unittest.main()