from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def read_links():
    file = open('links.txt', 'r')
    etf_links = []
    for line in file:
        etf_links.append(line)

    return etf_links


def accept_cookie_consent(my_driver):
    try:
        WebDriverWait(my_driver, 5).until(EC.visibility_of_element_located((By.ID, 'sp_message_container_213940')))
        iframe = my_driver.find_element_by_xpath("//iframe[@id = 'sp_message_iframe_213940']")
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


if __name__ == '__main__':
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/run/ETFRateDownloader/downloads')
    profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")

    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    links = read_links()

    for link in links:
        print(link)
        driver.get(link)
        driver = accept_cookie_consent(driver)
        driver = download_etf_data(driver)

    driver.close()
