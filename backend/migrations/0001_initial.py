

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('id_company', models.IntegerField(null=True, unique=True)),

  
                ('Company', models.CharField(max_length=128, verbose_name='Название компании')),
                ('Direction', models.CharField(blank=True, max_length=512, verbose_name='Направление деятельности')),
                ('Description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('Categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), blank=True, null=True, size=None, verbose_name='Категории')),
                ('Products', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), blank=True, null=True, size=None, verbose_name='Продукты')),
                ('Status', models.CharField(default='Действующая организация', max_length=128, verbose_name='Статус')),
                ('INN', models.BigIntegerField(null=True, verbose_name='ИНН')),
                ('OGRN', models.BigIntegerField(blank=True, null=True, verbose_name='ОГРН')),
                ('KPP', models.BigIntegerField(blank=True, null=True, verbose_name='КПП')),
                ('Entity', models.CharField(blank=True, max_length=128, null=True, verbose_name='Год образования')),
                ('Employ_number', models.IntegerField(blank=True, null=True, verbose_name='Количество сотрудников')),
                ('Region', models.CharField(blank=True, max_length=128, null=True, verbose_name='Регион')),
                ('Locality', models.CharField(blank=True, max_length=128, null=True, verbose_name='Город')),
                ('Address', models.CharField(blank=True, max_length=128, null=True, verbose_name='Адрес')),
                ('Telephone', models.CharField(blank=True, max_length=128, null=True, verbose_name='Телефон')),
                ('Post', models.CharField(blank=True, max_length=128, null=True, verbose_name='Эл.почта')),
                ('URL', models.CharField(blank=True, max_length=128, null=True, verbose_name='Сайт')),
                ('VK', models.CharField(blank=True, max_length=128, null=True)),
                ('Instagram', models.CharField(blank=True, max_length=128, null=True)),
                ('Facebook', models.CharField(blank=True, max_length=128, null=True)),
                ('Youtube', models.CharField(blank=True, max_length=128, null=True)),
                ('Catalogs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=128, null=True), blank=True, null=True, size=None, verbose_name='Каталоги')),

                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),

                ('is_moderate', models.BooleanField(default=False)),
                ('status_moderation', models.BooleanField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=250, null=True, verbose_name='Комментарий модератора')),

            ],
        ),
        migrations.CreateModel(
            name='ProfileCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_company', models.CharField(choices=[('US', 'Пользователь'), ('MA', 'Производитель')], max_length=2)),
                ('last_request', models.JSONField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование')),
                ('description', models.CharField(blank=True, max_length=512, null=True, verbose_name='Описание')),
                ('category', models.CharField(max_length=128, verbose_name='Категория')),
                ('deleted', models.BooleanField(default=False)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='backend.company')),
            ],
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='backend.profile', verbose_name='user'),
        ),

    ]
