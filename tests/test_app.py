from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest
import time

@pytest.fixture
def driver():
    # Requirement: Use Headless Chrome for Jenkins/EC2 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    # Update this URL to your EC2 IP and port 
    driver.get("http://13.60.224.71:8888") 
    yield driver
    driver.quit()

# --- 15 Automated Test Cases [cite: 51] ---

def test_title(driver):
    assert "bezkoder" in driver.title.lower()

def test_url(driver):
    assert "8888" in driver.current_url

def test_navbar_brand_exists(driver):
    brand = driver.find_element(By.CLASS_NAME, "navbar-brand")
    assert brand.is_displayed()

def test_add_button_visibility(driver):
    add_btn = driver.find_element(By.LINK_PATH, "//a[contains(text(),'Add')]")
    assert add_btn.is_displayed()

def test_search_bar_exists(driver):
    search = driver.find_element(By.ATTRIBUTE, "placeholder", "Search by title")
    assert search.is_displayed()

def test_navigation_to_add(driver):
    driver.find_element(By.LINK_TEXT, "Add").click()
    assert "/add" in driver.current_url

def test_form_labels_title(driver):
    driver.get("http://13.60.224.71:8888/add")
    label = driver.find_element(By.XPATH, "//label[text()='Title']")
    assert label.is_displayed()

def test_form_labels_desc(driver):
    driver.get("http://13.60.224.71:8888/add")
    label = driver.find_element(By.XPATH, "//label[text()='Description']")
    assert label.is_displayed()

def test_submit_button_exists(driver):
    driver.get("http://13.60.224.71:8888/add")
    btn = driver.find_element(By.CLASS_NAME, "btn-success")
    assert btn.text == "Submit"

def test_empty_search_results(driver):
    search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search by title']")
    search_input.send_keys("NonExistentTutorial")
    driver.find_element(By.XPATH, "//button[text()='Search']").click()
    time.sleep(1)
    results = driver.find_elements(By.CLASS_NAME, "list-group-item")
    assert len(results) == 0

def test_main_page_heading(driver):
    heading = driver.find_element(By.TAG_NAME, "h4")
    assert "Tutorials List" in heading.text

def test_remove_all_button(driver):
    btn = driver.find_element(By.CLASS_NAME, "m-3.btn.btn-sm.btn-danger")
    assert "Remove All" in btn.text

def test_footer_or_container_width(driver):
    container = driver.find_element(By.CLASS_NAME, "container")
    assert container.size['width'] > 0

def test_add_tutorial_placeholder(driver):
    driver.get("http://13.60.224.71:8888/add")
    title_input = driver.find_element(By.ID, "title")
    assert title_input.is_enabled()

def test_back_to_list_from_add(driver):
    driver.get("http://13.60.224.71:8888/add")
    driver.find_element(By.LINK_TEXT, "Tutorials").click()
    assert "/tutorials" in driver.current_url or driver.current_url.endswith("8888/")
