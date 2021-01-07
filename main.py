from selenium import webdriver
from selenium.webdriver.firefox.options import Options

if __name__ == '__main__':
    options = Options()
    # options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/home/tarek/Desktop/ETFRateDownloader')
    profile.set_preference("browser.helperApps.neverAsk.openFile", "text/csv,application/vnd.ms-excel")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/vnd.ms-excel")
    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    link = "https://www.ariva.de/ishares_core_msci_world_ucits_etf-fonds/historische_kurse"

    driver.get(link)

    # TODO There are apparently two iframes select the write one, better than just by list
    iframe = driver.find_elements_by_xpath('//iframe')
    driver.switch_to.frame(iframe[1])
    buttons = driver.find_elements_by_tag_name('button')

    my_button = None
    for button in buttons:
        if button.get_attribute('title') == 'Zustimmen':
            my_button = button
    if my_button:
        my_button.click()

    driver.switch_to.default_content()

    min_time = driver.find_element_by_id('minTime')
    min_time.clear()
    min_time.send_keys('1.1.2018')

    inputs = driver.find_elements_by_tag_name('input')
    my_input = None
    for input_tag in inputs:
        if input_tag.get_attribute('value') == 'Download':
            my_input = input_tag
    my_input.click()
