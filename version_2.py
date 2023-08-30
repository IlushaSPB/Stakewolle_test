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
def get_page_main(driver, number):
    baseurl = fr'https://www.mintscan.io/akash/blocks/{number}'
    driver.get(baseurl)
    driver.execute_script('window.scroll(0,document.body.scrollHeight)')


# получить страницу по хешу
def get_page_from_hash(driver, hash):
    baseurl = fr'https://www.mintscan.io/akash/transactions/{hash}'
    driver.get(baseurl)
    driver.execute_script('window.scroll(0,document.body.scrollHeight)')


# получить хеш из элемента
def get_hash(element):
    desired_value = None
    parts = element[0].split()
    desired_value = parts[3]
    return desired_value


# собрать и вывести детали транзакции в словарь
def tx_detail(soup):
    values = {}
    for n in range(5, 12):
        selectors = soup.select(
            fr'#content-root > div:nth-child(2) > div > section:nth-child(1) > div > div > div.contents.s-AlA33PZP3RDs > div.root.s-B5fp-zeMUDH- > div:nth-child({n})')

        if n == 5:
            chain_id_div = selectors[0].find('div', class_='typo', string='Chain ID')
            chain_id_value = chain_id_div.find_next('div', class_='typo s-UR0RXdEDmUvA').get_text().strip()
            values['Chain ID'] = chain_id_value

        elif n == 6:
            txhash_div = selectors[0].find('div', class_='typo', string='TxHash')
            txhash_value = txhash_div.find_next('div', class_='typo s-UR0RXdEDmUvA').get_text().strip()
            values['TxHash'] = txhash_value

        elif n == 7:
            height_div = selectors[0].find('div', class_='typo', string='Height')
            height_value = height_div.find_next('a').get_text().strip()
            values['Height'] = height_value

        elif n == 8:
            time_div = selectors[0].find('div', class_='typo', string='Time')
            time_value = time_div.find_next('div', class_='typo').get_text().strip()
            values['Time '] = time_value

        # have some problem with Gas Used / Wanted
        # elif n == 9:
        #     gas_used_element = selectors[0].find('div', text='Gas Used / Wanted')

        elif n == 11:
            memo_div = selectors[0].find('div', class_='typo', string='Memo')
            memo_value = memo_div.find_next('div', class_='typo').get_text().strip()
            values['Memo '] = memo_value

    print(values)


# перебрать значения хешей и собрать информацию
def get_content_from_hash(hashes):
    driver = init_driver()

    for hash in hashes:
        print('\n Finding information in hash: ', hash, )
        get_page_from_hash(driver, hash)
        time.sleep(1)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        tx_detail(soup)

    close_driver(driver)


# собрать информацию со страницы блока, используя номер блока
def get_content(number):
    print('\n Finding transactions in block: ', number, '...')

    driver = init_driver()
    get_page_main(driver, number)
    time.sleep(1)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    hashes = []
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
        hashes.append(get_hash(values))
    print(hashes)

    close_driver(driver)

    get_content_from_hash(hashes)


# для теста
get_content(11260637)
