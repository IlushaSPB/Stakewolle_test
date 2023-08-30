import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# иницилизация драйвера
def init_driver():
    CHROME_BIN_LOCATION = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
    CHROME_DRIVER_LOCATION = r'D:\Питон\chromedriver.exe'
    USER_DATA_DIR = r'C:\environments\selenium'

    options = Options()
    service = Service(CHROME_DRIVER_LOCATION)

    options.add_argument(f'user-data-dir={USER_DATA_DIR}')
    options.add_argument('--disable-popup-blocking')
    options.binary_location = CHROME_BIN_LOCATION

    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()

    return driver


# закрыть страницу
def close_driver(driver):
    driver.close()


# получить страницу блока
def get_page(driver, number):
    baseurl = fr'https://www.mintscan.io/akash/blocks/{number}'
    driver.get(baseurl)
    driver.execute_script('window.scroll(0,document.body.scrollHeight)')


# собрать информацию со страницы блока, используя номер блока
def get_content(number):
    print('\n Finding transactions in block: ', number, '...')

    driver = init_driver()
    get_page(driver, number)
    time.sleep(1)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    count = soup.select(
        '#content-root > section > div > div:nth-child(2) > div > div:nth-child(2) > div.contents.s-AlA33PZP3RDs > div:nth-child(1) > div:nth-child(6) > div > div:nth-child(2) > div')
    tx_count = int(count[0].text)
    if tx_count == 0:
        print("No transactions in block: ", number)
        return 0

    for i in range(1, tx_count + 1):
        common_selector = fr'#content-root > section > div > div:nth-child(2) > div > div:nth-child(3) > div.contents.s-AlA33PZP3RDs > div > div:nth-child({i}) > div > div'
        elements = soup.select(common_selector)
        values = [element.get_text() for element in elements]
        print(values[0])

    close_driver(driver)


# для теста
get_content(11260637)
get_content(11260638)
get_content(11260639)
