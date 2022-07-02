from django_filters import FilterSet
from django.db import models

from .models import Company, Product


class CompanyFilter(FilterSet):
    class Meta:
        model = Company
        fields = ['Company', 'INN', 'Region', 'Locality']


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'category']

