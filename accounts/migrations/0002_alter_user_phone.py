# Generated by Django 4.2.11 on 2024-06-14 08:58

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=13, unique=True, validators=[accounts.utils.phone_validator], verbose_name='phone'),
        ),
    ]
