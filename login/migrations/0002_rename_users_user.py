# Generated by Django 3.2 on 2021-04-09 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]