from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    user = 'US'
    manufacturer = 'MA'
    choice = [
        (user, 'Пользователь'),
        (manufacturer, 'Производитель'),
    ]
    role = models.CharField(max_length=2, choices=choice, default=user)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_request = models.JSONField(null=True)

    def __str__(self):
        return f'{self.user}'


class ProfileCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.OneToOneField('Company', on_delete=models.CASCADE)


class Company(models.Model):
    user = models.ForeignKey(Profile, verbose_name="user", related_name="companies", on_delete=models.CASCADE, null=True)
    id_company = models.IntegerField(blank=False, unique=True)
    Company = models.CharField(max_length=128, verbose_name='Название компании')
    Direction = models.CharField(max_length=512, blank=True, verbose_name='Направление деятельности')
    Description = models.TextField(null=True, blank=True, verbose_name='Описание')
    Categories = ArrayField(base_field=models.CharField(max_length=128), null=True, blank=True, verbose_name='Категории')
    Products = ArrayField(base_field=models.CharField(max_length=128), null=True, blank=True, verbose_name='Продукты')
    Status = models.CharField(max_length=128, verbose_name='Статус',default='Действующая организация')
    INN = models.BigIntegerField(null=True, verbose_name='ИНН')
    OGRN = models.BigIntegerField(null=True, blank=True, verbose_name='ОГРН')
    KPP = models.BigIntegerField(null=True, blank=True, verbose_name='КПП')
    Entity = models.CharField(max_length=128, null=True, blank=True, verbose_name='Год образования')
    Employ_number = models.IntegerField(null=True, blank=True, verbose_name='Количество сотрудников')
    Region = models.CharField(max_length=128, null=True, verbose_name='Регион', blank=True)
    Locality = models.CharField(max_length=128, null=True, verbose_name='Город', blank=True)
    Address = models.CharField(max_length=128, null=True, verbose_name='Адрес', blank=True)
    Telephone = models.CharField(max_length=128, null=True, verbose_name='Телефон', blank=True)
    Post = models.CharField(max_length=128, null=True, blank=True, verbose_name='Эл.почта')
    URL = models.CharField(max_length=128, null=True, blank=True, verbose_name='Сайт')
    VK = models.CharField(max_length=128, null=True, blank=True)
    Instagram = models.CharField(max_length=128, null=True, blank=True)
    Facebook = models.CharField(max_length=128, null=True, blank=True)
    Youtube = models.CharField(max_length=128, null=True, blank=True)
    Catalogs = ArrayField(models.CharField(max_length=128, null=True, blank=True), blank=True, verbose_name='Каталоги', null=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    is_moderate = models.BooleanField(default=False)
    status_moderation = models.BooleanField(null=True, blank=True)
    comment = models.CharField(max_length=250, null=True, blank=True, verbose_name='Комментарий модератора')

    def __str__(self):
        return f'{self.Company}({self.INN})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('analitics_categories')
        cache.delete('analitics_directions')
        cache.delete('analitics_locality')


class Product(models.Model):
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=64, verbose_name='Наименование')
    description = models.CharField(max_length=512, null=True, verbose_name='Описание', blank=True)
    category = models.CharField(max_length=128, verbose_name='Категория')
    deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f'/product/{self.pk}/'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
