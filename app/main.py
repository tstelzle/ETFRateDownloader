import logging
import os

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

DOWNLOAD_DIR = "/run/ETFRateDownloader/downloads"

ERROR_FILE = "links.exception"
LOG_FILE = "etf.log"
API_URL = "https://www.ariva.de/quote/historic/historic.csv?secu={secu_id}&boerse_id={boerse_id}&clean_split=1&clean_payout=1&clean_bezug=1&min_time=01.01.2018&max_time=07.11.2023&trenner=%3B&go=Download"
PRIORITIZED_BOERSE_IDS = [45]


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
        iframe = my_driver.find_element(By.CSS_SELECTOR, "iframe[id^=sp_message_iframe_")
        my_driver.switch_to.frame(iframe)

        element = my_driver.find_element(By.XPATH, "//*[text()='Akzeptieren und weiter']")
        element.click()

        my_driver.switch_to.default_content()

        return my_driver
    except NoSuchElementException:
        return my_driver
    except TimeoutException:
        return my_driver


def download_etf_data_from_api(secu_id: int, boerse_id: int):
    url = API_URL.format(secu_id=secu_id, boerse_id=boerse_id)
    response = requests.get(url)
    if response.status_code == 200:
        filename = response.headers.get("Content-Disposition").split("=")[1]
        filename_with_directory = f"{DOWNLOAD_DIR}/{filename}"
        with open(filename_with_directory, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download file: {response.status_code}")


def delete_old_files():
    global DOWNLOAD_DIR
    for reading_file in os.listdir(DOWNLOAD_DIR):
        root, extension = os.path.splitext(reading_file)
        if extension == ".csv" or extension == ".error":
            os.remove(os.path.join(DOWNLOAD_DIR, reading_file))


def append_to_file(input_file: str, input_string: str) -> None:
    with open(input_file, "a") as file_to_append:
        file_to_append.write(input_string)


def get_secu_id(my_driver) -> int:
    a_tag = my_driver.find_element(By.XPATH, '//a[@aria-label="TODO"]')
    if a_tag is not None:
        return a_tag.get_attribute("href").split("=")[1]

    return -1


def get_boerse_id(my_driver) -> int:
    boerse_ids = []
    selected_id = -1
    select = Select(my_driver.find_element(By.XPATH, '//select[@name="boerse_id"]'))
    for option in select.options:
        current_id = int(option.get_attribute("value"))
        boerse_ids.append(current_id)
        selected = option.get_attribute("selected")
        if selected is not None:
            selected_id = current_id

    common_boerse_ids = [element for element in PRIORITIZED_BOERSE_IDS if element in boerse_ids]

    if common_boerse_ids:
        return common_boerse_ids[0]
    else:
        return selected_id


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename=os.path.join(DOWNLOAD_DIR, LOG_FILE),
                        encoding="utf-8", level=logging.INFO)

    delete_old_files()

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    links = read_file("links.txt")

    try:
        os.mknod(os.path.join(DOWNLOAD_DIR, ERROR_FILE), 0o777)
    except FileExistsError as e:
        pass

    for link in links:
        try:
            driver.get(link)
            driver = accept_init_popup(driver)
            secu_id = get_secu_id(driver)
            if secu_id == -1:
                raise Exception("Secu ID Not Found.")
            boerse_id = get_boerse_id(driver)
            download_etf_data_from_api(secu_id, boerse_id)
            logging.info("Downloaded: {0}".format(link))
        except Exception as e:
            logging.error("Downloading {0} with {1}".format(link, e))
            append_to_file(os.path.join(DOWNLOAD_DIR, ERROR_FILE), link)
            pass

    for file in os.listdir(DOWNLOAD_DIR):
        os.chmod(os.path.join(DOWNLOAD_DIR, file), 0o777)

    driver.quit()
