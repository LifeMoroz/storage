# Generated by Django 2.0.4 on 2018-04-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_document_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default='Дефолтное имя', max_length=255, verbose_name='Название'),
            preserve_default=False,
        ),
    ]
