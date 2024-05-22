from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
    return driver

def enter_phone_number_otp(driver, creds):
    try:
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(creds[0])
        time.sleep(1)
        print(f"Entered user phone number {creds[0]}")
        driver.find_element(By.ID, "send-otp-btn-id").click()
        WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "loader")))
        WebDriverWait(driver, timeout=30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
        time.sleep(1)
        _input_otp_field = "//input[@data-group-idx='{}']"
        for i, otp in enumerate(creds[1]):
            otp_field = _input_otp_field.format(str(i))
            driver.find_element(By.XPATH, otp_field).send_keys(otp)
        time.sleep(1)
        driver.find_element(By.ID, "submit-otp-btn-id").click()
        time.sleep(2)
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
        print("Successfully entered user phone number and OTP")
    except NoSuchElementException as e:
        print(f"An element was not found during OTP entry: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred during OTP entry: {e}")
    except Exception as e:
        print(f"An error occurred during OTP entry: {e}")

def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
    driver = None
    try:
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
        print("Login successful")
        return driver
    except TimeoutException as e:
        print(f"Timeout occurred during login: {e}")
    except NoSuchElementException as e:
        print(f"An element was not found during login: {e}")
    except Exception as e:
        print(f"An error occurred during login: {e}")
        if driver:
            driver.quit()

def navigate_to_certificates(driver):
    try:
        certificates_xpath = "span.icon-administrator_filled.krayon__Icon-module__eRVVq.krayon__Icon-module__szG-X.Sidebar_featureIcon__2JTL4[data-qa='icon-administrator'][data-size='xx_s'][data-type='primary']"
        WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, certificates_xpath)))
        driver.find_element(By.CSS_SELECTOR, certificates_xpath).click()
        print("Navigated to Certificates")
    except NoSuchElementException as e:
        print(f"An element was not found while navigating to certificates: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred while navigating to certificates: {e}")
    except Exception as e:
        print(f"An error occurred while navigating to certificates: {e}")

def select_certificate_type(driver):
    try:
        certificate_type_xpath = "//select[@id='certificate-type']"
        select = Select(driver.find_element(By.XPATH, certificate_type_xpath))
        select.select_by_visible_text('School Leaving Certificate')
        print("Selected certificate type: School Leaving Certificate")
    except NoSuchElementException as e:
        print(f"An element was not found while selecting certificate type: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred while selecting certificate type: {e}")
    except Exception as e:
        print(f"An error occurred while selecting certificate type: {e}")

def search_and_select_student(driver):
    try:
        search_box_xpath = "//input[@id='student-search']"
        driver.find_element(By.XPATH, search_box_xpath).send_keys('Sam')
        student_result_xpath = "//div[@class='student-result' and text()='Sam']"
        WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, student_result_xpath)))
        driver.find_element(By.XPATH, student_result_xpath).click()
        print("Searched and selected student: Sam")
    except NoSuchElementException as e:
        print(f"An element was not found while searching and selecting student: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred while searching and selecting student: {e}")
    except Exception as e:
        print(f"An error occurred while searching and selecting student: {e}")

def generate_certificate(driver):
    try:
        generate_button_xpath = "//button[text()='Generate']"
        driver.find_element(By.XPATH, generate_button_xpath).click()
        remarks_xpath = "//textarea[@id='remarks']"
        driver.find_element(By.XPATH, remarks_xpath).send_keys('All criteria met')
        download_button_xpath = "//button[text()='Download']"
        driver.find_element(By.XPATH, download_button_xpath).click()
        print("Certificate generated and downloaded")
    except NoSuchElementException as e:
        print(f"An element was not found while generating certificate: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred while generating certificate: {e}")
    except Exception as e:
        print(f"An error occurred while generating certificate: {e}")

def validate_certificate_history(driver):
    try:
        history_tab_xpath = "//a[text()='History']"
        driver.find_element(By.XPATH, history_tab_xpath).click()
        history_entry_xpath = "//div[text()='Sam - School Leaving Certificate']"
        assert WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, history_entry_xpath)))
        print("Validated certificate history for Sam - School Leaving Certificate")
    except NoSuchElementException as e:
        print(f"An element was not found while validating certificate history: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred while validating certificate history: {e}")
    except Exception as e:
        print(f"An error occurred while validating certificate history: {e}")

def click_administrator_icon(driver):
    try:
        wait = WebDriverWait(driver, timeout=10)
        icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-administrator_filled")))
        icon.click()
        print("Icon clicked successfully.")
    except NoSuchElementException as e:
        print(f"An element was not found while clicking the administrator icon: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred while clicking the administrator icon: {e}")
    except Exception as e:
        print(f"An error occurred while clicking the administrator icon: {e}")

def main():
    driver = None
    try:
        driver = login()
        if driver is None:
            print("Login failed, exiting...")
            return

        navigate_to_certificates(driver)
        select_certificate_type(driver)
        search_and_select_student(driver)
        generate_certificate(driver)
        validate_certificate_shistory(driver)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
