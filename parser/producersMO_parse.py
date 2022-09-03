import asyncio
import aiohttp
import json
import logging
import os
from datetime import datetime

import psycopg2
import redis
import requests
from bs4 import BeautifulSoup


Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logfile_producers.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.INFO
                    )
logger = logging.getLogger()

r = redis.StrictRedis(decode_responses=True)

data_dict = []


async def producers_parse(session: object, url: list):
    """ В аргументе функции указать txt файл со ссылками профилей компаний для парсинга """
    dt0 = datetime.now()

    count = 0

    logger.info(f'Делаю запрос на страницу {url}')

    async with session.get(url=url) as response:
        html_page = await response.text()
        # result = q.content

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
            # print(location)
            data['Region'] = location[0].strip()
            data['Locality'] = location[1].strip()
        except:
            location = soup.find(class_='comp-card-info-a-geo').text.strip()
            # print(location)
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

        data_dict.append(data)


# def read_file(file_name: str):
#     with open(file_name, encoding='utf-8') as file:
#         lines = [line.strip() for line in file.readlines()]
#         return lines


def read_from_redis():
    urls = []
    key = 0
    while True:
        value = r.get(key)
        if value is None:
            logger.info(f'Количество записей {key + 1}')
            return urls
        urls.append(value)
        key += 1
        logger.info(f'Record #{key}')


# def write_to_file():
#     dt0 = datetime.now()
#     with open('data_moscow_full.json', 'w') as json_file:
#         json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
#     dt1 = datetime.now()
#     logger.info(f'Время записи в файл {dt1 - dt0}')


