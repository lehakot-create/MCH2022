import asyncio
import aiohttp
import json
import logging
import os
from datetime import datetime
import environ

import psycopg2
import redis
import requests
from bs4 import BeautifulSoup


env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
database = os.environ.get("SQL_DATABASE")
user = os.environ.get("SQL_USER")
password = os.environ.get("SQL_PASSWORD")
port = os.environ.get("SQL_PORT")


Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logfile_producers.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.INFO
                    )
logger = logging.getLogger()

r = redis.StrictRedis(decode_responses=True)


async def producers_parse(session: object, record: dict, id: int):
    """
    Модуль парсинга страницы производителя
    :param session: получаем объект сессии
    :param record: запись Редис {"url": "url", "processed": "false"}
    :param id: id записи Редис
    :return: результат парсинга в формате dict
    """
    dt0 = datetime.now()

    url = record.get("url")
    count = 0

    logger.info(f'Делаю запрос на страницу {url}')

    async with session.get(url=url) as response:
        html_page = await response.text()

        logger.info(f'Запрос получен')

        soup = BeautifulSoup(html_page, 'lxml')

        ''' ID '''
        id_company = soup.find('div', class_='comp-card comp-card-top node-stat').get('rel').replace('node-', '')

        ''' Название, направление, описание '''
        person = soup.find(class_='manufacturers-card-info-col-1').find('h1').text.strip()
        direction = soup.find(class_='comp-card-info-txt').text.strip()
        description = soup.find(class_="abcomp-desc").text.strip()

        ''' Категория '''
        categories = soup.find_all(class_='category-bott-li')
        categories_item = []
        for item in categories:
            categories_item.append(item.text)

        ''' Продукция '''
        products = soup.find_all(class_='productis-nav-li')
        products_item = []
        for item in products:
            products_item.append(item.text)

        ''' Заполнение словаря компании '''
        data = {
            'id_company': id_company,
            'Company': person,
            'Direction': direction,
            'Description': description,
            'Categories': categories_item,
            'Products': products_item
        }

        ''' Реквизиты '''
        requisites = soup.find_all(class_='brequisits-row')
        for item in range(len(requisites)):
            requisites_key = requisites[item].find('div', class_="brequisits-col-1").text.replace(':', '')

            if requisites_key == 'Статус':
                key = 'Status'
            elif requisites_key == 'ИНН':
                key = 'INN'
            elif requisites_key == 'ОГРН':
                key = 'OGRN'
            elif requisites_key == 'КПП':
                key = 'KPP'
            elif requisites_key == 'Название юр лица':
                key = 'Entity'
            elif requisites_key == 'Кол-во сотрудников':
                key = 'Employ_number'
            else:
                pass

            val = requisites[item].find('div', class_="brequisits-col-2").text
            data[key] = val

        ''' Регион и город '''
        try:
            location = soup.find(class_='comp-card-info-a-geo').text.strip().split(',')
            data['Region'] = location[0].strip()
            data['Locality'] = location[1].strip()
        except:
            location = soup.find(class_='comp-card-info-a-geo').text.strip()
            data['Region'] = location
            data['Locality'] = location

        ''' Контакты и соцсети '''
        contacts = soup.find_all(class_='bconts-row')
        for item in range(len(contacts)):
            try:
                contacts_key = contacts[item].find('div', class_="bconts-col-1").text.replace(':', '')
                if contacts_key == 'Адрес':
                    key = 'Address'
                elif contacts_key == 'Телефон':
                    key = 'Telephone'
                elif contacts_key == 'Почта':
                    key = 'Post'
                elif contacts_key == 'Сайт':
                    key = 'URL'
                elif contacts_key == 'Вконтакте':
                    key = 'VK'
                elif contacts_key == 'Инстаграм':
                    key = 'Instagram'
                elif contacts_key == 'Фейсбук':
                    key = 'Facebook'
                elif contacts_key == 'Ютуб':
                    key = 'Youtube'
                else:
                    pass
                val = contacts[item].find('div', class_="bconts-col-2").text.replace('\n', '')
                data[key] = val
            except:
                pass

        ''' Каталоги '''
        catalogs_item = []

        try:
            catalogs = soup.find('div', class_='abcomp-acts').find_all('a', class_="abcomp-act")
            if os.path.exists(f'catalogs/{person}_{data["INN"]}/'):
                pass
            else:
                os.mkdir(f'catalogs/{person}_{data["INN"]}/')

            for catalog in catalogs:
                download_catalog = catalog.get('href')
                catalog_bytes = requests.get(f'https://xn--b1aedfedwrdfl5a6k.xn--p1ai{download_catalog}').content
                filename = catalog.find(class_='abcomp-name').text

                if os.path.isfile(f'catalogs/{person}_{data["INN"]}/{filename}'):
                    catalogs_item.append(f'catalogs/{person}_{data["INN"]}/{filename}')
                    data['Catalogs'] = catalogs_item

                else:
                    with open(f'catalogs/{person}_{data["INN"]}/{filename}', 'wb') as file:
                        file.write(catalog_bytes)
                    catalogs_item.append(f'catalogs/{person}_{data["INN"]}/{filename}')
                    data['Catalogs'] = catalogs_item

        except:
            data['Catalogs'] = catalogs_item

        ''' счетчик в консоль '''
        count += 1
        print(f'#{count}: {url} is done')
        logger.info(f'Получены данные со страницы {url}')
        dt1 = datetime.now()
        logger.info(f'Время выполнения {dt1 - dt0}')

        write_to_postgres(data, record, id)


