# Generated by Django 2.0.5 on 2018-05-08 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180426_0122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Учебная дисциплина', 'verbose_name_plural': 'Учебные дисциплины'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Файл', 'verbose_name_plural': 'Файлы'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.RemoveField(
            model_name='specialization',
            name='image',
        ),
    ]
