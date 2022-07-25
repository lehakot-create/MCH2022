import os
import environ
import requests


env = environ.Env()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_KEY = os.environ.get('YANDEX_GEOCODER_API_KEY')


def app(address):
    params = {'apikey': API_KEY,
              'format': 'json',
              'geocode': address}
    req = requests.get(f'https://geocode-maps.yandex.ru/1.x/', params=params)
    if req.status_code == '403':
        print(req.text)
        return {'err_code': 403, 'err_detail': address}
    else:
        coords = req.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return tuple(coords.split(' '))


def remove_dublicate(key, queryset):
    """
    Убирает дубликаты из queryset
    :param queryset: получает queryset
    :return: {'categories': [cat1, cat2, cat3, ... cat_n]}
    """
    lst = []
    for dct in queryset:
        if len(dct.get(key)):
            for el in dct.get(key):
                if el not in lst:
                    lst.append(el)
    lst_out = list(map(lambda x: {key: x}, lst))
    return lst_out

