# Generated by Django 3.2.7 on 2021-09-27 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_ingridients'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingridients',
            new_name='Ingredient',
        ),
    ]
