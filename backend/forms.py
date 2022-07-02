from django.forms import ModelForm

from backend.models import Company, Product


class ManufacturerForm(ModelForm):
    class Meta:
        model = Company
        fields = ('Company',
                  'Direction',
                  'Description',
                  'Categories',
                  'Products',
                  'Status',
                  'INN',
                  'OGRN',
                  'KPP',
                  'Entity',
                  'Employ_number',
                  'Region',
                  'Locality',
                  'Address',
                  'Telephone',
                  'Post',
                  'URL',
                  'VK',
                  'Instagram',
                  'Facebook',
                  'Youtube',)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name',
                  'description',
                  'category',)
