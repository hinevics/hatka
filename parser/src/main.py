import re
from bs4 import BeautifulSoup
import requests
import logging
import colorlog
import pickle

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
            logger.info(f'parsing flat {number}: Start!')
            new_url =  URL_BASE + href['href']
            response = requests.get(new_url)
            soup_rent = BeautifulSoup(response.content, 'html.parser')
            if not str(n) in data.keys():
                rent = {
                    'href': new_url
                }

                title = soup_rent.select('h1.order-1')[0].text
                logger.debug(f'received: title: {title}')
                rent['title'] = title

                adres = soup_rent.select('li.md\:w-auto')[0].text
                logger.debug(f'received: adres: {adres}')

                rent['adres'] = adres

                price = soup_rent.select('.md\:items-center > div:nth-child(1) > h2:nth-child(1)')[0].text
                logger.debug(f'received: price: {price}')
                data[number] = rent
                logger.info(f'parsing flat {number}: Completed!')
        with open(PATH_SAVE + f"/data_{n}.pkl", "wb") as file:
            pickle.dump(data, file)
        logger.info(f'parsing page {n}: Completed!')
        data = {}


if __name__ == "__main__":
    parser()
