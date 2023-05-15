import logging
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# DOWNLOAD_DIR = "/run/ETFRateDownloader/downloads"
DOWNLOAD_DIR = "./"

ERROR_FILE = "links.exception"
LOG_FILE = "etf.log"
CREDENTIALS_FILE = "credentials.txt"


def read_file(file_name: str):
    try:
        links_file = open(file_name, 'r')
    except FileNotFoundError as ex:
        logging.error(ex)
        quit(-1)
    lines = []
    for line in links_file:
        lines.append(line)

    return lines


def accept_init_popup(my_driver):
    try:
        WebDriverWait(my_driver, 5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[id^=sp_message_container_')))
        iframe = my_driver.find_element_by_css_selector("iframe[id^=sp_message_iframe_")
        my_driver.switch_to.frame(iframe)

        element = my_driver.find_element_by_xpath("//*[text()='Akzeptieren und weiter']")
        element.click()

        my_driver.switch_to.default_content()

        return my_driver
    except NoSuchElementException:
        return my_driver
    except TimeoutException:
        return my_driver


def login_to_ariva(my_driver):
    try:
        username, password = read_file(CREDENTIALS_FILE)

        my_driver.get("https://www.ariva.de/")

        accept_init_popup(my_driver)
        my_driver.get("https://www.ariva.de/user/login/")

        anmelden_button = None
        username_element = None
        input_elements = my_driver.find_elements_by_tag_name("input")
        for el in input_elements:
            if el.get_attribute("name") == "ISID":
                username_element = el
                continue
            if el.get_attribute("type") == "submit":
                anmelden_button = el
                continue

        if username_element is None:
            logging.error("Username Element Not Found.")

        pw_element = my_driver.find_element_by_id("pw")

        username_element.send_keys(username.rstrip())
        pw_element.send_keys(password.rstrip())

        anmelden_button.click()
    except Exception as e:
        logging.error(e)

    return my_driver


def download_etf_data(my_driver):
    min_time = driver.find_element_by_id('minTime')
    min_time.clear()
    min_time.send_keys('1.1.2018')

    bottom_news_letter = my_driver.find_element_by_id("bottomNewsletterHintOuter")
    try:
        if bottom_news_letter.is_displayed():
            bottom_news_letter.click()
            my_driver.find_element_by_xpath("/html/body/div[3]/div/span").click()
    except Exception as ex:
        logging.error(ex)

    inputs = my_driver.find_elements_by_tag_name('input')
    my_input = None
    for input_tag in inputs:
        if input_tag.get_attribute('value') == 'Download':
            my_input = input_tag

    my_input.click()

    return my_driver


def delete_old_files():
    global DOWNLOAD_DIR
    for reading_file in os.listdir(DOWNLOAD_DIR):
        root, extension = os.path.splitext(reading_file)
        if extension == ".csv" or extension == ".error":
            os.remove(os.path.join(DOWNLOAD_DIR, reading_file))


def append_to_file(input_file: str, input_string: str) -> None:
    with open(input_file, "a") as file_to_append:
        file_to_append.write(input_string)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename=os.path.join(DOWNLOAD_DIR, LOG_FILE), encoding="utf-8", level=logging.INFO)

    delete_old_files()

    options = Options()
    # options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", DOWNLOAD_DIR)
    profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")

    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    login_to_ariva(driver)
    links = read_file("links.txt")

    try:
        os.mknod(os.path.join(DOWNLOAD_DIR, ERROR_FILE), 0o777)
    except FileExistsError as e:
        pass

    for link in links:
        try:
            driver.get(link)
            driver = accept_init_popup(driver)
            driver = download_etf_data(driver)
            logging.info("Downloaded: {0}".format(link))
        except Exception as e:
            logging.error("Downloading {0} with {1}".format(link, e))
            append_to_file(os.path.join(DOWNLOAD_DIR, ERROR_FILE), link)
            pass

    for file in os.listdir(DOWNLOAD_DIR):
        os.chmod(os.path.join(DOWNLOAD_DIR, file), 0o777)

    driver.quit()