def write_to_postgres():
    print(data_dict)
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')
    # el = {'id_company': '22420', 'Company': 'Simply chips', 'Direction': 'Производство картофельных чипсов',
    #              'Description': 'Вкусные и хрустящие картофельные чипсы Simply chips от российского '
    #                             'производителя. 6 оригинальных вкусов: Гималайская соль, Острый томат, '
    #                             'Пряный томат, Сладкий чили, Сыр пармезан с чесноком и зеленью, Медовая горчица. '
    #                             'Крупная нарезка 2мм и высококачественное подсолнечное масло. Оптовые поставки от '
    #                             '1 коробки по России.',
    #              'Categories': ['Пищевые продукты', 'Снековая продукция', 'Чипсы'], 'Products': [],
    #              'Status': 'Действующая организация', 'INN': '9718092685', 'Entity': 'ООО ГК "ПАРТНЕР"',
    #              'Employ_number': '2', 'Region': 'Москва', 'Locality': 'Московский',
    #              'Address': 'г. Москва, ул.Рябиновая, 45', 'Telephone': '+7 985 274 0858',
    #              'Post': 'simplychips@yandex.ru', 'URL': 'https://simplychips.ru/', 'Catalogs': []}
    # Company.objects.create(
    #     id_company=el.get('id_company', None),
    #     Company=el.get('Company', None),
    #     Direction=el.get('Direction', None),
    #     Description=el.get('Description', None),
    #     Categories=el.get('Categories', None),
    #     Products=el.get('Products', None),
    #     Status=el.get('Status', None),
    #     INN=el.get('INN', None),
    #     OGRN=el.get('OGRN', None),
    #     KPP=el.get('KPP', None),
    #     Entity=el.get('Entity', None),
    #     Employ_number=el.get('Employ_number', None),
    #     Region=el.get('Region', None),
    #     Locality=el.get('Locality', None),
    #     Address=el.get('Address', None),
    #     Telephone=el.get('Telephone', None),
    #     Post=el.get('Post', None),
    #     URL=el.get('URL', None),
    #     VK=el.get('VK', None),
    #     Instagram=el.get('Instagram', None),
    #     Facebook=el.get('Facebook', None),
    #     Youtube=el.get('Youtube', None),
    #     Catalogs=el.get('Catalogs', None)
    # )
    try:
        conn = psycopg2.connect(database='postgres',
                                user='postgres',
                                password='postgres',
                                host='0.0.0.0',
                                port=5432
                                )
        cursor = conn.cursor()

        keys = ['id_company', 'Company', 'Direction', 'Description', 'Categories', 'Products', 'Status', 'INN',
                'OGRN', 'KPP', 'Entity', 'Employ_number', 'Region', 'Locality',
                'Address', 'Telephone', 'Post',
                'URL', 'VK', 'Instagram', 'Facebook',
                'Youtube', 'Catalogs']

        # data_dict = {'id_company': '22420', 'Company': 'Simply chips', 'Direction': 'Производство картофельных чипсов',
        #              'Description': 'Вкусные и хрустящие картофельные чипсы Simply chips от российского '
        #                             'производителя. 6 оригинальных вкусов: Гималайская соль, Острый томат, '
        #                             'Пряный томат, Сладкий чили, Сыр пармезан с чесноком и зеленью, Медовая горчица. '
        #                             'Крупная нарезка 2мм и высококачественное подсолнечное масло. Оптовые поставки от '
        #                             '1 коробки по России.',
        #              'Categories': ['Пищевые продукты', 'Снековая продукция', 'Чипсы'], 'Products': [],
        #              'Status': 'Действующая организация', 'INN': '9718092685', 'Entity': 'ООО ГК "ПАРТНЕР"',
        #              'Employ_number': '2', 'Region': 'Москва', 'Locality': 'Московский',
        #              'Address': 'г. Москва, ул.Рябиновая, 45', 'Telephone': '+7 985 274 0858',
        #              'Post': 'simplychips@yandex.ru',
        #              'URL': 'https://simplychips.ru/', 'Catalogs': []}



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

        for data in data_dict:
            insert_data = []
            for key in keys:
                insert_data.append(data.get(key))
            insert_data.append('false')

            insert_query = """INSERT INTO backend_company (id_company, "Company", "Direction", "Description", "Categories", "Products", 
            "Status", "INN", "OGRN", "KPP", "Entity", "Employ_number", "Region", "Locality", "Address", "Telephone", "Post",
            "URL", "VK", "Instagram", "Facebook", "Youtube", "Catalogs", "is_moderate") 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        # values = (22420, 'Simply chips', 'Производство картофельных чипсов', 'Вкусные и хрустящие картофельные чипсы Simply chips от российского производителя. 6 оригинальных вкусов: Гималайская соль, Острый томат, Пряный томат, Сладкий чили, Сыр пармезан с чесноком и зеленью, Медовая горчица. Крупная нарезка 2мм и высококачественное подсолнечное масло. Оптовые поставки от 1 коробки по России.',
        #           ['Пищевые продукты', 'Снековая продукция', 'Чипсы'],
        #           [],
        #           'Действующая организация',
        #           '9718092685',
        #           '',
        #           '',
        #           'ООО ГК "ПАРТНЕР"',
        #           '2',
        #           'Москва',
        #           'Московский',
        #           'г. Москва, ул.Рябиновая, 45',
        #           '+7 985 274 0858',
        #           'simplychips@yandex.ru',
        #           'https://simplychips.ru/',
        #           '',
        #           '',
        #           '',
        #           '',
        #           [])
            cursor.execute(insert_query, insert_data)

            conn.commit()
            print(f'Сделана запись {data.get("id_company")}')


        # cursor.execute("""INSERT INTO tmp (
        # "id_company", "Company", "Direction", "Description", "Categories", "Products", "Status", "INN",
        #         "OGRN", "KPP", "Entity", "Employ_number", "Region", "Locality", "Address", "Telephone", "Post",
        #         "URL", "VK", "Instagram", "Facebook", "Youtube", "Catalogs"
        # ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        # %s, %s, %s, %s, %s, %s, %s, %s,) """, (insert_data), )
        # cursor.execute("""SELECT * FROM backend_company WHERE "Company"='DeLux' LIMIT 5""")
        # cursor.execute(insert_query, ('21847', 'УпакСнаб'))
        # print(cursor.fetchall())

        # logger.info(f'Элемент записан {item}')

    except psycopg2.OperationalError as e:
        logger.info(f'Ошибка при подключении к БД {e.with_traceback()}')
        conn.rollback()
    except psycopg2.OperationalError.InvalidTextRepresentation as e:
        logger.info(f'Error {e}')

    finally:
        if conn:
            cursor.close()
            conn.close()
            logger.info(f'Соединение с БД Закрыто')


async def create_tasks(lines: list):
    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for line in lines:
            task = asyncio.create_task(producers_parse(session, line))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    dt0 = datetime.now()

    # urls = read_file('urls_moscow.txt')
    urls = read_from_redis()

    asyncio.run(create_tasks(urls))

    # producers_parse(lines)

    # write_to_file()
    write_to_postgres()

    dt1 = datetime.now()
    logger.info(f'Время выполнения {dt1 - dt0}')


if __name__ == '__main__':
    main()
    # write_to_postgres()
