import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

def get_browser():
    """Pick browser type from env (default: chrome)."""
    return os.getenv("BROWSER", "chrome").lower()

def get_resolution():
    """Parse resolution string into (width, height)."""
    res_str = os.getenv("RESOLUTION", "1280x720")
    try:
        width, height = res_str.lower().split("x")
        return int(width), int(height)
    except Exception:
        return 1280, 720

@pytest.fixture(scope="session")
def base_url():
    """Provide base URL for tests."""
    return os.getenv("BASE_URL", "http://localhost:3000")

@pytest.fixture(scope="session")
def driver():
    """Provide a Selenium WebDriver based on env settings."""
    browser = get_browser()
    resolution = get_resolution()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # remove if you want to see browser
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.set_window_size(*resolution)

    yield driver
    driver.quit()
