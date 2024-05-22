
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from helium import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
def get_webdriver_instance(browser=None):
    base_url = "https://accounts.teachmint.com/"
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-user-media-security=true")
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-usermedia-screen-capturing")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--auto-select-desktop-capture-source=Screen 1")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if browser == "headless":
        options.add_argument("--headless")
        options.add_argument("--use-system-clipboard")
        options.add_argument("--window-size=1920x1080")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    options.set_capability('goog:chromeOptions', caps)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    driver.maximize_window()
    driver.get(base_url)
    set_driver(driver)
    return driver

def enter_phone_number_otp(driver, creds):
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys(creds[0])
    time.sleep(1)
    print(f"entered user phone number {creds[0]}")
    driver.find_element(By.ID, "send-otp-btn-id").click()
    WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
    time.sleep(1)
    _input_otp_field = "//input[@data-group-idx='{}']"
    for i, otp in enumerate(creds[1]):
        otp_field = _input_otp_field.format(str(i))
        write(otp, into=S(otp_field))
        print(f"entered otp {creds[1]}")
    time.sleep(1)
    driver.find_element(By.ID, "submit-otp-btn-id").click()
    time.sleep(2)
    # Adding explicit wait for the element
    try:
        skip_button = WebDriverWait(driver, timeout=30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@onclick='onSkipPassCreationClick()']"))
        )
        skip_button.click()
    except TimeoutException:
        print("Skip button not found or not clickable")
    WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
    time.sleep(1)
    print("successfully entered user phone number and otp")

def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
    driver = get_webdriver_instance()
    WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
    time.sleep(1)
    enter_phone_number_otp(driver, admin_credentials)
    user_name = f"//div[@class='profile-user-name']/..//div[text()='{account_name}']"
    WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, user_name)))
    driver.find_element(By.XPATH, user_name).click()
    dashboard_xpath = "//a[text()='Dashboard']"
    WebDriverWait(driver, timeout=100).until(EC.presence_of_element_located((By.XPATH, dashboard_xpath)))
    return driver

def navigate_to_certificates(driver):
    certificates_xpath = "//a[text()='Certificates']"
    WebDriverWait(driver,timeout=30).until(EC.element_to_be_clickable((By.XPATH, certificates_xpath)))
    driver.find_element(By.XPATH, certificates_xpath).click()

def select_certificate_type(driver):
    certificate_type_xpath = "//select[@id='certificate-type']"
    select = Select(driver.find_element(By.XPATH, certificate_type_xpath))
    select.select_by_visible_text('School Leaving Certificate')

def search_and_select_student(driver):
    search_box_xpath = "//input[@id='student-search']"
    driver.find_element(By.XPATH, search_box_xpath).send_keys('Sam')
    student_result_xpath = "//div[@class='student-result' and text()='Sam']"
    WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, student_result_xpath)))
    driver.find_element(By.XPATH, student_result_xpath).click()

def generate_certificate(driver):
    generate_button_xpath = "//button[text()='Generate']"
    driver.find_element(By.XPATH, generate_button_xpath).click()
    remarks_xpath = "//textarea[@id='remarks']"
    driver.find_element(By.XPATH, remarks_xpath).send_keys('All criteria met')
    download_button_xpath = "//button[text()='Download']"
    driver.find_element(By.XPATH, download_button_xpath).click()

def validate_certificate_history(driver):
    history_tab_xpath = "//a[text()='History']"
    driver.find_element(By.XPATH, history_tab_xpath).click()
    history_entry_xpath = "//div[text()='Sam - School Leaving Certificate']"
    assert WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, history_entry_xpath)))

def main():
    driver = login()
    navigate_to_certificates(driver)
    select_certificate_type(driver)
    search_and_select_student(driver)
    generate_certificate(driver)
    validate_certificate_history(driver)
    driver.quit()

if __name__ == "__main__":
    main()
