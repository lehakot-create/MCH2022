# Generated by Django 4.0.6 on 2022-08-04 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='id_company',
            field=models.IntegerField(unique=True),
        ),
    ]