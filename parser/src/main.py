import re
from bs4 import BeautifulSoup
import requests
import logging
import colorlog
import pickle
import pathlib

from config import PATH_SAVE

# format logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
color_format = '%(log_color)s' + log_format
formatter_console = colorlog.ColoredFormatter(color_format)
formatter_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# all logs
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter_console)
logger.addHandler(console_handler)


def find_number(href: str):
    res = href['aria-label']
    res = re.search(pattern=r'\№(?P<number>\d+)', string=res)
    return res.group('number')


def get_page(url: str, number: int) -> str:
    url = url.format(number=number)
    response = requests.get(url)
    return response


def parser():
    path_save = pathlib.Path(PATH_SAVE)
    if not path_save.exists():
        raise FileExistsError('Path not normal!!!')
    data = {}
    URL_PAGE = r'https://realt.by/belarus/rent/flat-for-long/?page={number}'
    URL_BASE = r'https://realt.by'
    NUMBER_PAGES = 125
    for n in range(1, NUMBER_PAGES + 1):
        logger.info(f'parsing page {n}: Start!')
        html = get_page(url=URL_PAGE, number=n)
        soup = BeautifulSoup(html.content, 'html.parser')
        div_elements_with_data_index = soup.find_all('div', {'data-index': True})

        for rent in div_elements_with_data_index:
            href = rent.find_all('a')[0]
            number = find_number(href)
            logger.debug(f'parsing flat {number}: Start!')
            new_url = URL_BASE + href['href']
            response = requests.get(new_url)
            soup_rent = BeautifulSoup(response.content, 'html.parser')
            if not str(n) in data.keys():
                rent = {
                    'href': new_url
                }

                # Title
                title_list = soup_rent.select('h1.order-1')
                if title_list:
                    title = title_list[0].text
                    logger.debug(f'received: title: {title}')
                else:
                    title = None
                    logger.error(f'received: title: {title}')
                rent['title'] = title

                # Adres
                adres_list = soup_rent.select(r'li.md\:w-auto')
                if adres_list:
                    adres = adres_list[0].text
                    logger.debug(f'received: adres: {adres}')
                else:
                    adres = None
                    logger.error(f'received: adres: {adres}')
                rent['adres'] = adres

                # Price
                price_list = soup_rent.select(
                    r'.md\:items-center > div:nth-child(1) > h2:nth-child(1)')
                if price_list:
                    price = price_list[0].text
                    logger.debug(f'received: price: {price}')
                else:
                    price = None
                    logger.error(f'received: price: {price}')
                rent['price'] = price

                data[number] = rent
                logger.debug(f'parsing flat {number}: Completed!')
        with open(path_save + f"/data_{n}.pkl", "wb") as file:
            pickle.dump(data, file)
        logger.info(f'parsing page {n}: Completed!')
        data = {}


if __name__ == "__main__":
    parser()
