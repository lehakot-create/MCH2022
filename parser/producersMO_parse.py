from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup
import json
import os


def producers_parse(producers_txt):

    ''' В аргументе функции указать txt файл со ссылками профилей компаний для парсинга '''

    with open(producers_txt, encoding='utf-8') as file:

        lines = [line.strip() for line in file.readlines()]

        data_dict = []
        count = 0

        for line in lines:
            q = requests.get(line)
            result = q.content

            soup = BeautifulSoup(result, 'lxml')

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
                print(location)
                data['Region'] = location[0].strip()
                data['Locality'] = location[1].strip()
            except:
                location = soup.find(class_='comp-card-info-a-geo').text.strip()
                print(location)
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
            print(f'#{count}: {line} is done')

            data_dict.append(data)

            sleep(randint(2, 5))

        with open('data_moscow_full.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

        return f'Найдено {count} компания(и)'


# producers_parse('urls_moscow.txt')