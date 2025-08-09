import pytest
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

WAIT_TIME = 15  # seconds
APP_PORT = 8050  # Dash default

@pytest.fixture(scope="session", autouse=True)
def start_dash_app():
    """Start the Dash app before tests and kill it after."""
    process = subprocess.Popen(["python", "app.py"])
    time.sleep(5)  # Give the app time to start
    yield
    process.terminate()

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(f"http://localhost:{APP_PORT}")
    yield driver
    driver.quit()

def wait_for_element(driver, by, value):
    return WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_text(driver, by, value, text):
    return WebDriverWait(driver, WAIT_TIME).until(
        EC.text_to_be_present_in_element((by, value), text)
    )

def test_header_present(driver):
    assert wait_for_text(driver, By.TAG_NAME, "h1", "3D Pink Morsel Sales Analysis"), "Header not found"

def test_visualization_present(driver):
    element = wait_for_element(driver, By.ID, "sales-3d-chart")
    assert element is not None, "Visualization not found"

def test_region_picker_present(driver):
    element = wait_for_element(driver, By.ID, "region-radio")
    assert element is not None, "Region picker not found"
