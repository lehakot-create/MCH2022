import os
import json

from backend.models import Company
from django.core.management.base import BaseCommand

from prj.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Эта команда заполняет базу данных'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename',
                            type=str, help='Название файла')

    def handle(self, *args, **kwargs):
        with open(os.path.join(BASE_DIR,
                               f'parser/{kwargs["filename"]}.json'),
                  encoding="utf-8") as f:
            data = json.loads(f.read())
            for el in data:
                try:
                    Company.objects.create(
                        id_company=el.get('id_company', None),
                        Company=el.get('Company', None),
                        Direction=el.get('Direction', None),
                        Description=el.get('Description', None),
                        Categories=el.get('Categories', None),
                        Products=el.get('Products', None),
                        Status=el.get('Status', None),
                        INN=el.get('INN', None),
                        OGRN=el.get('OGRN', None),
                        KPP=el.get('KPP', None),
                        Entity=el.get('Entity', None),
                        Employ_number=el.get('Employ_number', None),
                        Region=el.get('Region', None),
                        Locality=el.get('Locality', None),
                        Address=el.get('Address', None),
                        Telephone=el.get('Telephone', None),
                        Post=el.get('Post', None),
                        URL=el.get('URL', None),
                        VK=el.get('VK', None),
                        Instagram=el.get('Instagram', None),
                        Facebook=el.get('Facebook', None),
                        Youtube=el.get('Youtube', None),
                        Catalogs=el.get('Catalogs', None)
                    )
                    print(f'Сделана запись: {el.get("id_company")}')
                except BaseException as e:
                    print(f'{el.get("id_company")} - error - {e}')
            self.stdout.write(
                self.style.SUCCESS('Данные успешно записаны в базу данных'))
