from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 20

class BasePage:
    def __init__(self, driver, base_url=None, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    # Navigation
    def visit(self, path=""):
        if not self.base_url:
            raise AssertionError("base_url not set on page object")
        url = f"{self.base_url}/{path.lstrip('/')}"
        self.driver.get(url)
        return self

    # Wait helpers
    def wait(self, condition, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(condition)

    # Element helpers
    def el(self, by_locator, timeout=None):
        return self.wait(EC.presence_of_element_located(by_locator), timeout)

    def click(self, by_locator, timeout=None):
        elem = self.wait(EC.element_to_be_clickable(by_locator), timeout)
        elem.click()
        return elem

    def type(self, by_locator, text, clear=True, timeout=None):
        elem = self.el(by_locator, timeout)
        if clear:
            elem.clear()
        elem.send_keys(text)
        return elem

    def text_of(self, by_locator, timeout=None):
        return self.el(by_locator, timeout).text

    def all(self, by_locator, timeout=None):
        self.wait(EC.presence_of_all_elements_located(by_locator), timeout)
        return self.driver.find_elements(*by_locator)

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    