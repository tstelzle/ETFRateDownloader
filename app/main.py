import os
from datetime import date
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

download_dir = "/run/ETFRateDownloader/downloads"


def format_link(given_link: str):
    return given_link.replace('.', '-').replace('/', '_')


def read_links():
    links_file = open('links.txt', 'r')
    etf_links = []
    for line in links_file:
        etf_links.append(line)

    return etf_links


def accept_cookie_consent(my_driver):
    try:
        WebDriverWait(my_driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[id^=sp_message_container_')))
        iframe = my_driver.find_element_by_css_selector("iframe[id^=sp_message_iframe_")
        my_driver.switch_to.frame(iframe)
        buttons = my_driver.find_elements_by_tag_name('button')

        my_button = None
        for button in buttons:
            if button.get_attribute('title') == 'Zustimmen':
                my_button = button
        if my_button:
            my_button.click()

        my_driver.switch_to.default_content()

        return my_driver
    except NoSuchElementException:
        return my_driver
    except TimeoutException:
        return my_driver


def download_etf_data(my_driver):
    min_time = driver.find_element_by_id('minTime')
    min_time.clear()
    min_time.send_keys('1.1.2018')

    inputs = my_driver.find_elements_by_tag_name('input')
    my_input = None
    for input_tag in inputs:
        if input_tag.get_attribute('value') == 'Download':
            my_input = input_tag
    my_input.click()

    return my_driver


def create_today_dir():
    global download_dir
    today = date.today().strftime("%Y-%m-%d")
    new_download_dir = download_dir + today
    if not os.path.exists(new_download_dir):
        os.mkdir(new_download_dir)
        os.chmod(new_download_dir, 0o777)

    return new_download_dir


def delete_old_files():
    global download_dir
    for reading_file in os.listdir(download_dir):
        root, extension = os.path.splitext(reading_file)
        if extension == ".csv" or extension == ".error":
            os.remove(os.path.join(download_dir, reading_file))


if __name__ == '__main__':
    delete_old_files()

    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")

    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    links = read_links()

    for link in links:
        try:
            driver.get(link)
            driver = accept_cookie_consent(driver)
            driver = download_etf_data(driver)
            print(datetime.now(), "Downloaded:", link)
        except Exception as e:
            print(datetime.now(), '- Error downloading:', link, e)
            os.mknod(os.path.join(download_dir, format_link(link) + '.error'))
            pass

    for file in os.listdir(download_dir):
        os.chmod(os.path.join(download_dir, file), 0o777)

    driver.quit()