def write_to_postgres(data: dict, record: dict, id: int):
    """
    Записываем данные в БД Postgres
    :param data: данные в формате словаря
    :param record: запись Редис {"url": "url", "processed": "false"}
    :param id: id записи Редис
    :return:
    """
    try:
        conn = psycopg2.connect(database=database,
                                user=user,
                                password=password,
                                host="0.0.0.0",
                                port=port
                                )
        cursor = conn.cursor()

        keys = ['id_company', 'Company', 'Direction', 'Description', 'Categories', 'Products', 'Status', 'INN',
                'OGRN', 'KPP', 'Entity', 'Employ_number', 'Region', 'Locality',
                'Address', 'Telephone', 'Post',
                'URL', 'VK', 'Instagram', 'Facebook',
                'Youtube', 'Catalogs']

        cursor.execute("""CREATE TABLE IF NOT EXISTS backend_company(
                        ID SERIAL,
                        id_company INT,
                        Company VARCHAR(128),
                        Direction VARCHAR(512),
                        Description TEXT,
                        Categories VARCHAR(128) ARRAY,
                        Products VARCHAR(128) ARRAY,
                        Status VARCHAR(128),
                        INN BIGINT,
                        OGRN BIGINT,
                        KPP BIGINT,
                        Entity VARCHAR(128),
                        Employ_number INT,
                        Region VARCHAR(128),
                        Locality VARCHAR(128),
                        Address VARCHAR(128),
                        Telephone VARCHAR(128),
                        Post VARCHAR(128),
                        URL VARCHAR(128),
                        VK VARCHAR(128),
                        Instagram VARCHAR(128),
                        Facebook VARCHAR(128),
                        Youtube VARCHAR(128),
                        Catalogs VARCHAR(128) ARRAY
                        );""")

        insert_data = []
        for key in keys:
            insert_data.append(data.get(key))
        insert_data.append('false')

        insert_query = """INSERT INTO backend_company (id_company, "Company", "Direction", "Description", "Categories", "Products", 
        "Status", "INN", "OGRN", "KPP", "Entity", "Employ_number", "Region", "Locality", "Address", "Telephone", "Post",
        "URL", "VK", "Instagram", "Facebook", "Youtube", "Catalogs", "is_moderate") 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        cursor.execute(insert_query, insert_data)

        conn.commit()
        print(f'Сделана запись {data.get("id_company")}')

        url = record.get('url')
        value = {'url': url,
                 'processed': 'true'}
        rval = json.dumps(value)
        r.set(str(id), rval)

    except psycopg2.OperationalError as e:
        logger.info(f'Ошибка при подключении к БД {e.with_traceback()}')
        conn.rollback()
    except psycopg2.OperationalError.InvalidTextRepresentation as e:
        logger.info(f'Error {e}')
    except psycopg2.OperationalError.UniqueViolation as e:
        logger.info(f'Error {e}')

    finally:
        if conn:
            cursor.close()
            conn.close()
            logger.info(f'Соединение с БД Закрыто')


def read_from_redis(id: int):
    """
    Получаем данные из Редис по id
    :param id: id записи
    :return: запись в формате {"url": "url", "processed": "false"}, в остальных случаях None
    """
    try:
        rval = r.get(str(id))
        value = json.loads(rval)
    except json.JSONDecodeError:
        logger.info(f'Ошибка декодирования. Значение: {rval}. Функция: {__name__}')
        return None

    try:
        processed = value.get('processed')
    except AttributeError:
        return None

    if processed == 'false':
        return value


async def create_tasks():
    count = r.get('count')
    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for id in range(1, int(count) + 1):
            record = read_from_redis(id)
            if record is not None:
                task = asyncio.create_task(producers_parse(session, record, id))
                tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    dt0 = datetime.now()

    asyncio.run(create_tasks())

    dt1 = datetime.now()
    logger.info(f'Время выполнения {dt1 - dt0}')


if __name__ == '__main__':
    main()
