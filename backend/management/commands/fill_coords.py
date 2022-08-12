import datetime

from backend.models import Company
from django.core.management.base import BaseCommand
from django.core.cache import cache

from backend.utils import app


class Command(BaseCommand):
    help = 'Эта команда заполняет в базе данных координаты'

    @staticmethod
    def seconds_left():
        now = datetime.now().time()
        seconds_left = 86400 - (now.hour * 60 * 60
                                + now.minute * 60
                                + now.second)
        return seconds_left

    def handle(self, *args, **kwargs):
        all_company = Company.objects.filter(
            longitude=None, latitude=None)[:10]
        limit = cache.get('limit', None)
        print(f'Limit:{limit}')
        if not limit:
            cache.set('limit', 1, self.seconds_left())
            limit = cache.get('limit', None)
            print(limit)

        if limit == 999:
            self.stdout.write(self.style.ERROR('На сегодня лимит закончился'))
        else:
            for company in all_company:
                if limit < 999:
                    longitude = company.longitude
                    latitude = company.latitude
                    if longitude is None and latitude is None:
                        longitude, latitude = app(company.Address)
                        company.longitude = longitude
                        company.latitude = latitude
                        company.save()
                        print(f'Компании {company.Company} добавлены координаты: долгота-{longitude}; широта-{latitude}')
                        limit += 1
                        cache.set('limit', limit, self.seconds_left())
                else:
                    self.stdout.write(
                        self.style.ERROR('На сегодня лимит закончился'))
