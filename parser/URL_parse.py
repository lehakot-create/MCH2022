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

# conn = psycopg2.connect(dbname='postgres',
#                         user='postgres',
#                         password='postgres',
#                         host='0.0.0.0',
#                         port='5432')
# conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# cursor = conn.cursor()
# create_table_query = '''CREATE TABLE URLs
#                           (ID INT PRIMARY KEY     NOT NULL,
#                           url           TEXT    NOT NULL); '''
# cursor.execute(create_table_query)
# conn.commit()

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


# def write_to_file():
#     """
#     Пишет данные в файл
#     :param persons_url_list:  список данных
#     :return:
#     """
#     dt0_write_file = datetime.now()
#     with open('urls_moscow.txt', 'w') as file:
#         for line in persons_url_list:
#             file.write(f'{line}\n')
#     dt1_write_file = datetime.now()
#     logger.info(f'Время записи в файл {dt1_write_file - dt0_write_file}')


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


# def write_to_postgres():
#     dt0 = datetime.now()
#     for i, url in enumerate(persons_url_list):
#         insert_query = """ INSERT INTO URLs (ID, url) VALUES (%s, %s)"""
#         cursor.execute(insert_query, (i, url))
#         conn.commit()
#     dt1 = datetime.now()
#     logger.info(f'Время записи в Postgres {dt1 - dt0}')


def main():
    """
    Запускает процесс формирования задач, и записывает результат работы в файл
    :return:
    """
    dt0 = datetime.now()

    asyncio.run(create_tasks(226))

    # write_to_file()
    write_to_redis()
    # write_to_postgres()
    # dt0_write_file = datetime.now()
    # with open('urls_moscow.txt', 'w') as file:
    #     for line in persons_url_list:
    #         file.write(f'{line}\n')
    # dt1_write_file = datetime.now()
    # logger.info(f'Время записи в файл {dt1_write_file - dt0_write_file}')

    dt1 = datetime.now()
    logger.info(f'Время выполнения {dt1 - dt0}')


if __name__ == '__main__':
    main()
    # write_redis()
    # print(r.get('1'))

