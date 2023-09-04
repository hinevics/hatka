import re
from bs4 import BeautifulSoup
import logging
import colorlog
import pickle
import pathlib
import multiprocessing

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

from config import PATH_SAVE, EXECUTABLE_PATH

# format logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
color_format = '%(log_color)s' + log_format
formatter_console = colorlog.ColoredFormatter(color_format)
formatter_file = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# all logs
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter_console)
logger.addHandler(console_handler)

URL_PAGE = r'https://realt.by/belarus/rent/flat-for-long/?page={page_number}'
URL_BASE = r'https://realt.by'
NUMBER_PAGES = 125


def find_number(href: str):
    res = href['aria-label']
    res = re.search(pattern=r'\№(?P<number>\d+)', string=res)
    return res.group('number')


def get_page(driver, url: str, number: int) -> str:
    url = url.format(number=number)
    driver.get(r'https://realt.by/rent/flat-for-long/?page=1')
    return driver


def get_driver():
    options = FirefoxOptions()
    options.add_argument('--headless')
    firefox_service = Service(EXECUTABLE_PATH)
    driver = webdriver.Firefox(
        service=firefox_service,
        options=options
    )
    return driver


def parser(page_number):
    driver = get_driver()
    driver.get(
        URL_PAGE.format(page_number=page_number)
    )

    data = {}
    logger.info(f'parsing page {page_number}: Start!')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Забираю объявления
    div_elements_with_data_index = soup.find_all('div', {'data-index': True})

    for rent in div_elements_with_data_index:

        # Ссылка на объявление
        href = rent.find_all('a')[0]

        # Номер объявления
        number = find_number(href)

        logger.debug(f'page: {page_number}. parsing flat {number}: Start!')

        new_url = URL_BASE + href['href']
        driver.get(new_url)
        soup_rent = BeautifulSoup(driver.page_source, 'html.parser')

        if str(number) not in data.keys():
            rent = {
                'href': new_url
            }

            # Title
            title_list = soup_rent.select('h1.order-1')
            title = title_list[0].text if title_list else None
            logger.debug(f'page: {page_number}. received: title: {title}')
            rent['title'] = title

            # Text
            text_list = soup_rent.select(
                'section.bg-white:nth-child(3) > div:nth-child(2)')
            text = ' '.join([i.text for i in text_list]) if text_list else ''
            logger.debug(f'page: {page_number}. received: text: {text[:20]}')
            rent['text'] = text

            # Note
            note_list = soup_rent.select(
                'section.bg-white:nth-child(6) > div:nth-child(2)')
            note = ' '.join([i.text for i in note_list]) if note_list else ''
            logger.debug(f'page: {page_number}. received: note: {note[:20]}')
            rent['note'] = note

            # Adres
            adres_list = soup_rent.select(r'li.md\:w-auto')
            adres = adres_list[0].text if adres_list else None
            logger.debug(f'page: {page_number}. received: adres: {adres}')
            rent['adres'] = adres

            # Price
            price_list = soup_rent.select(
                r'.md\:items-center > div:nth-child(1) > h2:nth-child(1)')
            price = price_list[0].text if price_list else None
            logger.debug(f'page: {page_number}. received: price: {price}')
            rent['price'] = price

            # Other Params
            params = {}
            selected_params = soup_rent.select(r'ul.w-full:nth-child(2)')
            li_params = selected_params[0].find_all('li')
            for li in li_params:
                name_params = li.find_all('span')[0].text
                value_params = li.find_all('p')[0].text
                params[name_params] = value_params
            rent['params'] = params

            # owners
            select_owners = soup_rent.select(
                r'div.md\:p-6:nth-child(1) > div:nth-child(2)')
            owners = select_owners[0].text if select_owners else None
            rent['owners'] = owners

            # conveniences
            select_conveniences = soup_rent.select(
                r'section.bg-white:nth-child(5) > div:nth-child(2)')
            p_conveniences = select_conveniences[0].find_all('p') if select_conveniences else None
            conveniences = [c.text for c in p_conveniences] if p_conveniences else None
            rent['conveniences'] = conveniences

            data[number] = rent
            logger.debug(f'page: {page_number}. parsing flat {number}: Completed!')
    with open(str(path_save) + f"/data_{page_number}.pkl", "wb") as file:
        pickle.dump(data, file)
    logger.info(f'parsing page {page_number}: Completed!')
    data = {}


if __name__ == "__main__":
    path_save = pathlib.Path(PATH_SAVE)
    if not path_save.exists():
        raise FileExistsError('Path not normal!!!')
    with multiprocessing.Pool() as pool:
        pool.map(parser, range(1, NUMBER_PAGES + 1))
