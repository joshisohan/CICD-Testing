# Generated by Django 3.2.7 on 2021-09-23 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_satff',
            new_name='is_staff',
        ),
    ]