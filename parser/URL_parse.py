from bs4 import BeautifulSoup
import logging
from datetime import datetime
import asyncio
import aiohttp
import redis
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logfile.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.INFO
                    )
logger = logging.getLogger()

r = redis.Redis()

URL = 'https://xn--b1aedfedwrdfl5a6k.xn--p1ai/producers?region=23077&page='

persons_url_list = []


async def url_parse(session: object, url: str):
    """
    Получает страницу с сайта производитель.рф и возвращает с неё все адреса страниц производителей
    :param session:
    :param url: получаем адрес страницы
    :return: возвращаем список с адресами страниц производителей на сайте производитель.рф
    """
    logger.info(f'Делаю запрос на страницу {url}')

    async with session.get(url=url) as response:
        html_page = await response.text()

        logger.info(f'Запрос получен')

        soup = BeautifulSoup(html_page, 'lxml')
        persons1 = soup.find_all(class_='manufacturers-card-img')
        persons2 = soup.find_all(class_='manufacturers-card-img-3')

        for person in persons1:
            person_page_url = person.get('href')
            persons_url_list.append('https://xn--b1aedfedwrdfl5a6k.xn--p1ai' + person_page_url)

        for person in persons2:
            person_page_url = person.get('href')
            persons_url_list.append('https://xn--b1aedfedwrdfl5a6k.xn--p1ai' + person_page_url)

        logger.info(f'Пройдена страница {url}')


async def create_tasks(page: int):
    """
    Создает задачи для парсинга
    :param page: количество страниц с карточками производителей на сайте производитель.рф
    :return:
    """
    connector = aiohttp.TCPConnector(limit_per_host=10)  # ограничиваем количество соединений
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for i in range(0, page):
            url = f'{URL}{i}'

            task = asyncio.create_task(url_parse(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


def write_to_redis():
    """
    Пишем данные в Редис
    :return:
    """
    dt0 = datetime.now()

    for i, url in enumerate(persons_url_list):
        r.set(i, url)

    dt1 = datetime.now()
    logger.info(f'Время записи в Redis {dt1-dt0}')


def main():
    """
    Запускает процесс формирования задач, и записывает результат работы в файл
    :return:
    """
    dt0 = datetime.now()

    asyncio.run(create_tasks(226))

    write_to_redis()

    dt1 = datetime.now()
    logger.info(f'Время выполнения {dt1 - dt0}')


if __name__ == '__main__':
    main()
